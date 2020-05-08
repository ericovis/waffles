from django.contrib import admin
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'api/urls/(?P<slug>[^/]*)/clicks', views.ClickViewset, basename='click')
router.register(r'api/urls', views.UrlViewset)

urlpatterns = [
    path('<slug:slug>', views.redirect, name='redirect')
] + router.urls

