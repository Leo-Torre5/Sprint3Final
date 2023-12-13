# MelodyMatrix/admin.py
from django.contrib import admin
from .models import Album, Song, Artist, Genre, AlbumInstance
from user_management.models import UserProfile
from user_management.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Loan, LoanCart



class AlbumInstanceInline(admin.TabularInline):
    model = AlbumInstance
    extra = 1

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'copies_available', ]
    inlines = [AlbumInstanceInline]

@admin.register(AlbumInstance)
class AlbumInstanceAdmin(admin.ModelAdmin):
    list_display = ('album', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('album', 'format', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Song)
admin.site.register(Loan)
admin.site.register(LoanCart)
