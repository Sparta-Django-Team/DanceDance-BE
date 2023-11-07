from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from challenges.models import UserVideo
from challenges.serializers import UserVideoSerializer


# Create your views here.
class VideoListView(APIView):
    def get(self, request):
        user_videos = UserVideo.objects.all()
        serializer = UserVideoSerializer(user_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoDetailView(APIView):
    def get(self, request, video_id):
        video = get_object_or_404(UserVideo, id=video_id)
        serializer = UserVideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoLikeView(APIView):
    def get(self, request):
        pass
