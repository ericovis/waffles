from rest_framework import serializers
from django.core.validators import validate_slug
from . import models


def check_if_slug_exists(value):
    if models.Url.objects.filter(slug=value).exists():
        raise serializers.ValidationError("This slug already exists")
    return value


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()
    class Meta:
        model = models.User
        exclude = ('password', 'account', )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }



class ViewUrlSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()    
    clicks = serializers.SerializerMethodField()
    class Meta:
        model = models.Url
        exclude = ('id', 'account', )

    def get_clicks(self, obj):
        return obj.clicks_count


class CreateUrlSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, validators=[validate_slug, check_if_slug_exists])
    class Meta:
        model = models.Url
        fields = ('target', 'slug',)
    

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Click
        exclude = ('url', 'id')