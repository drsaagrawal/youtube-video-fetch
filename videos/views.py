from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import YoutubeVideos
from .serializers import YoutubeVideosSerializer


@api_view(['GET'])
def get_youtube_videos(request):
    """
    Get youtube videos details
    """
    limit = request.GET.get('limit', 20)
    offset = request.GET.get('offset', 0)
    search = request.GET.get('search')
    q = Q()
    if search:
        q |= Q(title__icontains=search) | Q(description__icontains=search)
    objs = YoutubeVideos.objects.filter(q).sort_by('-published_at')[offset:offset+limit]
    serializer = YoutubeVideosSerializer(objs)
    return Response(serializer.data)
