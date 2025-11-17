from django.forms import ModelForm
from .models import MusicPost

class MusicPostForm(ModelForm):
    class Meta:
        model = MusicPost
        fields = ['category', 'title', 'comment', 'image1', 'youtube_link']