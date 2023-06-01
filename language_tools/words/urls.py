from django.urls import path

from .views import index, words2mp3

urlpatterns = [
    path('',index), # show index
    path('words2mp3/',words2mp3), # words to mp3 
]