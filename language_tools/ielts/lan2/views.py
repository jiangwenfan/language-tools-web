from rest_framework.viewsets import ModelViewSet
from language.serializers import (
    BookSerializer,
    PaperSerializer,
    WordSerializer,
    ResultSerializer,
    UserSerializer
)
from language.models import BookModel, PaperModel, WordModel, ResultModel, UserModel
from django_filters.rest_framework import DjangoFilterBackend
from language.filters import BookFilter, PaperFilter, WordFilter,ResultFilter


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.filter(is_delete=False)


class BookView(ModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.filter(is_delete=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class PaperView(ModelViewSet):
    serializer_class = PaperSerializer
    queryset = PaperModel.objects.filter(is_delete=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaperFilter

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class WordView(ModelViewSet):
    serializer_class = WordSerializer
    queryset = WordModel.objects.filter(is_delete=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = WordFilter

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class ResultView(ModelViewSet):
    serializer_class = ResultSerializer
    queryset = ResultModel.objects.filter(is_delete=False)
    filter_backends = [DjangoFilterBackend]
    filtset_class = ResultFilter

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
