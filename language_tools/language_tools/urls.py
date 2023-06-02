
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('words/',include('vocabulary.urls')),
    path('ielts/',include('ielts.urls')),
     
]
