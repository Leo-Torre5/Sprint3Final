#MelodyMatrix/forms.py
from .models import AlbumInstance
from django import forms
from .models import Album, Song
from .models import Genre
from .models import LoanCart


class SongForm(forms.ModelForm):
    # Add a field for selecting the album
    album = forms.ModelChoiceField(queryset=Album.objects.all(), required=False)

    class Meta:
        model = Song
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        # Optionally, customize the label for the album field
        self.fields['album'].label = 'Album'


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class LoanAlbumForm(forms.ModelForm):
    """Form for a librarian to loan albums."""
    album_title = forms.CharField(disabled=True, required=False)

    # Add a DateField for the due date
    due_back = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        # Display only the album title, borrower, status, and due date to the librarian
        model = AlbumInstance
        fields = ('album_title', 'borrower', 'status', 'due_back',)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'summary', 'genre', 'copies_available', 'album_image']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'image']


class LoanCartForm(forms.ModelForm):
    class Meta:
        model = LoanCart
        fields = ['first_name', 'last_name', 'email', 'address', 'zip_code', 'state']
