# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import translate
from abc import ABCMeta, abstractmethod
import six
import config

#-----抽象クラス-----
class TranslateMeta(metaclass=ABCMeta):
    @abstractmethod
    def trans(self, speaksEN):
        pass



#-----継承クラス-----

#通常のgoogle翻訳を使用(無料)
class TranslateNormal(TranslateMeta):
    def __init__(self, LANG = "ja"):
        self.translator = Translator()
        self.mdest = LANG
    
    def trans(self, speaksEN):
        speaksJP = []
        for speakEN in speaksEN:
            transObj = self.translator.translate(speakEN,dest=self.mdest)
            speaksJP += [transObj.text]
        return speaksJP


#googleの NeuralNet APIを使用(有料)
class TranslateAPI(TranslateMeta):
    def __init__(self, LANG = "ja"):
        self.mdest = LANG
        self.translate_client = translate.Client()
    
    def trans(self, speaksEN):
        for i in range(len(speaksEN)):
            if isinstance(speaksEN[i],six.binary_type):
                speaksEN[i]=speaksEN[i].decode("utf-8")
        results = [self.translate_client.translate\
                    (speakEN, target_language=self.mdest, model="nmt")\
                    for speakEN in speaksEN]
        speaksJP = [result["translatedText"] for result in results]
        return speaksJP

#デバッグ用
if __name__ == "__main__":
    speaksEN = ["Akane-chan is cute yatter!"]
    transObj = TranslateNormal()
    speaksJP = transObj.trans(speaksEN)
    print(speaksJP)
