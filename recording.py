import base64
from googleapiclient import discovery
import httplib2
import numpy as np
import pyaudio  #録音機能を使うためのライブラリ
import wave     #wavファイルを扱うためのライブラリ
import config   #設定情報


#音声を一時保存するファイル名
WAVE_OUTPUT_FILENAME = "dump.wav"


#----------関数----------

def volume_detection(stream, CHUNK, FRAME_UNIT):
    frame = []
    detect = False
    
    for i in range(FRAME_UNIT):
        data = stream.read(CHUNK)
        x = np.frombuffer(data,dtype="int16")/32768.0
        frame.append(data)
        if x.max() > config.THRESHOLD:
            detect = True
    if detect:
        return frame
    else:
        return None

def recording2wave():
    #基本情報の設定
    FORMAT = pyaudio.paInt16 #音声のフォーマット
    CHANNELS = 1             #モノラル
    RATE = 44100             #サンプルレート
    CHUNK = 2**11            #データ点数
    iDeviceIndex = 0         #録音デバイスのインデックス番号
        
    #無音時、翻訳しない設定
    FRAME_UNIT = int(RATE / CHUNK * config.RECORD_UNIT) #録音フレーム数
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
            frames_per_buffer=CHUNK)
    
    fvoice = None
    while fvoice is None:
        fvoice = volume_detection(stream, CHUNK, FRAME_UNIT)
    
    print ("recording...")
    frames = fvoice
    while True:
        voice = volume_detection(stream, CHUNK, FRAME_UNIT)
        if voice is None:
            break
        else:
            frames+=voice
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
        'speech', 'v1', http=http, discoveryServiceUrl=DISCOVERY_URL, developerKey=config.key)


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
                'languageCode': config.RECORD_LANG, 
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
    raw_text=[]
    for i in response["results"]:
        raw_text.append(i["alternatives"][0]["transcript"])
    return raw_text



#デバッグ実行用    
if __name__ == '__main__': 
    while True:
        print(record())
