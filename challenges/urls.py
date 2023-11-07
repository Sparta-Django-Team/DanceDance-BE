from django.urls import path

from challenges import views

urlpatterns = [
    path("", views.VideoView.as_view(), name="video_view"),
]
