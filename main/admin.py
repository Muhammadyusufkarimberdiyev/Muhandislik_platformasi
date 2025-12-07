from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(BookCategory)
admin.site.register(VideoCategory)
admin.site.register(Book)
admin.site.register(Video)
admin.site.register(ExperimentCategory)
admin.site.register(Experiment)





# admin.py
from django.contrib import admin
from .models import ClassVideo, ClassCategory

@admin.register(ClassVideo)
class ClassVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'has_video_file')
    list_filter = ('category', 'date')
    search_fields = ('name',)
    
    def has_video_file(self, obj):
        return bool(obj.video_file)
    has_video_file.boolean = True
    has_video_file.short_description = 'Video fayl'

@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# ... Eski admin registrationlaringiz ...

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'registration_date', 'last_login_time', 'login_count', 'is_active')
    list_filter = ('is_active', 'registration_date', 'last_login_time')
    search_fields = ('user__username', 'user__email', 'full_name', 'phone')
    readonly_fields = ('registration_date', 'login_count', 'last_login_time')
    
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('user', 'full_name', 'phone')
        }),
        ('Statistika', {
            'fields': ('registration_date', 'last_login_time', 'login_count', 'is_active')
        }),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address', 'get_short_user_agent')
    list_filter = ('login_time', 'user')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'login_time', 'ip_address', 'user_agent')
    date_hierarchy = 'login_time'
    
    def get_short_user_agent(self, obj):
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return '-'
    get_short_user_agent.short_description = 'User Agent'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# User modelini kengaytirish
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('registration_date', 'login_count', 'last_login_time')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_login_count')
    
    def get_login_count(self, obj):
        return obj.profile.login_count if hasattr(obj, 'profile') else 0
    get_login_count.short_description = 'Kirish soni'


# User adminni qayta ro'yxatdan o'tkazish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)