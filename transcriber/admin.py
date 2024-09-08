from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TextToAudio)
admin.site.register(AudioToText)
admin.site.register(VideoToAudio)
admin.site.register(AudioToVideo)