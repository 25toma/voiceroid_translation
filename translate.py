# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import translate
from abc import ABCMeta, abstractmethod
import six
import config

#-----$BCj>]%/%i%9(B-----
class TranslateMeta(metaclass=ABCMeta):
    @abstractmethod
    def trans(self, raw_text):
        pass



#-----$B7Q>5%/%i%9(B-----

#$BDL>o$N(Bgoogle$BK]Lu$r;HMQ(B($BL5NA(B)
class TranslateNormal(TranslateMeta):
    def __init__(self):
        self.translator = Translator()
    
    def trans(self, raw_texts):
        trans_texts = []
        for raw_text in raw_texts:
            trans_result = self.translator.translate(raw_text, dest = config.TRANS_LANG)
            trans_texts += [trans_result.text]
        return trans_texts


#google$B$N(B NeuralNet API$B$r;HMQ(B($BM-NA(B)
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

#$B%G%P%C%0MQ(B
if __name__ == "__main__":
    raw_texts = ["Akane-chan is cute yatter!"]
    transObj = TranslateNormal()
    trans_texts = transObj.trans(raw_texts)
    print(trans_texts)
