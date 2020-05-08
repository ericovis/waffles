from rest_framework import viewsets, mixins
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver
from . import models, serializers



class UrlViewset(
                 viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin
                ):
    queryset = models.Url.objects.all()
    
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
    serializer_class = serializers.ClickSerializer


    def get_url(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(models.Url, slug=slug)        

    def get_queryset(self):        
        url = self.get_url()
        return models.Click.objects.filter(url=url)


def redirect(request, slug):
    url = get_object_or_404(models.Url, slug=slug)

    response = HttpResponse(status=301)
    response['Location'] = url.target

    click = models.Click(url=url)
    click.data = dict(request.headers)
    click.save()

    return response