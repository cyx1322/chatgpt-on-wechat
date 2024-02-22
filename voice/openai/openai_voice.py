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
from gradio_client import Client
import shutil  # 导入shutil模块用于文件操作
logger = logging.getLogger(__name__)
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
            client = Client("http://localhost:9872/")
            temp_file_name = "tmp/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 1000)) + ".wav"
            logger.debug(f"[GRADIO] text_to_Voice temp_file_name={temp_file_name}, input={text}")
            
            result = client.predict(
                "/Users/yixuanchen/Downloads/温迪/vo_SGEQ002_2_venti_09.wav",
                "如果「采风」时看到的景色一模一样，要怎么想出独具特色的诗对呢？!",
                text,  # 这是需要合成的文本
                "中文",
                "凑50字一切",
                5,
                1,
                1,
                False,    
                fn_index=3  # 根据实际的函数索引进行调整
            )

            # 假设result是生成的音频文件的路径
            generated_file_path = result  # 根据实际返回的内容调整变量名和值
            # 将生成的文件移动到目标路径
            shutil.move(generated_file_path, temp_file_name)

            logger.info("[GRADIO] text_to_Voice success")
            reply = temp_file_name  # 返回最终的文件路径
        except Exception as e:
            logger.error(e)
            reply = "遇到了一点小问题，请稍后再问我吧"
        return reply
