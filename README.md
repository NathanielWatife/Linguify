# Linguify
    Linguify Media Transcriber app is a Django-based web application that allows users to:

    - Convert Text to Audio: Users can input text, which is converted to an audio file.
    - Convert Audio to Text: Users can upload an audio file, and the app will transcribe it into text.
    - Extract Audio from Video: Users can upload a video file, and the app will extract and generate an audio file from it.
    - Convert Audio and Image to Video: Users can upload an audio file and an image, and the app will generate a video using the image as the background and the audio as the soundtrack.
    - The app provides an interface to download the resulting audio and video files, allowing users to view or play the generated content.


System Requirements
Python (version 3.8+)
Django (version 3.2+)
MoviePy (for video and audio processing)
gTTS (Google Text-to-Speech for converting text to audio)
SpeechRecognition (for audio-to-text transcription)
FFmpeg (required by MoviePy for video and audio conversion)
pydub (for audio file conversions if necessary)
Installation
Clone the Repository:

bash
Copy code
```
git clone <https://github.com/NathanielWatife/Linguify.git>
cd <Linguify>
```
Set Up a Virtual Environment:

bash
Copy code
```
python -m venv env
source env/bin/activate  # On Windows, use: env\Scripts\activate
```

Install Dependencies:

bash
Copy code
```
pip install -r requirements.txt
```
Install FFmpeg:
```
Linux: sudo apt-get install ffmpeg
macOS: brew install ffmpeg
Windows: Download ffmpeg and add it to your system's PATH.
```
Run Migrations:

bash
Copy code
```
python manage.py migrate
```
Run the Server:

bash
Copy code
```
python manage.py runserver
Access the Application: Open your browser and go to: http://127.0.0.1:8000/transcriber/
```

## App Structure
    - Directory Structure
plaintext
Copy code
├── CoreRoot/
│   ├── __init__.py
│   ├── settings.py        # Django settings for the project
│   ├── urls.py            # Main URL routing for the app
│   ├── wsgi.py
│
├── transcriber/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py           # Forms for handling user inputs
│   ├── models.py          # Models for storing media files and transcriptions
│   ├── urls.py            # URL routing for the transcriber app
│   ├── views.py           # Views for processing requests and rendering responses
│   ├── templates/
│       ├── transcriber/
│           ├── text_to_audio.html
│           ├── audio_to_text.html
│           ├── video_to_audio.html
│           ├── audio_to_video.html
├── media/                 # Stores all media files (audio, video, image)
├── db.sqlite3             # SQLite database (created after migrations)
├── manage.py
Models
MediaFile: Stores uploaded media files (audio, video, text, or images).

python
Copy code
```
class MediaFile(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```
TextToAudio: Stores the relationship between text and the generated audio file.

python
Copy code
```
class TextToAudio(models.Model):
    text = models.TextField()
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
```
AudioToText: Stores the transcription generated from an audio file.

python
Copy code
```
class AudioToText(models.Model):
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
    transcription = models.TextField()
```
VideoToAudio: Stores the video and the extracted audio file.

python
Copy code
```
class VideoToAudio(models.Model):
    video_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name='video_file')
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name='audio_file')
```
AudioToVideo: Stores the relationship between an audio file, an image, and the generated video file.

python
Copy code
```
class AudioToVideo(models.Model):
    audio_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
    image_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
    video_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE)
```
Forms
TextToAudioForm: Form to handle text input for generating audio.
AudioToTextForm: Form to handle file uploads for audio-to-text transcription.
VideoToAudioForm: Form to handle video file uploads for extracting audio.
AudioToVideoForm: Form to handle audio and image uploads for generating video.
Views
Text to Audio:

Converts input text to an audio file (MP3 format) using the gTTS library.
Displays the generated audio file and provides a download link.
python
Copy code
```
def text_to_audio(request):
    # Handles text-to-audio conversion using gTTS
```
Audio to Text:

Accepts an audio file, transcribes it to text using the SpeechRecognition library, and displays the transcription.
python
Copy code
```
def audio_to_text(request):
    # Handles audio-to-text conversion using SpeechRecognition
```
Video to Audio:

Extracts audio from an uploaded video file using MoviePy and saves the extracted audio.
python
Copy code
```
def video_to_audio(request):
    # Handles video-to-audio conversion using MoviePy
```
Audio to Video:

Combines an audio file and an image to generate a video using MoviePy.
The image is used as the background, and the audio is added as the soundtrack.
python
Copy code
```
def audio_to_video(request):
    # Handles audio-to-video conversion using MoviePy
```
Templates
text_to_audio.html: Renders a form for text input, converts the text to audio, and displays the output.
audio_to_text.html: Uploads an audio file and shows the transcribed text.
video_to_audio.html: Allows users to upload a video file and extract audio from it.
audio_to_video.html: Uploads an audio file and an image, generates a video, and displays the result.
Usage
Convert Text to Audio:

Navigate to /transcriber/text-to-audio/.
Enter text in the input box and click "Convert".
The generated audio file (MP3) will be displayed with a playback control and download link.
Convert Audio to Text:

Navigate to /transcriber/audio-to-text/.
Upload an audio file (e.g., MP3 or WAV) and click "Transcribe".
The transcribed text will be displayed on the same page.
Extract Audio from Video:

Navigate to /transcriber/video-to-audio/.
Upload a video file (e.g., MP4 or AVI) and click "Extract".
The extracted audio (MP3) will be available for playback and download.
Generate Video from Audio and Image:

Navigate to /transcriber/audio-to-video/.
Upload an audio file and an image, and click "Generate Video".
The generated video will be available for playback and download.
Notes
File Storage: All media files (audio, video, images) are saved in the media/ directory. Make sure that this directory is writable by the application.
Media Serving: Ensure that MEDIA_URL and MEDIA_ROOT are correctly configured in settings.py for proper media file serving during development.
Troubleshooting
File Not Found Error: Ensure that the media/ directory exists and is writable. You can create the directory manually or use Django's FileSystemStorage to handle file saving automatically.

Transcription Errors: If the transcription fails, ensure that the uploaded audio file is in a format supported by the SpeechRecognition library (e.g., WAV, FLAC).

Audio/Video Processing Issues: Ensure that ffmpeg is installed and correctly configured, as it is required by MoviePy for handling audio and video files.

