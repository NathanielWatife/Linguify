from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TextToAudioForm, AudioToTextForm, VideoToAudioForm, AudioToVideoForm
from .models import MediaFile, TextToAudio, AudioToText, VideoToAudio, AudioToVideo
import os
from gtts import gTTS
import speech_recognition as sr
from moviepy.editor import *
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
import uuid


# homepage views
def homepage(request):
# Retrieve the outputs from different models
    text_to_audio_outputs = TextToAudio.objects.all()
    audio_to_text_outputs = AudioToText.objects.all()
    video_to_audio_outputs = VideoToAudio.objects.all()
    audio_to_video_outputs = AudioToVideo.objects.all()

    # Pass all outputs to the template
    context = {
        'text_to_audio_outputs': text_to_audio_outputs,
        'audio_to_text_outputs': audio_to_text_outputs,
        'video_to_audio_outputs': video_to_audio_outputs,
        'audio_to_video_outputs': audio_to_video_outputs,
    }
    
    return render(request, 'transcriber/home.html', context)




# Helper function to save media files
def save_generated_audio_file(audio_path, filename):
    fs = FileSystemStorage()
    with open(audio_path, 'rb')as audio_file:
        filename = fs.save(filename, audio_file) # Save the file using FileSystemStorage
        media_file = MediaFile(file=filename, file_type='audio')
        media_file.save()
    return media_file

# Text to Audio View
def text_to_audio(request):
    if request.method == 'POST':
        form = TextToAudioForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            # Convert text to speech using gTTS
            tts = gTTS(text)
            audio_filename = 'text_to_audio.mp3'
            fs = FileSystemStorage()

            # Create the file in memory and save it with FileSystemStorage
            audio_file_path = fs.path(audio_filename) # Get the full path in the media folder

            # Save the file to disk
            tts.save(audio_file_path)

            # save generated audio file using specific function
            media_file = save_generated_audio_file(audio_file_path, audio_filename)

            # Save the record in TextToAudio model
            text_audio_entry = TextToAudio(text=text, audio_file=media_file)
            text_audio_entry.save()

            # Return the response with the audio file
        return HttpResponse(f'<audio controls><source src="{fs.url(audio_filename)}" type="audio/mp3"></audio>')
    else:
        form = TextToAudioForm()
    return render(request, 'transcriber/text_to_audio.html', {'form': form})



# Audio to Text View
# Helper function to save audio files for audio-to-text conversion
def save_audio_file(uploaded_file):
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)  # Save the file using FileSystemStorage
    media_file = MediaFile(file=filename, file_type='audio')  # Specify 'audio' as the file type
    media_file.save()
    return media_file

# Convert the uploaded audio file to WAV format using pydub
def convert_to_wav(file_path):
    audio = AudioSegment.from_file(file_path)  # pydub will auto-detect the format
    wav_path = os.path.splitext(file_path)[0] + '.wav'
    audio.export(wav_path, format="wav")
    return wav_path

# Audio to Text View
def audio_to_text(request):
    if request.method == 'POST':
        form = AudioToTextForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded audio file
            audio_file = form.cleaned_data['file']
            media_file = save_audio_file(audio_file)

            # Convert the audio file to WAV format using pydub
            wav_audio_path = convert_to_wav(media_file.file.path)

            # Convert audio to text using SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_audio_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    text = "Could not transcribe the audio."

            # Save the record in the AudioToText model
            audio_text_entry = AudioToText(audio_file=media_file, transcription=text)
            audio_text_entry.save()

            return HttpResponse(f"<p>Transcribed Text: {text}</p>")
    else:
        form = AudioToTextForm()

    return render(request, 'transcriber/audio_to_text.html', {'form': form})





# Helper function to save extracted audio from video files
def save_extracted_audio_file(extracted_audio_path, filename):
    fs = FileSystemStorage()
    with open(extracted_audio_path, 'rb') as audio_file:
        filename = fs.save(filename, audio_file)  # Save the file using FileSystemStorage
        media_file = MediaFile(file=filename, file_type='audio')  # Specify 'audio' as the file type
        media_file.save()
    return media_file

# Video to Audio View
def video_to_audio(request):
    if request.method == 'POST':
        form = VideoToAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded video file
            video_file = form.cleaned_data['file']
            fs = FileSystemStorage()

            # Save the video file to the file system
            video_filename = fs.save(video_file.name, video_file)
            media_video_file = MediaFile(file=video_filename, file_type='video')
            media_video_file.save()  # Save the video file in the MediaFile model first

            try:
                # Extract audio from the video using MoviePy
                video_path = media_video_file.file.path
                video_clip = VideoFileClip(video_path)
                extracted_audio_path = fs.path('extracted_audio.mp3')
                video_clip.audio.write_audiofile(extracted_audio_path)

                # Save extracted audio file using the specific function
                media_audio_file = save_extracted_audio_file(extracted_audio_path, 'extracted_audio.mp3')

                # Now save the VideoToAudio record after both media files are saved
                video_audio_entry = VideoToAudio(video_file=media_video_file, audio_file=media_audio_file)
                video_audio_entry.save()

                return HttpResponse(f'<audio controls><source src="/media/extracted_audio.mp3" type="audio/mp3"></audio>')
            except Exception as e:
                print(f"Error extracting audio from video: {e}")
                return HttpResponse(f"An error occurred: {e}")
    else:
        form = VideoToAudioForm()

    return render(request, 'transcriber/video_to_audio.html', {'form': form})





# Helper function to save generated video files for audio-to-video conversion
def save_generated_video_file(video_path, filename):
    fs = FileSystemStorage()
    with open(video_path, 'rb') as video_file:
        filename = fs.save(filename, video_file)  # Save the file using FileSystemStorage
        media_file = MediaFile(file=filename, file_type='video')  # Specify 'video' as the file type
        media_file.save()
    return media_file

# Audio to Video View
def audio_to_video(request):
    if request.method == 'POST':
        form = AudioToVideoForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded audio and image files
            audio_file = form.cleaned_data['audio_file']
            image_file = form.cleaned_data['image_file']
            fs = FileSystemStorage()
            audio_filename = fs.save(audio_file.name, audio_file)
            image_filename = fs.save(image_file.name, image_file)

            media_audio_file = MediaFile(file=audio_filename, file_type='audio')
            media_image_file = MediaFile(file=image_filename, file_type='image')

            media_audio_file.save()
            media_image_file.save()

            try:
                # Generate video from audio and image using moviepy
                audio_clip = AudioFileClip(media_audio_file.file.path)
                image_clip = ImageClip(media_image_file.file.path).set_duration(audio_clip.duration).set_audio(audio_clip)

                # Generate a unique filename for the video
                video_filename = f"audio_to_video_{uuid.uuid4().hex}.mp4"
                video_path = fs.path(video_filename)

                # Write the video file to disk
                image_clip.write_videofile(video_path, fps=24)

                # Save generated video file using the specific function
                media_video_file = save_generated_video_file(video_path, video_filename)

                # Save the record in AudioToVideo model
                audio_video_entry = AudioToVideo(audio_file=media_audio_file, image_file=media_image_file, video_file=media_video_file)
                audio_video_entry.save()

                return HttpResponse(f'<video controls><source src="/media/{video_filename}" type="video/mp4"></video>')
            except Exception as e:
                print(f"Error generating video: {e}")
                return HttpResponse(f"An error occurred while generating the video: {e}")
    else:
        form = AudioToVideoForm()

    return render(request, 'transcriber/audio_to_video.html', {'form': form})