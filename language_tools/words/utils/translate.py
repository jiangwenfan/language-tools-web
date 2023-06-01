import hashlib
import json
import os
import time
import uuid
from abc import ABCMeta, abstractmethod

import requests
from django.conf import settings
from django.db.models import QuerySet
from ielts.models import WordModel

from ..models import TranslateProviderModel, TranslateWordDataModel


class TranslateHandle(metaclass=ABCMeta):

    def get_unknown_words(self,words) -> list[str]:
        """获取不存在的"""
        exist_words: list[str] = [word_obj.name for word_obj in WordModel.objects.all()]

        new_words: set = set(words) - set(exist_words)

        return list(new_words)
    
    def get_queryset(self) -> QuerySet:
        #获取settings中启用的provider
        provider_name_en: str = settings.TRANSLATE_PROVIDER
        local_words_info :QuerySet =TranslateProviderModel.objects.get(name_en=provider_name_en).words.all()
        return local_words_info
    
    @abstractmethod
    def get_mp3_url(self,dict_info:dict) -> dict:
        ...

    @abstractmethod
    def real_write_word_table(self,dict_info: dict) -> str:
        ...

    def write_word_table(self,dict_info: dict):
        
        # download
        url = self.get_mp3_url(dict_info)

        self.download_mp3_file(url)

        # write
        self.real_write_word_table(dict_info)



    def download_mp3_file(self,url: str,file_id: str):
        response = requests.get(url=url)
        with open(file_id,"wb") as f:
            f.write(response.data)

    def get_not_local_dict_info(self,new_words: list[str]) -> list[str]:
        
        queryset = self.get_queryset()

        local_words: list[str] = [word_info.name for word_info in queryset]

        new2 = set(new_words) - set(local_words)

        local_new2 = set(local_words) - set(new_words)

        for word in local_new2:
            record: TranslateWordDataModel = queryset.get(name=word)
            
            # write table
            self.write_word_table(record.dict_info)

        return list[new2]


    @abstractmethod
    def request_handle(self) -> dict:
        ...

    def get_provider_info(self,new2: list[str]):
        for word in new2:
            dict_info: dict = self.request_handle(word)
            # write local dict info
            TranslateWordDataModel.objects.create(**{"name":word,"dict_info":dict_info})
            # write word table
            self.write_word_table(dict_info)
        
        
    def get_resource(self,words: list[str]):
        new = self.get_unknown_words(words)
        new2 = self.get_not_local_dict_info(new)

        self.get_provider_info(new)


class YoudaoProviderHandle(TranslateHandle):

    def get_mp3_url(self, dict_info: dict) -> dict:
        if dict_info["errorCode"] != '0':
            return "error"

        zhMp3Url = dict_info["tSpeakUrl"]
        enMp3Url = dict_info['speakUrl']

        return {"en":zhMp3Url,"zh":enMp3Url}


    def request_handle(self,word) -> dict:
        def _encrypt(signStr):
            hash_algorithm = hashlib.sha256()
            hash_algorithm.update(signStr.encode('utf-8'))    
            return hash_algorithm.hexdigest()
    
        def _truncate(q):
            if q is None:
                return None
            size = len(q)
            return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
        
        
        
        # request data
        curtime = str(int(time.time()))
        salt = str(uuid.uuid1())
        signStr = settings.APP_KEY + _truncate(word) + salt + curtime + settings.APP_SECRET

        data = {
            "from" : "en",
            "to" :"zh-CHS",
            "signType":"v3",
            "curtime": curtime,
            "sign":_encrypt(signStr),
            "appKey":settings.APP_KEY,
            "salt":salt,
            "q":word
            # 'vocabId':"您的用户词表ID"
        }

        # send
        response = requests.post(settings.YOUDAO_URL, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        text = response.content.decode("utf-8")
        return json.loads(text)





# demo
# YoudaoProviderHandle().get_resource()