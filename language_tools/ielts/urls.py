from django.urls import path, re_path

from .views import corpus_listen_check, get_chapters, get_papers, index

urlpatterns = [
    path("",index),
    path("corpus_listen_check/",corpus_listen_check),
    re_path("chapters/(?P<book_id>\d+)/",get_chapters),
    re_path("papers/(?P<chapter_id>\d+)/",get_papers),
]