#MelodyMatrix/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import return_album
from django.contrib import admin
from django.urls import path, include
from .views import search_view
from user_management.views import profile
from user_management.views import view_profile
from .views import genre_detail, all_genres
from .views import album_inventory
from .views import ArtistListView
from .views import genre_inventory, add_genre, delete_genre
from .views import artist_list
from .views import artist_inventory
from .views import AboutView
from .views import ContactUsView
from .views import LibraryPoliciesView
from .views import SongListView, SongCreateView, SongUpdateView, SongDeleteView
from .views import edit_genre
from .views import add_to_cart, view_cart, checkout, checkout_success



urlpatterns = [
        path('', views.index, name='index'),
        path('album_list/', views.AlbumListView.as_view(), name='album_list'),
        path('album_detail/<int:pk>', views.AlbumDetailView.as_view(), name='album_detail'),
        path('artist_list/', artist_list, name='artist_list'),
        path('artist_detail/<int:pk>', views.ArtistDetailView.as_view(), name='artist_detail'),
        path('my_vinyl/', views.LoanedAlbumsByUserListView.as_view(), name='my_vinyl'),
        path('artist/create/', views.ArtistCreate.as_view(), name='artist_create'),
        path('artist/<int:pk>/update/', views.ArtistUpdate.as_view(), name='artist_update'),
        path('artist/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
        path('album/create/', views.AlbumCreate.as_view(), name='album_create'),
        path('album/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album_update'),
        path('album/<int:pk>/delete/', views.album_delete, name='album_delete'),
        path('album/<uuid:pk>/loan/', views.loan_album_librarian, name='loan_album_librarian'),
        path('manage_inventory/', views.AvailAlbumsListView.as_view(), name='manage_inventory'),
        path('albuminstance/<uuid:pk>/return/', return_album, name='return_album'),
        path('user-management/', include('user_management.urls')),
        path('register/', include('register.urls')),
        path('search/', search_view, name='search'),
        path('profile/', profile, name='profile'),
        path('view_profile/', view_profile, name='view_profile'),
        path('genre_inventory/', genre_inventory, name='genre_inventory'),
        path('genre/<int:pk>/', genre_detail, name='genre_detail'),
        path('add_genre/', add_genre, name='add_genre'),
        path('genre/edit/<int:pk>/', edit_genre, name='edit_genre'),
        path('delete_genre/<int:pk>/', delete_genre, name='delete_genre'),
        path('all_genres/', all_genres, name='all_genres'),
        path('genre_inventory/', genre_inventory, name='genre_inventory'),
        path('manage_albums/', views.album_inventory, name='manage_albums'),
        path('artist_inventory/', artist_inventory, name='artist_inventory'),
        path('about/', AboutView.as_view(), name='about_us'),
        path('library_policies/', LibraryPoliciesView.as_view(), name='library_policies'),
        path('contact_us/', ContactUsView.as_view(), name='contact_us'),
        path('songs/', SongListView.as_view(), name='song_inventory'),
        path('songs/create/', SongCreateView.as_view(), name='song_create'),
        path('songs/<int:pk>/', SongUpdateView.as_view(), name='song_update'),
        path('songs/<int:pk>/delete/', SongDeleteView.as_view(), name='song_delete'),
        path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
        path('add_to_cart/<int:album_id>/', add_to_cart, name='add_to_cart'),
        path('view_cart/', view_cart, name='view_cart'),
        path('checkout/', checkout, name='checkout'),
        path('checkout/success/', checkout_success, name='checkout_success'),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
