# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
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
        from googletrans import Translator
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
        from google.cloud import translate
        self.translate_client = translate.Client()
    
    def trans(self, raw_texts):
        import six
        for i in range(len(raw_texts)):
            if isinstance(raw_texts[i], six.binary_type):
                raw_texts[i]=raw_texts[i].decode("utf-8")
        results = [self.translate_client.translate\
                    (raw_text, target_language = config.TRANS_LANG, model = "nmt")\
                    for raw_text in raw_texts]
        trans_texts = [result["translatedText"] for result in results]
        return trans_texts

#Recruit$B$N(B A3RT$B$r;HMQ(B
class Communicate_A3RT(TranslateMeta):
    def __init__(self):
        self.URL = "https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk"
        self.okCode = 200

    def trans(self, raw_texts):
        import json
        import requests
        while type(raw_texts) is list:
            raw_texts = "$B!#(B".join(raw_texts)
        params = {
            "apikey" : (None, config.A3RTkey),
            "query" : (None, raw_texts),
        }
        response = requests.post(self.URL, files = params)
        parsed = json.loads(response.text)
        if response.status_code == self.okCode:
            text = []
            for colume in parsed["results"]:
                text += [colume["reply"]]
            return text
        else:
            return parsed["message"]

    def response_analyze(self,response):
        print(dir(response))
        print("-"*10)
        print(response.connection)
        print("-"*10)
        print(response.content)
        print("-"*10)
        print(response.encoding)
        print("-"*10)
        print(response.headers)
        print("-"*10)
        print(response.history)
        print("-"*10)
        print(response.json)
        print("-"*10)
        print(response.ok)
        print("-"*10)
        print(response.raw)
        print("-"*10)
        print(response.reason)
        print("-"*10)
        print(response.request)
        print("-"*10)
        print(response.status_code)
        print("-"*10)
        print(response.text)
        print("-"*10)
        print(response.url)

#$B%G%P%C%0MQ(B
if __name__ == "__main__":
    raw_texts = ["Akane-chan is cute yatter!"]
    transObj = TranslateNormal()
    trans_texts = transObj.trans(raw_texts)
    print(trans_texts)
