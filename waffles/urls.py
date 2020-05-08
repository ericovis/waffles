from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('', include('core.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
]


if settings.DEBUG:
    from django.contrib.auth import views as auth_views
    urlpatterns += [
        path('login/', auth_views.LoginView.as_view()),
        path('logout/', auth_views.LogoutView.as_view()),
    ]
