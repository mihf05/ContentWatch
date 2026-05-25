from django.contrib import admin
from django.urls import path

from contentwatch.views import RegisterView, LoginView, UserMeView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/register', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login', LoginView.as_view(), name='auth_login'),
    path('api/auth/me', UserMeView.as_view(), name='auth_me'),
]
