# -*- coding: utf-8 -*-
import base64
from googleapiclient import discovery
import httplib2
import numpy as np
import pyaudio  #録音機能を使うためのライブラリ
import wave     #wavファイルを扱うためのライブラリ




#----------重要設定値----------

#APIキーを設定
key = "your API key"

#音声を保存するファイル名
WAVE_OUTPUT_FILENAME = "dump.wav"

#録音したい言語
RECORD_LANG = "en-US"     




#----------関数----------

def volume_detection(stream, CHUNK):
    THRESHOLD = 0.05         #音声検知レベル
    
    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data,dtype="int16")/32768.0
        if x.max() > THRESHOLD:
            return data


def recording2wave():
    #基本情報の設定
    FORMAT = pyaudio.paInt16 #音声のフォーマット
    CHANNELS = 1             #モノラル
    RATE = 44100             #サンプルレート
    CHUNK = 2**11            #データ点数
    iDeviceIndex = 0         #録音デバイスのインデックス番号
        
    #無音時、翻訳しない設定
    RECORD_SECONDS = 5       #音声検知してからの録音時間
    FRAME_NUM = int(RATE / CHUNK * RECORD_SECONDS) #録音フレーム数
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
            frames_per_buffer=CHUNK)
    
    frontData = volume_detection(stream, CHUNK)
    
    frames = [frontData]
    print ("recording...")
    for i in range(0, FRAME_NUM):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")
    
    #--------終了処理---------
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
 
 
 
#APIの情報を返す関数
def get_speech_service():
    #APIのURL情報
    DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                     'version={apiVersion}')
    http = httplib2.Http()
    return discovery.build(
        'speech', 'v1', http=http, discoveryServiceUrl=DISCOVERY_URL, developerKey=key)


def ApplySpeechAPI():
    #音声ファイルを開く
    with open(WAVE_OUTPUT_FILENAME, 'rb') as speech:
        speech_content = base64.b64encode(speech.read()) 
 
    #APIの情報を取得して、音声認識を行う
    service = get_speech_service()
    service_request = service.speech().recognize(
        body={
            'config': {
                'encoding': 'LINEAR16',
                'sampleRateHertz': 44100,
                'languageCode': RECORD_LANG, 
                'enableWordTimeOffsets': 'false',
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    return response


def record():
    recording2wave()
    response = ApplySpeechAPI()
    if "results" not in response:
        return None
    
    #音声情報を全て配列に格納する
    speaksJP=[]
    for i in response["results"]:
        speaksJP.append(i["alternatives"][0]["transcript"])
    return speaksJP



#デバッグ実行用    
if __name__ == '__main__': 
    while True:
        print(record())
