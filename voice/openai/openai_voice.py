"""
google voice service
"""
import json

import openai

from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
from voice.voice import Voice
import requests
from common import const
import datetime, random
import logging

class OpenaiVoice(Voice):
    def __init__(self):
        openai.api_key = conf().get("open_ai_api_key")

    def voiceToText(self, voice_file):
        logger.debug("[Openai] voice file name={}".format(voice_file))
        try:
            file = open(voice_file, "rb")
            result = openai.Audio.transcribe("whisper-1", file)
            text = result["text"]
            reply = Reply(ReplyType.TEXT, text)
            logger.info("[Openai] voiceToText text={} voice file name={}".format(text, voice_file))
        except Exception as e:
            reply = Reply(ReplyType.ERROR, "我暂时还无法听清您的语音，请稍后再试吧~")
        finally:
            return reply

    def textToVoice(self, text):
        try:
            # 使用指定的 API
            url = 'http://127.0.0.1:9880'
            
            # 准备请求参数
            params = {
                'text': text,
                'text_language': 'zh'
            }
            
            # 发送 GET 请求（如果需要 POST 请求，可以相应地修改）
            response = requests.get(url, params=params)
            
            # 生成文件名并保存语音文件，扩展名为 .wav
            file_name = "tmp/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 1000)) + ".wav"
            logging.debug(f"[CUSTOM API] text_to_Voice file_name={file_name}, input={text}")
            
            with open(file_name, 'wb') as f:
                f.write(response.content)
            
            logging.info(f"[CUSTOM API] text_to_Voice success")
            
            # 模拟返回语音文件路径的回应对象（这里简化为直接返回文件名）
            reply = file_name
        except Exception as e:
            logging.error(e)
            reply = "遇到了一点小问题，请稍后再问我吧"
        
        return reply
    
