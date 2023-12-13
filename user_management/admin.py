# user_management/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_library_card_number')
    search_fields = ('username', 'email', 'userprofile__library_card_number')

    def get_library_card_number(self, obj):
        return obj.userprofile.library_card_number if hasattr(obj, 'userprofile') else None

    get_library_card_number.short_description = 'Library Card Number'

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register the UserProfile model
admin.site.register(UserProfile)
