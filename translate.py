# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import translate
from abc import ABCMeta, abstractmethod
import six
import config

#-----$BCj>]%/%i%9(B-----
class TranslateMeta(metaclass=ABCMeta):
    @abstractmethod
    def trans(self, speaksEN):
        pass



#-----$B7Q>5%/%i%9(B-----

#$BDL>o$N(Bgoogle$BK]Lu$r;HMQ(B($BL5NA(B)
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


#google$B$N(B NeuralNet API$B$r;HMQ(B($BM-NA(B)
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

#$B%G%P%C%0MQ(B
if __name__ == "__main__":
    speaksEN = ["Akane-chan is cute yatter!"]
    transObj = TranslateNormal()
    speaksJP = transObj.trans(speaksEN)
    print(speaksJP)
