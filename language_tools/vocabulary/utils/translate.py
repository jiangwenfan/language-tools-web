import hashlib
import json
import logging
import os
import time
import uuid
from abc import ABCMeta, abstractmethod

import requests
from django.conf import settings
from django.db.models import QuerySet
from ielts.models import TagModel, WordModel

from ..models import ProviderModel, WordInfoModel


class TranslateHandle(metaclass=ABCMeta):

    def __init__(self) -> None:
        # create youdao mp3 file
        provider_name_en: str = settings.TRANSLATE_PROVIDER
        media_root: str = settings.MEDIA_ROOT
        self.provider_path = os.path.join(media_root,provider_name_en)
        if not os.path.exists(self.provider_path):
            os.mkdir(self.provider_path)

        self.provider_name_en: str = settings.TRANSLATE_PROVIDER
        self.provider_obj: ProviderModel = ProviderModel.objects.get(name_en=provider_name_en)

    def get_not_exist_words(self,words) -> list[str]:
        """获取不存在的"""
        exist_words: list[str] = [word_obj.name for word_obj in WordModel.objects.all()]

        new_words: set = set(words) - set(exist_words)

        return list(new_words)
    
    def get_queryset(self) -> QuerySet:
        #获取settings中启用的provider
        # provider_name_en: str = settings.TRANSLATE_PROVIDER
        local_words_info :QuerySet =ProviderModel.objects.get(name_en=self.provider_name_en).words_info.all()
        return local_words_info
    
    def get_mp3_file_name(self,file_id_name: str) -> str:
        #获取settings中启用的provider
        from .utils import generate_random_num

        # file_name: str = generate_random_num()+"_"+suffix+".mp3"
        file_name: str = file_id_name +".mp3"
        return os.path.join(self.provider_path,file_name)
        
    @abstractmethod
    def get_mp3_url(self,dict_info:dict) -> dict:
        """get mp3 url from word dict info
        dict_info = {
            "en":"",
            "zh":"",
        }
        """
        ...

    @abstractmethod
    def get_tag_type(self,dict_info:dict) -> list:
        """get word tag from dict info

        Args:
            dict_info (dict): _description_

        Returns:
            dict: _description_
        """
        ...

    @abstractmethod
    def real_write_word_table(self,dict_info: dict) -> WordModel:
        """write word table from every provider dict info"""
        ...

    def write_word_table_download_file(self,dict_info: dict):
        """download mp3 file and write table"""
        

        # write
        instance = self.real_write_word_table(dict_info)


        # download
        url_info: dict = self.get_mp3_url(dict_info)

        file_id_zh: str = str(uuid.uuid4())
        file_name_zh = self.get_mp3_file_name(file_id_zh)
        url_zh = url_info["zh"]

        file_id_en: str = str(uuid.uuid4())
        file_name_en = self.get_mp3_file_name(file_id_en)
        url_en = url_info["en"]

        self.download_mp3_file(url_zh,file_id=file_name_zh)
        self.download_mp3_file(url_en,file_id=file_name_en)

        mp3_data: dict = {
            "en_file_uuid":file_id_en,
            "zh_file_uuid":file_id_zh,
            "mp3_files":instance,
        }
        from ielts.models import Mp3FileModel
        Mp3FileModel.objects.create(**mp3_data)

        # create tag
        all_tags_exist: list = [tag_obj.name for tag_obj in TagModel.objects.all()]
        new_tags: list = self.get_tag_type(dict_info=dict_info)

        # TagModel.objects.bulk_create()
        for new_word in new_tags:
            if new_word not in all_tags_exist:
                tag = TagModel.objects.create(name=new_word)
            else:
                tag = TagModel.objects.get(name=new_word)
            tag.words.add(instance)

    def download_mp3_file(self,url: str,file_id: str):
        response = requests.get(url=url)
        with open(file_id,"wb") as f:
            f.write(response.content)

    def get_not_local_cache_words(self,new_words: list[str]) -> list[str]:
        """非本地缓存中的"""
        queryset = self.get_queryset()

        """
        >>> request=[1,2,3,4]
        >>> data=[2,3,5]
        >>> set(request)-set(data)
        {1, 4}
 
        """
        local_words: list[str] = [word_info.name for word_info in queryset]
        logging.warning(f"缓存中的所有: {local_words}")

        new2 = set(new_words) - set(local_words)
        logging.warning(f"需要新添加的: {new2}")



        """
        >>> request=[1,2,3,4]
        >>> data=[2,3,5]
        >>> set(request).intersection(set(data))
        {2, 3}
        >>> set(data).intersection(set(request))
        {2, 3}
        """

        local_new2 = set(local_words).intersection(set(new_words))
        logging.warning(f"存在cache中的: {local_new2}")
        for word in local_new2:
            record: WordInfoModel = queryset.get(name=word)
            
            # write table
            self.write_word_table_download_file(record.dict_info)

        return list(new2)


    @abstractmethod
    def request_handle(self,word: str) -> dict:
        """get word dict info from remote server"""
        ...

    def add_new_words(self,add_words: list[str]):
        for add_word in add_words:
            dict_info: dict = self.request_handle(add_word)
            # write local dict info
            instance: WordInfoModel= WordInfoModel.objects.create(**{"name":add_word,"dict_info":dict_info})
            # provider
            instance.translateprovidermodel_set.add(self.provider_obj)

            # write word table
            self.write_word_table_download_file(dict_info)
        
        
    def get_resource(self,input_words: list[str]):
        not_exist_words: list[str] = self.get_not_exist_words(input_words)
        add_words: list[str] = self.get_not_local_cache_words(not_exist_words)

        self.add_new_words(add_words)




class YoudaoProviderHandle(TranslateHandle):
    """使用: YoudaoProviderHandle().get_resource(input_words=["attribute"])

    Args:
        TranslateHandle (_type_): _description_
    """
    def get_mp3_url(self, dict_info: dict) -> dict:
        logging.warning(f"获取mm: {dict_info}")
        if dict_info["errorCode"] != '0':
            return "error"

        zhMp3Url = dict_info["tSpeakUrl"]
        enMp3Url = dict_info['speakUrl']

        res = {"zh":zhMp3Url,"en":enMp3Url}
        logging.warning(f"mp3 url: {res}")
        return res


    def request_handle(self,word: str) -> dict:
        logging.warning(f"请求: {word}")
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


    def real_write_word_table(self, dict_info: dict) -> WordModel:
        import logging
        logging.error(f"真: {dict_info} {type(dict_info)}")
        basic = dict_info["basic"]
        word_data: dict = {
            "name":dict_info["query"],
            "zh":basic["explains"],
            "symbol":basic["phonetic"],
            "grammar_info":basic["wfs"]
        }
        instance = WordModel.objects.create(**word_data)
        return instance

    def get_tag_type(self, dict_info: dict) -> list:
        basic: list = dict_info["basic"]["exam_type"]
        return basic


# demo
# YoudaoProviderHandle().get_resource(input_words=["paper"])