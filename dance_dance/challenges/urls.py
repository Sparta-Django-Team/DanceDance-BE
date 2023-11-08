from django.urls import path

from dance_dance.challenges import views

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list_view"),
    path("<int:video_id>/", views.VideoDetailView.as_view(), name="video_list_view"),
    path("<int:video_id>/like/", views.VideoLikeView.as_view(), name="video_like_view"),
    path("tag/", views.TagCreateView.as_view(), name="tag_create_view"),
    path("upload/<str:file_type>/", views.VideoLoadView.as_view(), name="video_load_view"),
]
