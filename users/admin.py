from django.contrib import admin
from .models import Portfolio
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_id')  # Display user and profile_id in the admin list view
    search_fields = ('user__username', 'profile_id')  # Allow searching by username and profile_id

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Portfolio)
