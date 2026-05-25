from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from contentwatch.views import (
    RegisterView, LoginView, UserMeView,
    EngagementTimeSeries, ViewTimeSeries, InsightsView,
    ContentTypeBucketView, DurationBucketView, TimeBucketView,
    ContentDNAView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # ── API Schema & Docs ────────────────────────────────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ── Auth (existing) ──────────────────────────────────────────────
    path('api/auth/register', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login', LoginView.as_view(), name='auth_login'),
    path('api/auth/me', UserMeView.as_view(), name='auth_me'),

    # ── Analytics (existing) ─────────────────────────────────────────
    path('api/user/insights', InsightsView.as_view(), name='insights'),
    path('api/user/timeseries/engagements', EngagementTimeSeries.as_view(), name='engagements'),
    path('api/user/timeseries/views', ViewTimeSeries.as_view(), name='views'),
    path('api/user/bucket/contentype', ContentTypeBucketView.as_view(), name='content_type_bucket'),
    path('api/user/bucket/duration', DurationBucketView.as_view(), name='duration_bucket'),
    path('api/user/bucket/time', TimeBucketView.as_view(), name='time_bucket'),
    path('api/user/contentdna', ContentDNAView.as_view(), name='content_dna'),

    # ── Collaboration Infrastructure ─────────────────────────────────
    path('api/', include('teams.urls')),
    path('api/', include('roles.urls')),
    path('api/', include('workflows.urls')),
    path('api/', include('approvals.urls')),
    path('api/', include('campaigns.urls')),
    path('api/', include('assets.urls')),
    path('api/', include('collaboration.urls')),
    path('api/', include('messaging.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
