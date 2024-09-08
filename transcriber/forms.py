from django import forms
from .models import *

class TextToAudioForm(forms.Form):
    """
    Form to input text and convert it into audio.
    """
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter text here...'}),
        label="Text",
        max_length=5000,
        help_text="Enter the text you want to convert to audio."
    )


class AudioToTextForm(forms.ModelForm):
    """
    Form to upload an audio file and convert it into text.
    """
    class Meta:
        model = MediaFile
        fields = ['file']
        widgets = {
        'file': forms.ClearableFileInput(attrs={'accept': 'audio/*'}),
        }
        labels = {
        'file': 'Upload Audio File',
        }

        def clean_file(self):
            file = self.cleaned_data['file']
            if not file.name.endswith(('.wav', '.mp3', '.m4a', '.flac')):
                raise forms.ValidationError("Invalid audio file format. Please upload a valid audio file.")
            return file

class VideoToAudioForm(forms.ModelForm):
    """
    Form to upload a video file and extract its audio.
    """
    class Meta:
        model = MediaFile
        fields = ['file']
        widgets = {'file': forms.ClearableFileInput(attrs={'accept': 'video/*'}),}
        labels = {
            'file': 'Upload Video File',
        }

        def clean_file(self):
            file = self.cleaned_data['file']
            if not file.name.endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
                raise forms.ValidationError("Invalid video file format. Please upload a valid video file.")
            return file

class AudioToVideoForm(forms.Form):
    """
    Form to upload an audio file and an image file to convert them into a video.
    """
    audio_file = forms.FileField(
    widget=forms.ClearableFileInput(attrs={'accept': 'audio/*'}),
    label="Upload Audio File"
    )
    image_file = forms.FileField(
    widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    label="Upload Image File"
    )

    def clean_audio_file(self):
        file = self.cleaned_data['audio_file']
        if not file.name.endswith(('.wav', '.mp3', '.m4a', '.flac')):
            raise forms.ValidationError("Invalid audio file format. Please upload a valid audio file.")
        return file

def clean_image_file(self):
    file = self.cleaned_data['image_file']
    if not file.name.endswith(('.jpg', '.jpeg', '.png')):
        raise forms.ValidationError("Invalid image file format. Please upload a valid image file.")
    return file