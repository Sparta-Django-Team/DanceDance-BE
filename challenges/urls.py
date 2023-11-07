from django.urls import path

from challenges import views

urlpatterns = [
    path("", views.VideoListView.as_view(), name="video_list_view"),
    path("<int:video_id>/", views.VideoDetailView.as_view(), name="video_list_view"),
    path("<int:video_id>/like/", views.VideoLikeView.as_view(), name="video_like_view"),
]
