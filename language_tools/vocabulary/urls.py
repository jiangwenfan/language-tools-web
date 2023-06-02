from django.urls import path

from .views import (
    get_words_from_html,
    get_words_from_pdf,
    get_words_from_subtitle,
    index,
    pull_words,
    words2mp3,
)

urlpatterns = [
    path('',index), # show index
    path('pull-words/',pull_words), #generate word data to local from youdao
    path('words2mp3/',words2mp3), # words to mp3 
    path('getwords-pdf/',get_words_from_pdf), # paper
    path('getwords-html/',get_words_from_html), # document
    path('getwords-subtitle/',get_words_from_subtitle), # movie
]