from nonebot import get_driver
from nonebot import on_command, on_message
from nonebot.log import logger
from nonebot.params import CommandArg, Matcher, Event
from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent, GroupMessageEvent, MessageSegment

import time
import copy
import difflib
import os
import shutil
import re
import pickle
import random
import importlib
import traceback
import asyncio

from .config import *
global_config = get_driver().config
# logger.info(config) # 这里可以打印出配置文件的内容

from .openai_func import TextGenerator
from .Extension import Extension

global_data = {}  # 用于存储所有数据的字典
global_data_path = f"{config['NG_DATA_PATH']}naturel_gpt.pkl"

global_extensions = {}  # 用于存储所有扩展的字典


""" ======== 定义会话类 ======== """
# 对话类
class Chat:
    preset_key = ''  # 预设标识
    chat_presets = None         # 当前对话预设
    chat_preset_dicts = None    # 预设字典
    is_insilence = False        # 是否处于沉默状态
    chat_attitude = 0           # 对话态度
    silence_time = 0            # 沉默时长
    is_enable = None            # 是否启用

    def __init__(self, chat_key:str, preset_key:str = ''):
        self.chat_presets = {}   # 当前对话预设
        self.chat_preset_dicts = {}   # 预设字典
        self.chat_key = chat_key    # 对话标识
        self.is_enable = True       # 启用会话
        if not preset_key:  # 如果没有预设，选择默认预设
            for pk in presets_dict:
                if presets_dict[pk]['is_default']:
                    preset_key = pk
                    break
            else:   # 如果没有默认预设，则选择第一个预设
                preset_key = list(presets_dict.keys())[0]
        self.change_presettings(preset_key)

    # 更新当前会话的全局对话历史行
    async def update_chat_history_row(self, sender:str, msg: str, require_summary:bool = False) -> None:
        messageunit = tg.generate_msg_template(sender=sender, msg=msg)
        self.chat_presets['chat_history'].append(messageunit)
        logger.info(f"[会话: {self.chat_key}]添加对话历史行: {messageunit}  |  当前对话历史行数: {len(self.chat_presets['chat_history'])}")
        while len(self.chat_presets['chat_history']) > config['CHAT_MEMORY_MAX_LENGTH'] * 2:    # 保证对话历史不超过最大长度的两倍
            self.chat_presets['chat_history'].pop(0)

        if len(self.chat_presets['chat_history']) > config['CHAT_MEMORY_MAX_LENGTH'] and require_summary: # 只有在需要时才进行总结 避免不必要的token消耗
            prev_summarized = f"Summary of last conversation:{self.chat_presets['chat_summarized']}\n\n" \
                if self.chat_presets.get('chat_summarized') else ''
            history_str = '\n'.join(self.chat_presets['chat_history'])
            prompt = (  # 以机器人的视角总结对话历史
                f"{prev_summarized}[Chat]\n"
                f"{history_str}"
                f"\n\n{self.chat_presets['bot_self_introl']}\nSummarize the chat in one paragraph from the perspective of '{self.chat_presets['bot_name']}' and record as much important information as possible from the conversation:"
            )
            if config.get('__DEBUG__'): logger.info(f"生成对话历史摘要prompt: {prompt}")
            res, success = await tg.get_response(prompt, type='summarize')  # 生成新的对话历史摘要
            if success:
                self.chat_presets['chat_summarized'] = res.strip()
            else:
                logger.error(f"生成对话历史摘要失败: {res}")
                return
            # logger.info(f"生成对话历史摘要: {self.chat_presets['chat_summarized']}")
            logger.info(f"摘要生成消耗token数: {tg.cal_token_count(prompt + self.chat_presets['chat_summarized'])}")
            self.chat_presets['chat_history'] = self.chat_presets['chat_history'][-config['CHAT_MEMORY_SHORT_LENGTH']:]

    # 更新对特定用户的对话历史行
    async def update_chat_history_row_for_user(self, sender:str, msg: str, userid:str, username:str, require_summary:bool = False) -> None:
        if userid not in global_preset_userdata[self.preset_key]:
            global_preset_userdata[self.preset_key][userid] = {'chat_history': []}
        messageunit = tg.generate_msg_template(sender=sender, msg=msg)
        global_preset_userdata[self.preset_key][userid]['chat_history'].append(messageunit)
        logger.info(f"添加对话历史行: {messageunit}  |  当前对话历史行数: {len(global_preset_userdata[self.preset_key][userid]['chat_history'])}")
        # 保证对话历史不超过最大长度
        if len(global_preset_userdata[self.preset_key][userid]['chat_history']) > config['USER_MEMORY_SUMMARY_THRESHOLD'] and require_summary:
            prev_summarized = f"Last impression:{global_preset_userdata[self.preset_key][userid].get('chat_summarized')}\n\n" \
                if global_preset_userdata[self.preset_key][userid].get('chat_summarized') else ''
            history_str = '\n'.join(global_preset_userdata[self.preset_key][userid]['chat_history'])
            prompt = (   # 以机器人的视角总结对话
                f"{prev_summarized}[Chat]\n"
                f"{history_str}"
                f"\n\n{self.chat_presets['bot_self_introl']}\nUpdate {username} impressions from the perspective of {self.chat_presets['bot_name']}:"
            )
            if config.get('__DEBUG__'): logger.info(f"生成对话历史摘要prompt: {prompt}")
            res, success = await tg.get_response(prompt, type='summarize')  # 生成新的对话历史摘要
            if success:
                global_preset_userdata[self.preset_key][userid]['chat_impression'] = res.strip()
            else:
                logger.error(f"生成对话印象摘要失败: {res}")
                return
            # logger.info(f"生成对话印象摘要: {global_preset_userdata[self.preset_key][userid]['chat_impression']}")
            logger.info(f"印象生成消耗token数: {tg.cal_token_count(prompt + global_preset_userdata[self.preset_key][userid]['chat_impression'])}")
            global_preset_userdata[self.preset_key][userid]['chat_history'] = global_preset_userdata[self.preset_key][userid]['chat_history'][-config['CHAT_MEMORY_SHORT_LENGTH']:]

    # 修改对话预设
    def change_presettings(self, preset_key:str) -> None:
        if preset_key not in self.chat_preset_dicts:    # 如果聊天预设字典中没有该预设，则从全局预设字典中拷贝一个
            self.chat_preset_dicts[preset_key] = copy.deepcopy(presets_dict[preset_key])
            logger.info(f"从全局预设中拷贝预设 {preset_key} 到聊天预设字典")
        self.chat_presets = self.chat_preset_dicts[preset_key]
        if 'chat_history' not in self.chat_presets: # 如果预设中没有对话历史，则添加一个空的对话历史
            self.chat_presets['chat_history'] = []
        self.preset_key = preset_key

    # 从全局预设更新对话预设
    def update_presettings(self, preset_key='', inplace:bool = False) -> None:
        if preset_key and inplace:  # 如果指定了预设名且是原地更新，则直接覆盖指定预设
            self.chat_preset_dicts[preset_key] = copy.deepcopy(presets_dict[preset_key])
            self.chat_preset_dicts[preset_key]['chat_history'] = []
            if self.get_chat_preset_key() == preset_key:    # 如果当前预设名与指定预设名相同，则更新当前预设
                logger.info(f"预设名相同... {preset_key}")
                self.chat_presets = self.chat_preset_dicts[preset_key]
        try:
            self.chat_presets['bot_self_introl'] = presets_dict[self.preset_key]['bot_self_introl']
            self.chat_presets['bot_name'] = presets_dict[self.preset_key]['bot_name']
        except KeyError:
            logger.error(f"尝试更新预设 {self.preset_key} 时发生错误，预设可能被删除。")

    # 对话 prompt 模板生成
    def get_chat_prompt_template(self, userid: None) -> str:
        # 印象描述
        impression_text = f"[impression]{global_preset_userdata[self.preset_key][userid].get('chat_impression')}\n" \
            if global_preset_userdata[self.preset_key].get(userid, {}).get('chat_impression', None) else ''  # 用户印象描述

        # 对话历史
        offset = 0
        chat_history:str = '\n'.join(self.chat_presets['chat_history'][-(config['CHAT_MEMORY_SHORT_LENGTH'] + offset):])  # 从对话历史中截取短期对话
        while tg.cal_token_count(chat_history) > config['CHAT_HISTORY_MAX_TOKENS']:
            offset += 1 # 如果对话历史过长，则逐行删除对话历史
            chat_history = '\n'.join(self.chat_presets['chat_history'][-(config['CHAT_MEMORY_SHORT_LENGTH'] + offset):])

        # 对话历史摘要
        summary = f"\n\n[Summary]: {self.chat_presets['chat_summarized']}" if self.chat_presets.get('chat_summarized', None) else ''  # 如果有对话历史摘要，则添加摘要

        # 拓展描述
        ext_descs = ''.join([global_extensions[ek].generate_description(chat_history) for ek in global_extensions.keys()])
        # 拓展使用示例
        extension_text = (
            '[Speak options]\n'
            'importrant: The speak option is available if and only if in the following strict format. Multiple options can be used in one reply.\n'
            # '- Random > min:a; max:b (send a random number between a and b)'
            f'{ext_descs}\n'
            'Use format: /#extension_name&param1&param2#/ (parameters are separated by &)\n\n'
            # 'example use in reply: i will send 2 random number /#Random&0&5#/ /#Random&5&10#/\n\n'    # 拓展使用示例 /#拓展名&参数1&参数2#/，参数之间用&分隔
        ) if config.get('NG_ENABLE_EXT') and ext_descs else (
            '[Speak options]\n'
            'No extension is currently available. Do not use the extension function like /#extension_name&param1&param2#/.\n\n'
        )

        # 发言提示
        say_prompt = "(Multiple segment replies are separated by '*;', single quotes are not included)" if config.get('NG_ENABLE_MSG_SPLIT') else ''

        # 返回对话 prompt 模板
        return (    # 返回对话 prompt 模板
            f"{self.chat_presets['bot_self_introl']}"
            f"\n{summary}\n{impression_text}"
            f"{extension_text}"
            # f"以下是与 \"{self.chat_presets['bot_name']}\" 的对话:"
            f"[Chat - current time: {time.strftime('%Y-%m-%d %H:%M:%S')}]\n"
            f"\n{chat_history}\n{self.chat_presets['bot_name']}{say_prompt}:"
        )

    # 获取当前对话bot的名称
    def get_chat_bot_name(self) -> str:
        return self.chat_presets['bot_name']

    # 获取当前对话bot的预设键
    def get_chat_preset_key(self) -> str:
        return self.preset_key

    # 开关当前会话
    def toggle_chat(self, enabled:bool=True) -> None:
        self.is_enable = enabled

    # 获取当前会话描述
    def generate_description(self):
        return f"[{'启用' if self.is_enable else '禁用'}] 会话: {self.chat_key} 预设: {self.get_chat_bot_name()}\n"

""" ======== 读取历史记忆数据 ======== """
# 检测历史数据pickle文件是否存在 不存在则初始化 存在则读取
if os.path.exists(global_data_path):
    with open(global_data_path, 'rb') as f:
        global_data = pickle.load(f)  # 读取历史数据pickle文件
        presets_dict:dict = global_data['PRESETS']  # 用于存储所有人格预设的字典
        global_preset_userdata:dict = global_data['PRESET_USERDATA']  # 用于存储所有人格预设的用户数据的字典
        chat_dict:dict = global_data['CHAT_DICT']  # 用于存储所有对话的字典
        logger.info("读取历史数据成功")
    # 检查所有会话是否合法
    for chat in chat_dict.values():
        # 检查会话对象的 is_enable 属性是否存在 不存在则添加避免更新后使用旧版本数据时出错
        if not hasattr(chat, 'is_enable'):
            chat.is_enable = True
else:   # 如果不存在历史数据json文件，则初始化
    # 检测目录是否存在 不存在则创建
    if not os.path.exists(config['NG_DATA_PATH']):
        os.makedirs(config['NG_DATA_PATH'], exist_ok=True)

    # 创建用于存储所有人格预设的字典
    presets_dict:dict = config['PRESETS']
    for key in presets_dict:
        presets_dict[key]['to_impression'] = {} # 用于存储所有人格对聊天对象印象的字典

    # 创建用于存储所有人格预设的用户数据的字典
    global_preset_userdata:dict = {}
    for key in presets_dict:
        global_preset_userdata[key] = {}

    # 创建用于存储所有对话的字典
    chat_dict:dict = {}
    logger.info("找不到历史数据，初始化成功")

# 记录最后保存数据的时间
last_save_data_time = time.time()

# 读取ApiKeys
api_keys = config['OPENAI_API_KEYS']
logger.info(f"共读取到 {len(api_keys)} 个API Key")

# 初始化对话文本生成器
tg: TextGenerator = TextGenerator(api_keys, {
    'model': config['CHAT_MODEL'],
    'max_tokens': config['REPLY_MAX_TOKENS'],
    'temperature': config['CHAT_TEMPERATURE'],
    'top_p': config['CHAT_TOP_P'],
    'frequency_penalty': config['CHAT_FREQUENCY_PENALTY'],
    'presence_penalty': config['CHAT_PRESENCE_PENALTY'],
    'max_summary_tokens': config['CHAT_MAX_SUMMARY_TOKENS'],
})

""" ======== 加载拓展模块 ======== """
# 加载拓展模块
if config.get('NG_ENABLE_EXT'):
    ext_path = config['NG_EXT_PATH']
    abs_ext_path = os.path.abspath(ext_path)

    # 在当前文件夹下建立一个ext_cache文件夹 用于暂存拓展模块的.py文件以便于动态导入
    if not os.path.exists('ext_cache'):
        os.makedirs('ext_cache', exist_ok=True)
    # 删除ext_cache文件夹下的所有文件和文件夹
    for file in os.listdir('ext_cache'):
        file_path = os.path.join('ext_cache', file)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    # 在ext_cache文件夹下建立一个__init__.py文件 用于标记该文件夹为一个python包
    if not os.path.exists('ext_cache/__init__.py'):
        with open('ext_cache/__init__.py', 'w', encoding='utf-8') as f:
            f.write('')

    # 根据 Extension 文件 生成 Extension.py 并覆盖到拓展模块路径和 ext_cache 文件夹下
    with open(os.path.join(os.path.dirname(__file__), 'Extension.py'), 'r', encoding='utf-8') as f:
        ext_file = f.read()
    with open(f'{ext_path}Extension.py', 'w', encoding='utf-8') as f:
        f.write(ext_file)
    with open(f'ext_cache/Extension.py', 'w', encoding='utf-8') as f:
        f.write(ext_file)

    for tmpExt in config['NG_EXT_LOAD_LIST']:   # 遍历拓展模块列表
        if tmpExt.get('IS_ACTIVE') and tmpExt.get('EXT_NAME'):
            logger.info(f"正在从加载拓展模块 \"{tmpExt.get('EXT_NAME')}\" ...")
            try:
                file_name = tmpExt.get("EXT_NAME") + '.py'  # 拓展模块文件名

                # 复制拓展模块文件到ext_cache文件夹下
                shutil.copyfile(f'{ext_path}{file_name}', f'ext_cache/{file_name}')
                time.sleep(0.3)  # 等待文件复制完成
                # 从 ext_cache 文件夹下导入拓展模块
                CustomExtension:Extension = getattr(importlib.import_module(f'ext_cache.{tmpExt.get("EXT_NAME")}'), 'CustomExtension')
                time.sleep(0.3)  # 等待文件导入完成

                ext = CustomExtension(tmpExt.get("EXT_CONFIG", {}))  # 加载拓展模块并实例化
                global_extensions[ext.get_config().get('name').lower()] = ext  # 将拓展模块添加到全局拓展模块字典中
                logger.info(f"加载拓展模块 {ext} 成功")
            except Exception as e:
                logger.error(f"加载拓展模块 \"{tmpExt.get('EXT_NAME')}\" 失败 | 原因: {e}")


""" ======== 注册消息响应器 ======== """
# 注册消息响应器 收到任意消息时触发
matcher:Matcher = on_message(priority=config['NG_MSG_PRIORITY'], block=config['NG_BLOCK_OTHERS'])
@matcher.handle()
async def handler(event: Event) -> None:
    # 判断用户账号是否被屏蔽
    if event.get_user_id() in config['FORBIDDEN_USERS']:
        logger.info(f"用户 {event.get_user_id()} 被屏蔽，拒绝处理消息")
        return

    sta = time.time()
    sender_name = event.dict().get('sender', {}).get('nickname', '未知')
    resTmplate = (  # 测试用，获取消息的相关信息
        f"收到消息: {event.get_message()}"
        f"\n消息名称: {event.get_event_name()}"
        f"\n消息描述: {event.get_event_description()}"
        f"\n消息来源: {event.get_session_id()}"
        f"\n消息文本: {event.get_plaintext()}"
        f"\n消息主体: {event.get_user_id()}"
        f"\n消息内容: {event.get_message()}"
        f"\n发送者: {sender_name}"
        f"\n是否to-me: {event.is_tome()}"
        # f"\nJSON: {event.json()}"
    )
    if config.get('__DEBUG__'): logger.info(resTmplate)

    # 如果是忽略前缀 或者 消息为空，则跳过处理
    if event.get_plaintext().startswith(config['IGNORE_PREFIX']) or not event.get_plaintext():   
        logger.info("忽略前缀，跳过处理...")
        return

    # 判断群聊/私聊
    if isinstance(event, GroupMessageEvent):
        chat_key = 'group_' + event.get_session_id().split("_")[1]
        chat_type = 'group'
    elif isinstance(event, PrivateMessageEvent):
        chat_key = 'private_' + event.get_user_id()
        chat_type = 'private'
    else:
        logger.info("未知消息来源: " + event.get_session_id())
        return

    # 判断是否已经存在对话
    if chat_key in chat_dict:
        logger.info(f"已存在对话 {chat_key} - 继续对话")
    else:
        logger.info("不存在对话 - 创建新对话")
        # 创建新对话
        chat_dict[chat_key] = Chat(chat_key)
    chat:Chat = chat_dict[chat_key]

    # 判断对话是否被禁用
    if not chat.is_enable:
        logger.info("对话已被禁用，跳过处理...")
        return

    wake_up = False
    # 检测是否包含违禁词
    for w in config['WORD_FOR_FORBIDDEN']:
        if str(w) in event.get_plaintext():
            logger.info(f"检测到违禁词 {w}，拒绝处理...")
            return

    # 唤醒词检测
    for w in config['WORD_FOR_WAKE_UP']:
        if str(w) in event.get_plaintext():
            wake_up = True
            break

    # 随机回复判断
    if random.random() < config['RANDOM_CHAT_PROBABILITY']:
        wake_up = True

    # 判断是否需要回复
    if (    # 如果不是 bot 相关的信息，则直接返回
        (config['REPLY_ON_NAME_MENTION'] and (chat.get_chat_bot_name() in event.get_plaintext())) or \
        (config['REPLY_ON_AT'] and event.is_tome()) or wake_up\
    ):
        # 更新全局对话历史记录
        # chat.update_chat_history_row(sender=sender_name, msg=event.get_plaintext(), require_summary=True)
        await chat.update_chat_history_row(sender=sender_name,
                                    msg=f"@{chat.get_chat_bot_name()} {event.get_plaintext()}" if event.is_tome() and chat_type=='group' else event.get_plaintext(),
                                    require_summary=False)
        logger.info("符合 bot 发言条件，进行回复...")
    else:
        await chat.update_chat_history_row(sender=sender_name, msg=event.get_plaintext(), require_summary=False)
        logger.info("不是 bot 相关的信息，记录但不进行回复")
        return

    # 记录对用户的对话信息
    await chat.update_chat_history_row_for_user(sender=sender_name, msg=event.get_plaintext(), userid=event.get_user_id(), username=sender_name, require_summary=False)

    # 潜在人格唤醒机制 *待实现
    # 通过对话历史中的关键词进行检测，如果检测到潜在人格，进行累计，达到一定阈值后，抢占当前生效的人格

    # 主动聊天参与逻辑 *待定方案
    # 达到一定兴趣阈值后，开始进行一次启动发言准备 收集特定条数的对话历史作为发言参考
    # 启动发言后，一段时间内兴趣值逐渐下降，如果随后被呼叫，则兴趣值提升
    # 监测对话历史中是否有足够的话题参与度，如果有，则继续提高话题参与度，否则，降低话题参与度
    # 兴趣值影响发言频率，兴趣值越高，发言频率越高
    # 如果监测到对话记录中有不满情绪(如: 闭嘴、滚、不理你、安静等)，则大幅降低兴趣值并且降低发言频率，同时进入一段时间的沉默期(0-120分钟)
    # 沉默期中降低响应"提及"的概率，沉默期中被直接at，则恢复一定兴趣值提升兴趣值并取消沉默期
    # 兴趣值会影响回复的速度，兴趣值越高，回复速度越快
    # 发言概率贡献比例 = (随机值: 10% + 话题参与度: 50% + 兴趣值: 40%) * 发言几率基数(0.01~1.0)

    sta_time:float = time.time()

    # 生成对话 prompt 模板
    prompt_template = chat.get_chat_prompt_template(userid=event.get_user_id())
    if config.get('__DEBUG__'): logger.info("对话 prompt 模板: \n" + prompt_template)

    raw_res, success = await tg.get_response(prompt=prompt_template, type='chat', custom={'bot_name': chat.get_chat_bot_name(), 'sender_name': sender_name})  # 生成对话结果
    if not success:  # 如果生成对话结果失败，则直接返回
        logger.info("生成对话结果失败，跳过处理...")
        await matcher.finish(raw_res)

    # 输出对话原始响应结果
    if config.get('__DEBUG__'): logger.info(f"原始回应: {raw_res}")

    # 用于存储最终回复顺序内容的列表
    reply_list = []

    # 按照拓展调用的格式，将所有非调用部分去除后再将剩余信息切分放入回复列表
    pattern = '/#.*?#/'
    reply_list = re.sub(pattern, '', raw_res).split()
    # 对分割后的对话再次根据 '*;' 进行分割，表示对话结果中的分句，处理结果为列表，其中每个元素为一句话
    if config.get('NG_ENABLE_MSG_SPLIT'):
        reply_list = [reply.strip() for reply in re.split(r'\*;', ' '.join(reply_list)) if reply.strip()]

    if config.get('__DEBUG__'): logger.info("分割对话结果: " + str(reply_list))

    # 重置所有拓展调用次数
    for ext_name in global_extensions.keys():
        global_extensions[ext_name].reset_call_times()

    # 分割对话结果提取出所有 "/#拓展名&参数1&参数2#/" 格式的拓展调用指令 参数之间用&分隔
    ext_calls = re.findall(r"/#(.+?)#/", raw_res)
    for ext_call_str in ext_calls:  # 遍历所有拓展调用指令
        ext_name, *ext_args = ext_call_str.split('&')
        if ext_name.lower() in global_extensions.keys():
            # 提取出拓展调用指令中的参数为字典
            ext_args_dict:dict = {}
            # 按照参数顺序依次提取参数值
            for arg_name in global_extensions[ext_name].get_config().get('arguments').keys():
                if len(ext_args) > 0:
                    ext_args_dict[arg_name] = ext_args.pop(0)
                else:
                    ext_args_dict[arg_name] = None

            logger.info(f"检测到拓展调用指令: {ext_name} {ext_args_dict} | 正在调用拓展模块...")
            # 调用拓展的call方法
            try:
                ext_res:dict = await global_extensions[ext_name].call(ext_args_dict)
                if config.get('__DEBUG__'): logger.info(f"拓展 {ext_name} 返回结果: {ext_res}")
                if ext_res is not None:
                    # 将拓展返回的结果插入到回复列表的最后
                    reply_list.append(ext_res)
            except Exception as e:
                logger.error(f"调用拓展 {ext_name} 时发生错误: {e}")
                if config.get('__DEBUG__'): logger.error(f"[拓展 {ext_name}] 错误详情: {traceback.format_exc()}")
                ext_res = None
                # 将错误的调用指令从原始回复中去除，避免bot从上下文中学习到错误的信息
                raw_res = raw_res.replace(f"/#{ext_call_str}#/", '')
        else:
            logger.error(f"未找到拓展 {ext_name}，跳过调用...")
            # 将错误的调用指令从原始回复中去除，避免bot从上下文中学习到错误的信息
            raw_res = raw_res.replace(f"/#{ext_call_str}#/", '')

    if config.get('__DEBUG__'): logger.info(f"回复序列内容: {reply_list}")

    res_times = config.get('NG_MAX_RESPONSE_PER_MSG', 3)  # 获取每条消息最大回复次数
    # 根据回复内容列表逐条发送回复
    for reply in reply_list:
        # 判断回复内容是否为str
        if isinstance(reply, str) and reply.strip():
            await matcher.send(reply)
        else:
            for key in reply:   # 遍历回复内容类型字典
                if key == 'text' and reply.get(key) and reply.get(key).strip():    # 如果回复内容为文本，则发送文本
                    await matcher.send(reply.get(key))
                elif key == 'image' and reply.get(key): # 如果回复内容为图片，则发送图片
                    await matcher.send(MessageSegment.image(file=reply.get(key, '')))
                elif key == 'voice' and reply.get(key): # 如果回复内容为语音，则发送语音
                    logger.info(f"回复语音消息: {reply.get(key)}")
                    await matcher.send(Message(MessageSegment.record(file=reply.get(key), cache=0)))

                res_times -= 1
                if res_times < 1:  # 如果回复次数超过限制，则跳出循环
                    break
        await asyncio.sleep(1.5)  # 每条回复之间间隔1.5秒

    cost_token = tg.cal_token_count(prompt_template + raw_res)  # 计算对话结果的 token 数量

    while time.time() - sta_time < 1.5:   # 限制对话响应时间
        time.sleep(0.1)

    logger.info(f"token消耗: {cost_token} | 对话响应: \"{raw_res}\"")
    await chat.update_chat_history_row(sender=chat.get_chat_bot_name(), msg=raw_res, require_summary=True)  # 更新全局对话历史记录
    # 更新对用户的对话信息
    await chat.update_chat_history_row_for_user(sender=chat.get_chat_bot_name(), msg=raw_res, userid=event.get_user_id(), username=sender_name, require_summary=True)
    save_data()  # 保存数据
    if config.get('__DEBUG__'): logger.info(f"对话响应完成 | 耗时: {time.time() - sta_time}s")

""" ======== 注册指令响应器 ======== """
# 人格设定指令 用于设定人格的相关参数
identity:Matcher = on_command("identity", aliases={"人格设定", "人格", "rg"}, priority=2, block=True)
@identity.handle()
async def _(event: Event, arg: Message = CommandArg()):
    is_progress = False
    # 判断是否是禁止使用的用户
    if event.get_user_id() in config.get('FORBIDDEN_USERS', []):
        await identity.finish(f"您的账号({event.get_user_id()})已被禁用，请联系管理员。")

    # 判断群聊/私聊
    if isinstance(event, GroupMessageEvent):
        chat_key = 'group_' + event.get_session_id().split("_")[1]
    elif isinstance(event, PrivateMessageEvent):
        chat_key = 'private_' + event.get_user_id()
    else:
        logger.info("未知消息来源: " + event.get_session_id())
        return

    # 判断是否已经存在对话
    if chat_key in chat_dict:
        logger.info(f"已存在对话 {chat_key} - 继续对话")
    else:
        logger.info("不存在对话 - 创建新对话")
        # 创建新对话
        chat_dict[chat_key] = Chat(chat_key)
    chat:Chat = chat_dict[chat_key]

    cmd:str = arg.extract_plain_text()
    logger.info(f"接收到指令: {cmd} | 来源: {chat_key}")
    presets_show_text = '\n'.join([f'  -> {k + " (当前)" if k == chat.get_chat_preset_key() else k}' for k in list(presets_dict.keys())])

    if not cmd:
        await identity.finish((
            f"会话: {chat_key} [{'启用' if chat.is_enable else '禁用'}]\n"
            f"当前可用人格预设有:\n"
            f"{presets_show_text}\n"
            f"=======================\n"
            f"+ 使用预设: rg 设定 <预设名>\n"
            f"+ 查询预设: rg 查询 <预设名>\n"
            f"+ 更新预设: rg 更新 <预设名> <人格信息>\n"
            f"+ 添加预设: rg 添加 <预设名> <人格信息>\n"
            f"Tip: <人格信息> 是一段第三人称的人设说明(不超过200字, 不包含空格)\n"
        ))

    elif cmd in ['admin']:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("您没有权限执行此操作！")
        await identity.finish((
            f"当前可用人格预设有:\n"
            f"{presets_show_text}\n"
            f"=======================\n"
            f"+ 使用预设: rg 设定 <预设名> <-all?>\n"
            f"+ 查询预设: rg 查询 <预设名>\n"
            f"+ 更新预设: rg 更新 <预设名> <人格信息>\n"
            f"+ 添加预设: rg 添加 <预设名> <人格信息>\n"
            f"+ 删除预设(管理): rg 删除 <预设名>\n"
            f"+ 锁定预设(管理): rg 锁定 <预设名>\n"
            f"+ 解锁预设(管理): rg 解锁 <预设名>\n"
            f"+ 开启会话(管理): rg <开启/on> <-all?>\n"
            f"+ 停止会话(管理): rg <关闭/off> <-all?>\n"
            f"+ 停止会话(管理): rg <会话/chats>\n"
            f"+ 重置会话(管理): rg <重置/reset> <-all?>\n"
            f"+ 拓展信息(管理): rg <拓展/ext>\n"
            f"Tip: <人格信息> 是一段第三人称的人设说明(不超过200字, 不包含空格)\n"
        ))

    elif (cmd.split(' ')[0] in ["设定", "set"]) and len(cmd.split(' ')) >= 2:
        target_preset_key = cmd.split(' ')[1]
        if target_preset_key not in presets_dict:
            # 如果预设不存在，进行逐一进行字符匹配，选择最相似的预设
            target_preset_key = difflib.get_close_matches(target_preset_key, presets_dict.keys(), n=1, cutoff=0.3)
            if len(target_preset_key) == 0:
                await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
            else:
                target_preset_key = target_preset_key[0]
                await identity.send(f"预设不存在! 已为您匹配最相似的预设: {target_preset_key} v(￣▽￣)v")

        if len(cmd.split(' ')) >= 2 and cmd.split(' ')[2] == '-all':
            if str(event.user_id) not in config['ADMIN_USERID']:
                await identity.finish("您没有权限执行此操作！")
            for chat_key in chat_dict.keys():
                chat_dict[chat_key].change_presettings(target_preset_key)
            await identity.send(f"应用预设: {target_preset_key} (￣▽￣)-ok! (所有会话)")
        else:
            if chat_key in chat_dict:
                chat:Chat = chat_dict[chat_key]
                chat.change_presettings(target_preset_key)
            else:
                chat:Chat = Chat(chat_key, target_preset_key)
                chat_dict[chat_key] = chat
            await identity.send(f"应用预设: {target_preset_key} (￣▽￣)-ok!")
        is_progress = True

    elif (cmd.split(' ')[0] in ["查询", "query"]) and len(cmd.split(' ')) >= 2:
        target_preset_key = cmd.split(' ')[1]
        if target_preset_key not in presets_dict:
            # 如果预设不存在，进行逐一进行字符匹配，选择最相似的预设
            target_preset_key = difflib.get_close_matches(target_preset_key, presets_dict.keys(), n=1, cutoff=0.3)
            if len(target_preset_key) == 0:
                await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
            else:
                target_preset_key = target_preset_key[0]
                await identity.send(f"预设不存在! 帮您匹配最相似的预设: {target_preset_key} v(￣▽￣)v")
        is_progress = True
        await identity.finish(f"预设: {target_preset_key} | 人设信息:\n    {presets_dict[target_preset_key]['bot_self_introl']}")

    elif (cmd.split(' ')[0] in ["更新", "update"]) and len(cmd.split(' ')) >= 3:
        target_preset_key = cmd.split(' ')[1]
        if target_preset_key not in presets_dict:
            await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
        if presets_dict[target_preset_key]['is_locked'] and (str(event.user_id) not in config['ADMIN_USERID']):
            await identity.finish("该预设被神秘力量锁定了! 不能编辑呢 (＠_＠;)")
        presets_dict[target_preset_key]['bot_self_introl'] = cmd.split(' ', 2)[2]
        is_progress = True
        await identity.send(f"更新预设: {target_preset_key} 成功! (￣▽￣)")

    elif (cmd.split(' ')[0] in ["添加", "new"]) and len(cmd.split(' ')) >= 3:
        target_preset_key = cmd.split(' ')[1]
        introl = cmd.split(' ', 2)[2]
        if target_preset_key in presets_dict:
            await identity.finish("预设已存在! 请检查后重试!")
        presets_dict[target_preset_key] = {
            'bot_name': target_preset_key,
            'is_locked': False,
            'is_default': False,
            'bot_self_introl': introl,
        }
        is_progress = True
        await identity.send(f"添加预设: {target_preset_key} 成功! (￣▽￣)")

    elif (cmd.split(' ')[0] in ["删除", "del"]) and len(cmd.split(' ')) == 2:
        target_preset_key = cmd.split(' ')[1]
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        if target_preset_key not in presets_dict:
            await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
        del presets_dict[target_preset_key]
        is_progress = True
        await identity.send(f"删除预设: {target_preset_key} 成功! (￣▽￣)")

    elif (cmd.split(' ')[0] in ["锁定", "lock"]) and len(cmd.split(' ')) == 2:
        target_preset_key = cmd.split(' ')[1]
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        if target_preset_key not in presets_dict:
            await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
        presets_dict[target_preset_key]['is_locked'] = True
        is_progress = True
        await identity.send(f"锁定预设: {target_preset_key} 成功! (￣▽￣)")

    elif (cmd.split(' ')[0] in ["解锁", "unlock"]) and len(cmd.split(' ')) == 2:
        target_preset_key = cmd.split(' ')[1]
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        if target_preset_key not in presets_dict:
            await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
        presets_dict[target_preset_key]['is_locked'] = False
        is_progress = True
        await identity.send(f"解锁预设: {target_preset_key} 成功! (￣▽￣)")

    elif cmd in ["拓展", "ext"]:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        # 查询所有拓展插件并生成汇报信息
        ext_info = ''
        for ext in global_extensions.values():
            ext_info += f"  {ext.generate_description()}"
        await identity.finish((
            f"当前已加载的拓展插件:\n{ext_info}"
        ))

    elif cmd in ["开启", "on"]:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        chat.toggle_chat(enabled=True)
        await identity.finish("已开启会话! <(￣▽￣)>")

    elif (cmd.split(' ')[0] in ["开启", "on"]) and len(cmd.split(' ')) == 2:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        if cmd.split(' ')[1] == '-all':
            for c in chat_dict.values():
                c.toggle_chat(enabled=True)
        await identity.finish("已开启所有会话! <(￣▽￣)>")

    elif cmd in ["关闭", "off"]:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        chat.toggle_chat(enabled=False)
        await identity.finish("已停止会话! <(＿　＿)>")

    elif (cmd.split(' ')[0] in ["关闭", "off"]) and len(cmd.split(' ')) == 2:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        if cmd.split(' ')[1] == '-all':
            for c in chat_dict.values():
                c.toggle_chat(enabled=False)
        await identity.finish("已停止所有会话! <(＿　＿)>")

    elif (cmd.split(' ')[0] in ["重置", "reset"]) and len(cmd.split(' ')) == 2:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        target_preset_key = cmd.split(' ')[1]
        tmp_preset_key = chat.get_chat_preset_key()
        if target_preset_key == '-all': # 重置所有预设
            chat.chat_presets = {}      # 当前对话预设
            chat.chat_preset_dicts = {} # 预设字典
            chat.change_presettings(tmp_preset_key)
            await identity.finish("已重置当前会话所有预设! <(￣▽￣)>")
        if target_preset_key not in presets_dict:
            await identity.finish("找不到匹配的人格预设! 是不是手滑了呢？(；′⌒`)")
        chat.update_presettings(preset_key=tmp_preset_key, inplace=True)    # 更新当前预设并覆盖
        await identity.finish(f"已重置当前会话预设: {target_preset_key}! <(￣▽￣)>")

    elif cmd.split(' ')[0] == "debug":
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        debug_cmd = cmd.split(' ')[1]
        if debug_cmd == 'show':
            await identity.finish(str(chat_dict))
        elif debug_cmd == 'run':
            await identity.finish(str(exec(cmd.split(' ', 2)[2])))

    elif cmd in ["会话", "chats"]:
        if str(event.user_id) not in config['ADMIN_USERID']:
            await identity.finish("对不起！你没有权限进行此操作 ＞﹏＜")
        chat_info = ''
        for chat in chat_dict.values():
            chat_info += f"+ {chat.generate_description()}"
        await identity.finish((f"当前已加载的会话:\n{chat_info}"))

    else:
        await identity.finish("输入的命令好像有点问题呢... 请检查下再试试吧！ ╮(>_<)╭")

    if is_progress: # 如果有编辑进度，进行数据保存
        # 更新所有全局预设到会话预设中
        for chat in chat_dict.values():
            chat.update_presettings()
        # 更新全局预设数据
        for key in presets_dict:
            global_preset_userdata[key] = {}
        logger.info(f"用户: {event.get_user_id()} 进行了人格预设编辑: {cmd}")
        save_data()  # 保存数据

""" ======== 保存记忆数据 ======== """
# 保存数据到本地
def save_data():
    global last_save_data_time
    if time.time() - last_save_data_time < 60:  # 如果距离上次保存时间不足60秒则不保存
        return
    global_data['PRESETS'] = presets_dict
    global_data['PRESET_USERDATA'] = global_preset_userdata
    global_data['CHAT_DICT'] = chat_dict
    # 检测目录是否存在 不存在则创建
    if not os.path.exists(config['NG_DATA_PATH']):
        os.makedirs(config['NG_DATA_PATH'], exist_ok=True)
    # 保存到pickle文件
    with open(global_data_path, 'wb') as f:
        pickle.dump(global_data, f)
    last_save_data_time = time.time()
    logger.info("数据保存成功")
