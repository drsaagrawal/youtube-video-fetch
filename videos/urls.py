from django.conf.urls import url

from .views import get_youtube_videos

urlpatterns = [
    url(r'^get_employers/$', get_youtube_videos),
]