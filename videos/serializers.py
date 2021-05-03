from rest_framework import serializers

from .models import YoutubeVideos


class YoutubeVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideos
