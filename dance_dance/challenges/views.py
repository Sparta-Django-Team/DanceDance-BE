import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from dance_dance.challenges.functions import download_video
from dance_dance.challenges.models import UserVideo
from dance_dance.challenges.serializers import (
    OriginalVideoSerializer,
    TagCreateSerializer,
    UserVideoSerializer,
)
from dance_dance.common.pagination import PaginationHandlerMixin
from dance_dance.common.response import create_response


class VideoListPagination(PageNumberPagination):
    page_size = 1


class VideoListView(PaginationHandlerMixin, APIView):
    permission_classes = [AllowAny]
    pagination_class = VideoListPagination

    @swagger_auto_schema(
        tags=["User Video List"],
        operation_summary="유저 영상 리스트 조회",
        responses={
            status.HTTP_200_OK: UserVideoSerializer,
        },
    )
    def get(self, request):
        user_videos = UserVideo.objects.all()
        logger.info(user_videos)
        page = self.paginate_queryset(user_videos)
        serializer = self.get_paginated_response(UserVideoSerializer(page, many=True).data)
        return create_response(serializer.data, status_code=status.HTTP_200_OK)


class VideoDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["User Video Detail"],
        operation_summary="유저 영상 상세페이지 조회",
        responses={
            status.HTTP_200_OK: UserVideoSerializer,
        },
    )
    def get(self, request, video_id):
        video = get_object_or_404(UserVideo, id=video_id)
        serializer = UserVideoSerializer(video)
        return create_response(serializer.data, status_code=status.HTTP_200_OK)


class VideoLikeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["User Video Like"],
        operation_summary="유저 영상 좋아요",
    )
    def post(self, request, video_id):
        # if        # User or Original 구분
        video = get_object_or_404(UserVideo, id=video_id)
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            return create_response("unlike", status_code=status.HTTP_200_OK)
        else:
            video.likes.add(request.user)
            return create_response("like", status_code=status.HTTP_200_OK)


class VideoLoadView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Video Processing"],
        operation_summary="비디오 로드 및 Score 추출",
    )
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
            return create_response(serializer.data, status_code=status.HTTP_201_CREATED)
        return create_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class TagCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Tag Create"],
        operation_summary="태그 생성",
    )
    def post(self, request):
        serializer = TagCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(serializer.data, status_code=status.HTTP_200_OK)
        else:
            return create_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
