from rest_framework import viewsets, mixins
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.signals import request_finished
from django.views.generic.base import View
from django.dispatch import receiver
from . import models, serializers


class UrlViewset(
                 viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin
                ):
    """
    This view manages the URL objects
    """
    def get_queryset(self):
        return models.Url.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUrlSerializer
        
        return serializers.ViewUrlSerializer
    
    def get_object(self):
        return get_object_or_404(models.Url, slug=self.kwargs.get('pk'))


class ClickViewset(
                   viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin
                  ):
    """
    This view manages the Click objects related to a specific URL
    """
    serializer_class = serializers.ClickSerializer


    def get_url(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(models.Url, slug=slug)        

    def get_queryset(self):        
        url = self.get_url()
        return models.Click.objects.filter(url=url)


class RedirectView(View):
    """
    This handles redirects
    """
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def process_click_data(self, click):
        headers = dict(self.request.headers)
        click.user_agent = headers.get('User-Agent')
        click.referer=headers.get('Referer')
        click.client_ip = self.get_client_ip()
        click.save()
        return click
    
    def get_response(self, url):
        response = HttpResponse(status=301)
        response['Location'] = url.target       
        response['Cache-Control'] = 'no-cache'
        return response

    def dispatch(self, request, slug, *args, **kwargs):
        url = get_object_or_404(models.Url, slug=slug)
        click = self.process_click_data(models.Click(url=url))
        response = self.get_response(url)
        return response