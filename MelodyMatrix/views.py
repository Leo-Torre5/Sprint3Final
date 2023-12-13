#MelodyMatrix/views.py
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.db.models import Count
from django.contrib.auth import get_user_model
from .models import Album, Artist, AlbumInstance, Genre, Song
from django.http import Http404
from .forms import GenreForm
from .forms import LoanAlbumForm, AlbumForm, SearchForm
from user_management.forms import UserCreationForm
from user_management.models import UserProfile
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .forms import SongForm
from django.db.models import ProtectedError
from .forms import GenreForm
from django.db.models import F, Func, CharField
from django.contrib.auth.decorators import login_required
from .models import LoanCart
from .forms import LoanCartForm
from django.utils import timezone
from datetime import timedelta
from .models import Loan










class AboutView(TemplateView):
    template_name = 'MelodyMatrix/about_us.html'

class ContactUsView(TemplateView):
    template_name = 'MelodyMatrix/contact_us.html'

class LibraryPoliciesView(TemplateView):
    template_name = 'MelodyMatrix/library_policies.html'



def index(request):
    """View function for home page of the site."""
    num_albums = Album.objects.all().count()
    num_instances = AlbumInstance.objects.all().count()
    num_instances_available = AlbumInstance.objects.filter(status__exact='a').count()
    num_artists = Artist.objects.count() # Add this line to get the count of artists.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_albums': num_albums,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_artists': num_artists,# Include num_artists in the context
        'num_visits': num_visits, }
    return render(request, 'MelodyMatrix/index.html', context=context)


def artist_list(request):
    sort_param = request.GET.get('sort', 'name')  # Default sorting by name (A-Z)
    if sort_param == 'name':
        artists = Artist.objects.all().annotate(lower_name=Func(F('artist_name'), function='LOWER', output_field=CharField())).order_by('lower_name')
    elif sort_param == '-name':
        artists = Artist.objects.all().annotate(lower_name=Func(F('artist_name'), function='LOWER', output_field=CharField())).order_by('-lower_name')
    elif sort_param == 'oldest':
        artists = Artist.objects.all().order_by('id')
    elif sort_param == '-oldest':
        artists = Artist.objects.all().order_by('-id')
    else:
        # Handle other sorting options if needed
        artists = Artist.objects.all()

    return render(request, 'MelodyMatrix/artist_list.html', {'artists': artists})


def artist_inventory(request):
    artists = Artist.objects.all()
    return render(request, 'MelodyMatrix/artist_inventory.html', {'artists': artists})


def all_genres(request):
    genres = Genre.objects.all()
    return render(request, 'MelodyMatrix/all_genres.html', {'genres': genres})


def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    artists = Artist.objects.filter(genre=genre)
    albums = Album.objects.filter(genre=genre)

    context = {
        'genre': genre,
        'artists': artists,
        'albums': albums,
    }

    return render(request, 'MelodyMatrix/genre_detail.html', context)



class AlbumListView(generic.ListView):
    model = Album
    template_name = 'MelodyMatrix/album_list.html'  # Update with your actual template name
    context_object_name = 'album_list'

    def get_queryset(self):
        # Default sorting by title (A-Z)
        sort_param = self.request.GET.get('sort', 'title')

        if sort_param == 'title':
            return Album.objects.annotate(lower_title=Func(F('title'), function='LOWER', output_field=CharField())).order_by('lower_title')
        elif sort_param == '-title':
            return Album.objects.annotate(lower_title=Func(F('title'), function='LOWER', output_field=CharField())).order_by('-lower_title')
        elif sort_param == 'oldest':
            return Album.objects.all().order_by('id')
        elif sort_param == '-oldest':
            return Album.objects.all().order_by('-id')
        else:
            # Handle other sorting options if needed
            return Album.objects.all()




class AlbumDetailView(generic.DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_copies'] = self.object.albuminstance_set.filter(status='a')
        return context


class ArtistListView( generic.ListView):
    model = Artist



class ArtistDetailView(generic.DetailView):
    model = Artist


class LoanedAlbumsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing albums on loan or reserved to the current user."""
    model = AlbumInstance
    template_name = 'MelodyMatrix/my_vinyl.html'
    paginate_by = 10

    def get_queryset(self):
        return AlbumInstance.objects.filter(borrower=self.request.user, status__in=['o', 'r']).order_by('due_back')


class ArtistCreate(CreateView):
    model = Artist
    fields = ['artist_name', 'summary', 'genre', 'artist_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('artist_inventory'))

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['artist_name', 'summary', 'genre', 'artist_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('artist_inventory'))

class AlbumCreate(CreateView):
    model = Album
    form_class = AlbumForm  # Use the new form class
    template_name = 'MelodyMatrix/album_form.html'

    def form_valid(self, form):
        # You can add any additional logic here if needed
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manage_albums')  # Update with your actual URL for the list of albums

class AlbumUpdate(UpdateView):
    model = Album
    form_class = AlbumForm  # Use the new form class
    template_name = 'MelodyMatrix/album_form.html'

    def form_valid(self, form):
        # You can add any additional logic here if needed
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manage_albums')  # Update with your actual URL for the list of albums

def album_inventory(request):
    albums = Album.objects.all()
    context = {'album_list': albums}
    return render(request, 'MelodyMatrix/manage_albums.html', context)




def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)

    try:
        artist_name = artist.artist_name
        artist.delete()
        messages.success(request, f'{artist_name} has been deleted')
    except Exception as e:
        messages.error(request, f'{artist.artist_name} cannot be deleted. Albums exist for this artist. Error: {e}')

    return redirect('artist_inventory')


def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)

    try:
        album_title = album.title
        album.delete()
        messages.success(request, f'{album_title} has been deleted')
    except ProtectedError:
        messages.error(request, f'{album_title} cannot be deleted. Artists exist for this album')

    return redirect('manage_albums')


class AvailAlbumsListView(generic.ListView):
    model = AlbumInstance
    template_name = 'MelodyMatrix/manage_inventory.html'
    paginate_by = 10

    def get_queryset(self):
        return AlbumInstance.objects.all().order_by('album__title')



def loan_album_librarian(request, pk):
    album_instance = get_object_or_404(AlbumInstance, pk=pk)

    if request.method == 'POST':
        form = LoanAlbumForm(request.POST, instance=album_instance)

        if form.is_valid():
            # Retrieve the due_back from the form
            due_back = form.cleaned_data['due_back']

            # Update the AlbumInstance fields
            album_instance = form.save(commit=False)
            album_instance.due_back = due_back
            album_instance.LOAN_STATUS = 'o'  # Update the status to 'On loan'
            album_instance.save()

            return HttpResponseRedirect(reverse('manage_inventory'))

    else:
        form = LoanAlbumForm(instance=album_instance,
                             initial={'album_title': album_instance.album.title,
                                      'due_back': album_instance.due_back,
                                      'status': 'o'})

    return render(request, 'MelodyMatrix/loan_album_librarian.html', {'form': form})


def return_album(request, pk):
    album_instance = get_object_or_404(AlbumInstance, pk=pk)

    if request.method == 'POST':
        form = LoanAlbumForm(request.POST, instance=album_instance)

        if form.is_valid():
            status = form.cleaned_data['status']

            if status == 'a':
                album_instance.status = 'a'
                album_instance.borrower = None
                album_instance.due_back = None
                album_instance.save()
                messages.success(request, f'Album "{album_instance.album.title}" has been returned.')
                return redirect('manage_inventory')
            else:
                messages.error(request, 'Invalid status for returning the album.')

    else:
        # Set the default status in the model instance
        album_instance.status = 'a'
        album_instance.save()

        # Create an instance of the LoanAlbumForm
        form = LoanAlbumForm(instance=album_instance, initial={'album_title': album_instance.album.title})

    return render(request, 'MelodyMatrix/return_album.html', {'form': form, 'album_instance': album_instance})


def genre_inventory(request):
    # Default sorting by name (A-Z)
    sort_param = request.GET.get('sort', 'name')

    if sort_param == 'name':
        genres = Genre.objects.all().annotate(lower_name=Func(F('name'), function='LOWER', output_field=CharField())).order_by('lower_name')
    elif sort_param == '-name':
        genres = Genre.objects.all().annotate(lower_name=Func(F('name'), function='LOWER', output_field=CharField())).order_by('-lower_name')
    else:
        # Handle other sorting options if needed
        genres = Genre.objects.all()

    return render(request, 'MelodyMatrix/genre_inventory.html', {'genres': genres})


def delete_genre(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == 'POST':
        # Delete the genre
        genre_name = genre.name
        genre.delete()

        # Add a success message (optional)
        messages.success(request, f'The genre "{genre_name}" has been deleted.')
        print(messages.get_messages(request))

        # Redirect to the genre inventory page
        return redirect('genre_inventory')

    return render(request, 'MelodyMatrix/delete_genre.html', {'genre': genre})


def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the genre inventory page
            return redirect('genre_inventory')
    else:
        form = GenreForm()

    return render(request, 'MelodyMatrix/add_genre.html', {'form': form})

@permission_required('MelodyMatrix.edit_albuminstance')
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.save()
            return render(request, 'MelodyMatrix/album_detail.html', {'album': album})
    else:
        form = AlbumForm()
    return render(request, 'MelodyMatrix/album_form.html', {'form': form})


class SongListView(ListView):
    model = Song
    template_name = 'MelodyMatrix/song_inventory.html'
    context_object_name = 'song_list'

class SongCreateView(View):
    template_name = 'MelodyMatrix/song_form.html'
    form_class = SongForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'form_title': 'Add Song'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Set the album instance for the song before saving
            song = form.save(commit=False)
            song.album = form.cleaned_data['album']
            song.save()
            return redirect('song_inventory')
        return render(request, self.template_name, {'form': form, 'form_title': 'Add Song'})

class SongUpdateView(UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'MelodyMatrix/song_form.html'
    success_url = reverse_lazy('song_inventory')

class SongDeleteView(DeleteView):
    model = Song
    template_name = 'MelodyMatrix/song_confirm_delete.html'
    success_url = reverse_lazy('song_inventory')


def edit_genre(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_inventory')  # Redirect to the genre detail page or any other appropriate page
    else:
        form = GenreForm(instance=genre)

    return render(request, 'MelodyMatrix/edit_genre.html', {'form': form, 'genre': genre})



def privacy_policy_view(request):

    return render(request, 'MelodyMatrix/Privacy_Policy.html')



def about_us(request):
    return render(request, 'about_us.html', {'content': 'About Us'})

def contact_us(request):
    return render(request, 'contact_us.html', {'content': 'Contact Us'})

def library_policies(request):
    return render(request, 'library_policies.html', {'content': 'Library Policies'})

def privacy_policies(request):
    return render(request, 'privacy_policies.html', {'content': 'Privacy Policies'})


def search_view(request):
    query = request.GET.get('query')

    # Initialize content variables with empty strings
    about_us_content = ''
    contact_us_content = ''
    library_policies_content = ''
    privacy_policies_content = ''

    # Check if there is a non-empty query
    if query:
        # Search for artists
        artists = Artist.objects.filter(artist_name__icontains=query)

        # Search for albums
        albums = Album.objects.filter(title__icontains=query)

        # Search for genres
        genres = Genre.objects.filter(name__icontains=query)

        # Search for songs
        songs = Song.objects.filter(title__icontains=query)

        # Get the albums for the songs
        song_albums = [song.album for song in songs]

        # Initialize content variables with actual content
        about_us_content = 'About Us'
        contact_us_content = 'Contact Us'
        library_policies_content = 'Policies'
        privacy_policies_content = 'Policies'
    else:
        # If there's no query, set empty lists for results
        artists = []
        albums = []
        genres = []
        songs = []
        song_albums = []

    context = {
        'query': query,
        'artists': artists,
        'albums': albums,
        'genres': genres,
        'songs': zip(songs, song_albums),
        'about_us_results': about_us_content.lower().count(query.lower()) > 0,
        'contact_us_results': contact_us_content.lower().count(query.lower()) > 0,
        'library_policies_results': library_policies_content.lower().count(query.lower()) > 0,
        'privacy_policies_results': privacy_policies_content.lower().count(query.lower()) > 0,
    }

    return render(request, 'search_results.html', context)


@login_required
def add_to_cart(request, album_id):
    # Logic to add album to the user's cart
    # Check if the user has a cart, create one if not
    cart, created = LoanCart.objects.get_or_create(user=request.user)

    # Add the selected album to the cart
    album = Album.objects.get(pk=album_id)
    cart.albums.add(album)

    return redirect('view_cart')


@login_required
def view_cart(request):
    # Logic to display the user's cart
    cart, created = LoanCart.objects.get_or_create(user=request.user)
    return render(request, 'MelodyMatrix/view_cart.html', {'cart': cart})



@login_required
def checkout(request):
    # Get the user's cart
    cart, created = LoanCart.objects.get_or_create(user=request.user)

    # Prepopulate first name and last name fields with user information
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        # Add other initial data if needed
    }

    if request.method == 'POST':
        # Check if the cart is not empty
        if cart.albums.exists():
            # Your existing checkout logic
            for album in cart.albums.all():
                Loan.objects.create(borrower=request.user, album=album, due_back=timezone.now() + timedelta(days=14))
                album.status = 'o'
                album.save()

            cart.albums.clear()

            messages.success(request, 'Checkout successful. Your albums are now on loan.')
            return redirect('checkout_success')  # Redirect to a checkout success page

        else:
            # Redirect to view_cart.html with a warning message
            messages.warning(request, 'Your cart is empty. Add albums to the cart before trying to reserve.')
            return render(request, 'MelodyMatrix/view_cart.html', {'cart': cart, 'initial_data': initial_data})

    return render(request, 'MelodyMatrix/view_cart.html', {'cart': cart, 'initial_data': initial_data})


def checkout_success(request):
    return render(request, 'MelodyMatrix/checkout_success.html')

