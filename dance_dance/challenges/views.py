import glob

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from dance_dance.challenges.models import UserVideo
from dance_dance.challenges.serializers import UserVideoSerializer

from dance_dance.challenges.functions import createFolder, download_video

import json

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
    def post(self, request, type):
        if request.method == 'POST':
            data = json.loads(request.body)
            video_url = data['video_url']
        print(video_url)
        if type == 1:
            file_type = "new"
        elif type == 0:
            file_type = "origin"

        download_results = download_video(video_url)
        chl_name = download_results["challenge_name"].replace(" ", "")
        lm_path = f"/temp/landmarks/{file_type}"
        createFolder("./temp/landmarks/")
        end_str = f"{chl_name}.mp4"
        for f in glob.glob(f"temp/landmarks/{file_type}/*{end_str}.csv"):
            print("확인")
            print(f)

        print("챌린지 이름: " + chl_name)  # 챌린지 이름
        print("Landmark 경로: " + lm_path)  # landmark 경로


        video_route = download_results["video_route"]
        contents = [video_route, file_type]
        return Response(download_results, status=status.HTTP_200_OK)
