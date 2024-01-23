from django.urls import path

from dance_dance.challenges import views

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list_view"),
    path("<int:video_id>", views.VideoDetailView.as_view(), name="video_list_view"),
    path("<int:video_id>/likes", views.VideoLikeView.as_view(), name="video_like_view"),
    path("tags", views.TagCreateView.as_view(), name="tag_create_view"),
    path("upload/origin", views.VideoLoadOriginView.as_view(), name="video_load_origin_view"),
    path("upload/user", views.VideoLoadUserView.as_view(), name="video_load_user_view"),
]
