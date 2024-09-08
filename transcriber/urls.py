from django.urls import path
from . import views

urlpatterns = [
    # home urls
    path('', views.homepage, name="homepage"),
    # 
    path('text-to-audio/', views.text_to_audio, name='text_to_audio'),
    path('audio-to-text/', views.audio_to_text, name='audio_to_text'),
    path('video-to-audio/', views.video_to_audio, name='video_to_audio'),
    path('audio-to-video/', views.audio_to_video, name='audio_to_video'),
]
