from django.contrib import admin
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from contentwatch.views import (
    RegisterView, LoginView, UserMeView,
    EngagementTimeSeries, ViewTimeSeries, InsightsView
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/auth/register', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login', LoginView.as_view(), name='auth_login'),
    path('api/auth/me', UserMeView.as_view(), name='auth_me'),

    path('api/user/insights', InsightsView.as_view(), name='insights'),
    path('api/user/timeseries/engagements', EngagementTimeSeries.as_view(), name='engagements'),
    path('api/user/timeseries/views', ViewTimeSeries.as_view(), name='views'),
]

