from django.urls import path

from dance_dance.challenges import views

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list_view"),
    path("<int:video_id>/", views.VideoDetailView.as_view(), name="video_list_view"),
    path("<int:video_id>/like/", views.VideoLikeView.as_view(), name="video_like_view"),
    path("upload/<int:type>/", views.VideoLoadView.as_view(), name="video_load_view"),
]
