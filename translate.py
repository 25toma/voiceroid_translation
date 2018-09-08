# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import translate
from abc import ABCMeta, abstractmethod
import six
import config

#-----抽象クラス-----
class TranslateMeta(metaclass=ABCMeta):
    @abstractmethod
    def trans(self, raw_text):
        pass



#-----継承クラス-----

#通常のgoogle翻訳を使用(無料)
class TranslateNormal(TranslateMeta):
    def __init__(self):
        self.translator = Translator()
    
    def trans(self, raw_texts):
        trans_texts = []
        for raw_text in raw_texts:
            trans_result = self.translator.translate(raw_text, dest = config.TRANS_LANG)
            trans_texts += [trans_result.text]
        return trans_texts


#googleの NeuralNet APIを使用(有料)
class TranslateNMT(TranslateMeta):
    def __init__(self):
        self.translate_client = translate.Client()
    
    def trans(self, raw_texts):
        for i in range(len(raw_texts)):
            if isinstance(raw_texts[i], six.binary_type):
                raw_texts[i]=raw_texts[i].decode("utf-8")
        results = [self.translate_client.translate\
                    (raw_text, target_language = config.TRANS_LANG, model = "nmt")\
                    for raw_text in raw_texts]
        trans_texts = [result["translatedText"] for result in results]
        return trans_texts

#デバッグ用
if __name__ == "__main__":
    raw_texts = ["Akane-chan is cute yatter!"]
    transObj = TranslateNormal()
    trans_texts = transObj.trans(raw_texts)
    print(trans_texts)
