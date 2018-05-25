from django import forms
from .models import Bookmark


class BookmarkForm(forms.ModelForm):

    class Meta:  # Meta != monkey
        model = Bookmark
        fields = ('url', 'name', 'notes')
