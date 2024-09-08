from django.db import models

# Create your models here.
# choices 
FILE_TYPE_CHOICES = [
('text', 'Text'),
('audio', 'Audio'),
('video', 'Video'),
('image', 'Image'),
]

class MediaFile(models.Model):
    """
    Ge
    """
    file = models.FileField(upload_to='uploads/%Y/%m/%d')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type.capitalize()} File: {self.file.name}"

class TextToAudio(models.Model):
    """"""
    text = models.TextField()
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Text to Adio Conversion: {self.text[:50]}..."
    

class AudioToText(models.Model):
    """
    Stores details for the audio to text conversion.
    """
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE) # Uploaded audio file
    transcription = models.TextField() # Transcribed text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio to Text Transcription (from {self.audio_file.file.name})"

class VideoToAudio(models.Model):
    """
    Stores details for the video to audio extraction.
    """
    video_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name="video_file") # Uploaded video file
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name="extracted_audio_file") # Extracted audio file
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video to Audio Conversion (from {self.video_file.file.name})"

class AudioToVideo(models.Model):
    """
    Stores details for the audio to video conversion (audio with a static image).
    """
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name="audio_to_video_audio_file") # Uploaded audio file
    image_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name="audio_to_video_image_file") # Uploaded image file
    video_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name="generated_video_file") # Generated video file
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio to Video Conversion (from {self.audio_file.file.name} and {self.image_file.file.name})"


