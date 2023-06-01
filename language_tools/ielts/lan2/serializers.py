from rest_framework.serializers import ModelSerializer
from language.models import BookModel, PaperModel, WordModel, ResultModel, UserModel


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'phone', 'password', 'created_time')
        extra_kwargs = {"created_time": {"read_only": True}}


class BookSerializer(ModelSerializer):
    class Meta:
        model = BookModel
        fields = ("name", "description", "cover", "created_time")
        extra_kwargs = {"created_time": {"read_only": True}}


class PaperSerializer(ModelSerializer):
    class Meta:
        model = PaperModel
        fields = ("bid", "name", "chapter", "created_time")
        extra_kwargs = {"created_time": {"read_only": True}}


class WordSerializer(ModelSerializer):
    class Meta:
        model = WordModel
        fields = ("pid","name", "zh", "symbol", "mp3", "created_time")
        extra_kwargs = {"created_time": {"read_only": True}}


class ResultSerializer(ModelSerializer):
    class Meta:
        model = ResultModel
        fields = ("name", "accuracy", "error_words", "created_time")
        extra_kwargs = {"created_time": {"read_only": True}}
