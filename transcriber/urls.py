from django.urls import path
from . import views

urlpatterns = [
    # home urls
    path('', views.homepage, name="homepage"),
    path('text-to-audio/', views.text_to_audio, name='text-to-audio'),
    path('audio-to-text/', views.audio_to_text, name='audio-to-text'),
    path('audio-to-video/', views.audio_to_video, name='audio-to-video'),
    path('video-to-audio/', views.video_to_audio, name='video-to-audio'),
]
