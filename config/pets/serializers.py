from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Cat, Dog, Horse, Rabbit

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("url", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user


class PetOwnerMixin(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")


class CatSerializer(PetOwnerMixin):
    class Meta:
        model = Cat
        fields = "__all__"


class DogSerializer(PetOwnerMixin):
    class Meta:
        model = Dog
        fields = "__all__"


class HorseSerializer(PetOwnerMixin):
    class Meta:
        model = Horse
        fields = "__all__"


class RabbitSerializer(PetOwnerMixin):
    class Meta:
        model = Rabbit
        fields = "__all__"
