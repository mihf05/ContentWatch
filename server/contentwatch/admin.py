from django.contrib import admin

from .models import (
    User, PlatformIntegration, Post, PostFeatures, AnalysisRun, Insight, ContentDNA, 
)

admin.site.register([
    User,
    PlatformIntegration, 
    Post,
    PostFeatures,
    AnalysisRun,
    Insight,
    ContentDNA
])