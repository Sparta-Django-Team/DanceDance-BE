from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from challenges.models import UserVideo
from challenges.serializers import UserVideoListSerializer


# Create your views here.
class VideoView(APIView):
    def get(self, request):
        user_videos = UserVideo.objects.all()
        serializer = UserVideoListSerializer(user_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
