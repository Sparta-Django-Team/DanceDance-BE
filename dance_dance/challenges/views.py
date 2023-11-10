import json

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from dance_dance.challenges.functions import download_video
from dance_dance.challenges.models import UserVideo
from dance_dance.challenges.serializers import (
    OriginalVideoSerializer,
    TagCreateSerializer,
    UserVideoSerializer,
)


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
    def post(self, request, video_id):
        video = get_object_or_404(UserVideo, id=video_id)
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            video.likes.add(request.user)
            return Response("좋아요 했습니다.", status=status.HTTP_200_OK)


class VideoLoadView(APIView):
    def post(self, request, file_type):  # file_type은 origin or user만 사용하도록 선택하게끔 한다
        if request.method == "POST":
            data = json.loads(request.body)
            video_url = data["video_url"]
        results = download_video(video_url, file_type)

        if file_type == "origin":
            serializer = OriginalVideoSerializer(data=results)
        elif file_type == "user":
            serializer = UserVideoSerializer(data=results)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagCreateView(APIView):
    def post(self, request):
        serializer = TagCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
