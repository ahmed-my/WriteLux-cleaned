from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Portfolio, ContactQuery, Folder

# Inline model to display Portfolio images in Folder admin
class PortfolioInline(admin.TabularInline):
    model = Portfolio.folder.through  # Access the through model of the ManyToMany field
    extra = 1  # Number of extra forms in the inline

class FolderAdmin(admin.ModelAdmin):
    inlines = [PortfolioInline]  # Include PortfolioInline in FolderAdmin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    list_display = ('name', 'user')  # Display name and user

admin.site.register(Folder, FolderAdmin)

# Define UserProfileAdmin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_id')  # Display user and profile_id in the admin list view
    search_fields = ('user__username', 'profile_id')  # Allow searching by username and profile_id

# Custom UserProfile and User admin
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

# Register UserProfile with the newly defined UserProfileAdmin
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Portfolio)

# Register ContactQuery with customized admin
@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
