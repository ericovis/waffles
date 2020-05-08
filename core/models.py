import uuid0
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
from .utils import Base62

def get_media_path(instance, filename):
    extension = str(filename).split('.')[-1]
    return '{}.{}'.format(uuid0.generate(), extension)


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



class User(AbstractBaseUser, CustomIdModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    email = models.EmailField('email', unique=True)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    is_active = models.BooleanField(
        'active',
        default=True,
    )


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
    referer = models.URLField(blank=True, null=True)
    user_agent = models.CharField(max_length=300, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
