import uuid0
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import Base62


class CustomIdModel(models.Model):
    id = models.CharField(
        primary_key=True,
        unique=True,
        editable=False,
        max_length=21)

    def save(self, *args, **kwargs):
        while not self.id:
            new_id = self.pkgen()
            if not self.__class__.objects.filter(id=new_id).exists():
                self.id = new_id
        super().save(*args, **kwargs)

    def pkgen(self):
        return uuid0.generate().base62

    class Meta:
        abstract = True


class User(CustomIdModel, AbstractUser):
    pass


class Url(models.Model):
    target = models.URLField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.slug} -> {self.target}'
   
    @property
    def clicks_count(self):
        return self.clicks.count()
    

class Click(CustomIdModel):
    url = models.ForeignKey(Url, related_name='clicks', on_delete=models.CASCADE)
    client_ip = models.CharField(max_length=100, blank=True, null=True)
    referer = models.URLField(blank=True, null=True)
    user_agent = models.CharField(max_length=300, blank=True, null=True)    
    created_on = models.DateTimeField(auto_now_add=True)
