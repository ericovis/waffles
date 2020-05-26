from django.dispatch import receiver
from django.core.signals import request_finished
from django.db import models
from .models import Url
from .utils import Base62


@receiver(models.signals.post_save, sender=Url)
def generate_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = Base62.encode(instance.pk)
        instance.save()