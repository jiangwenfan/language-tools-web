from django.db import models
from django.utils import timezone


class BookModel(models.Model):
    name = models.CharField(verbose_name="book name", max_length=200,help_text="book name")
    cover = models.CharField(verbose_name="cover name", max_length=500,blank=True,null=True)
    description = models.CharField(verbose_name="", max_length=500)
    created_time = models.DateTimeField(auto_now_add=True,help_text="create time",verbose_name="create time")
    updated_time = models.DateField(auto_now=True,help_text="update time",verbose_name="update time")
    class Meta:
        db_table = "ielts_book"

    def __str__(self) -> str:
        return self.name
    

class ChapterModel(models.Model):
    name = models.CharField(max_length=200)
    book_id = models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name="chapters")
    created_time = models.DateTimeField(auto_now_add=True,help_text="create time",verbose_name="create time")
    updated_time = models.DateField(auto_now=True,help_text="update time",verbose_name="update time")
    class Meta:
        db_table = "ielts_chapter"
    def __str__(self) -> str:
        return self.name


class PaperModel(models.Model):
    name = models.CharField(verbose_name="paper name", max_length=200)  # xxx
    chapter = models.ForeignKey(ChapterModel,on_delete=models.CASCADE,related_name="papers")
    words = models.ManyToManyField('WordModel')
    created_time = models.DateTimeField(auto_now_add=True,help_text="create time",verbose_name="create time")
    updated_time = models.DateField(auto_now=True,help_text="update time",verbose_name="update time")
    class Meta:
        db_table = "ielts_paper"
    
    def __str__(self) -> str:
        return self.name
class WordModel(models.Model):
    name = models.CharField(max_length=200,help_text="word en",verbose_name="word en", )
    zh = models.CharField(null=True,blank=True,max_length=200,help_text="word zh",verbose_name="word zh")
    symbol = models.CharField(null=True,blank=True,max_length=200,help_text="word pronounce symbol",verbose_name="word pronounce symbol")
    grammar_info = models.JSONField(verbose_name="grammar info",help_text="grammar info")
    created_time = models.DateTimeField(auto_now_add=True,help_text="create time",verbose_name="create time")
    updated_time = models.DateField(auto_now=True,help_text="update time",verbose_name="update time")
    
    class Meta:
        db_table = "ielts_word"
        
    def __str__(self) -> str:
        return self.name
class Mp3FileModel(models.Model):
    en_file_uuid = models.UUIDField(null=True,blank=True,editable=False,help_text="word en mp3 short url",verbose_name="")
    zh_file_uuid = models.UUIDField(null=True,blank=True,editable=False,help_text="word zh mp3 short url",verbose_name="")
    mp3_files = models.ForeignKey(WordModel,on_delete=models.CASCADE)
    class Meta:
        db_table = "ielts_word_mp3"

    def __str__(self) -> str:
        return self.name
class TagModel(models.Model):
    name = models.CharField(unique=True,max_length=200,verbose_name="标签",help_text="标签")
    words = models.ManyToManyField(WordModel)

    class Meta:
        db_table = "ielts_word_tag"

    def __str__(self) -> str:
        return self.name
# class ResultModel(Base):
#     rtype = models.CharField(max_length=10)  # 1.听音拼写 2.听音辨义
#     bid = models.ForeignKey(BookModel, on_delete=models.CASCADE)
#     uid = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     pid = models.ForeignKey(PaperModel,on_delete=models.CASCADE)
#     accuracy = models.CharField(max_length=100, verbose_name="正")
#     error_words = models.JSONField()
#     """
#     [a,b,c]
#     """
