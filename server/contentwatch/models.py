from django.contrib.auth.models import AbstractUser
from django.db import models


# ContentWatch models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email


class PlatformIntegration(models.Model):
    PLATFORM_CHOICES = [
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    
    access_token = models.TextField(null=True, blank=True)  # optional
    channel_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    PLATFORM_CHOICES = [
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platforms_used = models.ForeignKey(PlatformIntegration, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    title = models.TextField()
    
    views = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()

    duration = models.IntegerField(help_text="seconds")
    posted_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class PostFeatures(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    engagement_rate = models.FloatField()
    like_ratio = models.FloatField()
    comment_ratio = models.FloatField()

    is_short = models.BooleanField()
    time_bucket = models.CharField(max_length=20)
    topic = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class AnalysisRun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="completed")
    total_posts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Insight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    analysis = models.ForeignKey(AnalysisRun, on_delete=models.CASCADE)

    best_content_type = models.CharField(max_length=100)
    best_topic = models.CharField(max_length=100)
    best_posting_time = models.CharField(max_length=100)
    best_duration = models.CharField(max_length=100)

    strategy = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class ContentDNA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    short_form_affinity = models.FloatField()
    education_score = models.FloatField()
    entertainment_score = models.FloatField()
    
    morning_performance = models.FloatField()
    evening_performance = models.FloatField()
    night_performance = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)