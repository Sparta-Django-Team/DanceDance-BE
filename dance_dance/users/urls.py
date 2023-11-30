from django.urls import path

from dance_dance.users.views import (
    FollowerListView,
    FollowingListView,
    FollowView,
    JWTTokenRefreshView,
    JWTTokenView,
    KakaoLoginAPI,
    KakaoLoginRedirectAPI,
    SignUpView,
    UserDetailView,
)

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("kakao/redirect", KakaoLoginRedirectAPI.as_view(), name="kakao-login-redirect"),
    path("kakao/callback", KakaoLoginAPI.as_view(), name="kakao-login-callback"),
    path("jwt", JWTTokenView.as_view(), name="jwt"),
    path("jwt/refresh", JWTTokenRefreshView.as_view(), name="jwt-refresh"),
    path("detail", UserDetailView.as_view(), name="user-detail"),
    path("follower/<int:followed_id>", FollowView.as_view(), name="follow_view"),
    path("followings/<int:following_id>", FollowingListView.as_view(), name="following_list_view"),
    path("followers/<int:follower_id>", FollowerListView.as_view(), name="follower_list_view"),
]
