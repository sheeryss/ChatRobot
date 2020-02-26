import urllib
import requests
import chr_to_mp3
import mp3_to_chr
import json
from aip import AipSpeech
import wave
from pydub import AudioSegment
from pygame import mixer 
from pyaudio import PyAudio,paInt16
import time
import os

#实现录音
def start_record():#实现录音
    try:
        pa=PyAudio()
        stream=pa.open(format = paInt16,channels=1,rate=8000,input=True,frames_per_buffer=2000)
        my_buf=[]
        count=0
        print("正在录音")
        while count<2*7:#控制录音时间,7秒
            audio= stream.read(2000)
            my_buf.append(audio)
            count+=1
        save_record('01.wav',my_buf)#调用保存音频文件函数
        stream.close()
        print("录音完成！")
        return True
    except:
        print('start_record failed')

#保存录音文件
def save_record(filename,data):
    try:
        wf=wave.open(filename,'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(8000)
        wf.writeframes(b"".join(data))
        wf.close()
    except:
        print('save_record failed')

#录音转成文字
def get_chat_text():
    try:
        APP_ID = '16007034'
        API_KEY = '9cVZDkCrl0sZP3wpQlMeqZq2'
        SECRET_KEY = 'lGTYdBrcomGUAgfPCt2jrYO9Rg68IMAB'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return fp.read()
        ret = client.asr(get_file_content('01.wav'), 'wav', 16000, {'dev_pid': 1537, })
        print('获取识别到的文字 : ', ret['result'][0])#获取识别到的文字
        return ret['result'][0]
    except:
        print('get_chat_text failed')

#文字提交给图灵并返回理解结果
def post_chat(chat_text):
    try:
        url = "http://openapi.tuling123.com/openapi/api/v2"
        data = {
            "perception": {
                "inputText": {
                    "text": ""
                },
                "selfInfo": {
                    "location": {
                        "city": "成都",
                    }
                }
            },
            "userInfo": {
                "apiKey": "56807c2c01c8497ab879e69d71f100fc",
                "userId": "test"
            }
        }
        data['perception']['inputText']['text'] = chat_text
        data['userInfo']['apiKey'] = list_api[i]
        print(data)
        header = {"Referer": "http://www.tuling123.com/member/robot/1140264/center/frame.jhtml?page=0&child=0","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36"}
        tuling = requests.post(url, json=data, headers=header)
        conent = tuling.json()
        print('语音返回文字 ： ', conent)
        return conent
    except:
        print('post_chat failed')

#播放理解后的语音
def play_audio():
    try:
        mixer.init()
        mixer.music.load('auido.mp3')
        mixer.music.play()
        time.sleep(3)
        mixer.music.stop()
    except:
        print('play_audio failed')

#主函数
if __name__ == '__main__':
    while(1):
        try:
            result = start_record()
            if(result) :
                i=0
                list_api = ['56807c2c01c8497ab879e69d71f100fc','c6cd95abb0784aee8a8bc322d9c06cfb','6d842f11ec7f4fd4bb62472275643e05', 'b78b6d2f8c374b29b427975db0812715','d27ff782be0c400e8f6b7af0d0c6c039']
                chat_text = get_chat_text()
                #处理请求次数超限制的情况（5个robot循环）
                for i in range(0,5):
                    response = post_chat(chat_text)
                    if (response['intent']['code'] == 4003):
                        continue
                    else:
                        break
                #文字转语音
                chr_to_mp3.change_to_mp3(response['results'][0]['values']['text'])
                play_audio()
            else:
                print('save record failed')
        except:
            print('work failed')    
