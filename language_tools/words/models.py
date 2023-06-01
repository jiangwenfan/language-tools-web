from django.db import models


class TranslateWordDataModel(models.Model):
    name = models.CharField(max_length=200,help_text="word name",verbose_name="word name")
    dict_info = models.JSONField(help_text="dict info",verbose_name="dict info")

    
    class Meta:
        db_table = "words_translate_word_data"

class TranslateProviderModel(models.Model):
    name_en = models.CharField(unique=True,max_length=200,help_text="en name",verbose_name="en name")
    name = models.CharField(max_length=200,help_text="zh name",verbose_name="zh name")
    words = models.ManyToManyField(TranslateWordDataModel)

    class Meta:
        db_table = "words_translate_provider"