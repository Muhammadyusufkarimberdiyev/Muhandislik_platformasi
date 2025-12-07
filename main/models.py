from django.db import models
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ... Eski modellaringiz ...

class UserProfile(models.Model):
    """Foydalanuvchi profili va tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
    class Meta:
        verbose_name = "Foydalanuvchi Profili"
        verbose_name_plural = "Foydalanuvchilar Profili"


class LoginHistory(models.Model):
    """Kirish tarixi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
    
    class Meta:
        verbose_name = "Kirish Tarixi"
        verbose_name_plural = "Kirish Tarixi"
        ordering = ['-login_time']


# Signal - User yaratilganda avtomatik profile yaratish
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

        
class BookCategory(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name="books")
    text = models.TextField(max_length=355)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    file=models.FileField(upload_to="")
    def __str__(self):
        return self.name


class VideoCategory(models.Model):
    name = models.CharField(max_length=55)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=55)
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, related_name="videos")
    link = models.URLField(max_length=1000)
    min=models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ClassCategory(models.Model):
    name = models.CharField(max_length=55)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class ClassVideo(models.Model):
    name = models.CharField(max_length=55)
    category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE, related_name="videos")
    link = models.URLField(max_length=1000, blank=True, null=True)
    video_file = models.FileField(upload_to='class_videos/', blank=True, null=True)  # VIDEO FAYL
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def get_video_url(self):
        """Video URL yoki fayl yo'lini qaytaradi"""
        if self.video_file:
            return self.video_file.url
        return self.link or ""
    
from django.db import models

class ExperimentCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class Experiment(models.Model):
    DIFFICULTY = (
        ("easy", "Boshlang'ich"),
        ("medium", "O‘rta"),
        ("hard", "Murakkab"),
    )
    category = models.ForeignKey(
        ExperimentCategory,
        on_delete=models.CASCADE,
        related_name="experiments"
    )
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="", blank=True, null=True)
    html_file = models.FileField(upload_to="experiments/", blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default="hard")

  
    date = models.DateTimeField(auto_now_add=True)

    def display_url(self):
        if self.html_file:
            return self.html_file.url
        if self.link:
            return self.link
        if self.youtubelink1:
            return self.youtubelink1
        if self.youtubelink2:
            return self.youtubelink2
        if self.youtubelink3:
            return self.youtubelink3
        return "#"

    def __str__(self):
        return self.name
