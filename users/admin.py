from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Portfolio, ContactQuery

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_id')
    search_fields = ('username', 'email', 'userprofile__profile_id')

    def get_profile_id(self, instance):
        return instance.userprofile.profile_id
    get_profile_id.short_description = 'Profile ID'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_id')  # Display user and profile_id in the admin list view
    search_fields = ('user__username', 'profile_id')  # Allow searching by username and profile_id

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Portfolio)

@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')