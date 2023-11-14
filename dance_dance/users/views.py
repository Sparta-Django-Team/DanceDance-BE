from django.shortcuts import redirect
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from dance_dance.common.exception.exceptions import AuthenticationFailedException
from dance_dance.common.response import create_response
from dance_dance.users.kakao_oauth import KakaoLoginFlowService
from dance_dance.users.models import User
from dance_dance.users.serializers import (
    KakaoInputSerializer,
    KakaoOutputSerializer,
    SignupSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="회원가입",
        request_body=SignupSerializer,
        responses={
            status.HTTP_201_CREATED: UserDetailSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return create_response(data=UserDetailSerializer(user).data, status_code=status.HTTP_201_CREATED)


class KakaoLoginRedirectAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인 리다이렉트",
    )
    def get(self, request: Request) -> redirect:
        kaka_login_flow = KakaoLoginFlowService()
        authorization_url = kaka_login_flow.get_authorization_url()
        return redirect(authorization_url)


class KakaoLoginAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인 콜백",
        query_serializer=KakaoInputSerializer,
        responses={
            status.HTTP_200_OK: KakaoOutputSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        input_serializer = KakaoInputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")

        if error is not None:
            raise AuthenticationFailedException(error)

        if code is None:
            raise AuthenticationFailedException("Code is not provided")

        # Kakao Login Flow
        kakao_login_flow = KakaoLoginFlowService()
        kakao_token = kakao_login_flow.get_token(code=code)
        user_info = kakao_login_flow.get_user_info(kakao_token=kakao_token)

        # Create Social User
        user = User.objects.filter(social_id=user_info["id"])
        if not user.exists():
            user = User.objects.create_social_user(
                social_id=user_info["id"],
                nickname=user_info["kakao_account"]["profile"]["nickname"],
                email=user_info["kakao_account"]["email"],
                thumbnail_image_url=user_info["kakao_account"]["profile"]["thumbnail_image_url"],
            )

        # Response Access Token & Refresh Token
        refresh = RefreshToken.for_user(user.get())
        output_serializer = KakaoOutputSerializer(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        )
        return create_response(data=output_serializer.data, status_code=status.HTTP_200_OK)


class JWTTokenView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="JWT 토큰 발급",
        request_body=TokenObtainPairSerializer,
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return create_response(data=serializer.validated_data, status_code=status.HTTP_200_OK)


class JWTTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=["인증"], operation_summary="JWT 리프레쉬 토큰 발급", request_body=TokenRefreshSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return create_response(data=serializer.validated_data, status_code=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 조회",
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserDetailSerializer(user)
        return create_response(data=serializer.data, status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 탈퇴",
    )
    def delete(self, request: Request) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.save()
        return create_response(status_code=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 수정",
        request_body=UserUpdateSerializer,
        responses={status.HTTP_200_OK: UserUpdateSerializer},
    )
    def put(self, request: Request) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_response(data=serializer.data, status_code=status.HTTP_200_OK)
