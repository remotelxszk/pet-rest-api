from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import Cat, Dog, Horse, Rabbit


from .models import Cat, Dog, Horse, Rabbit
from .serializers import (
    GroupSerializer,
    UserSerializer,
    UserCreateSerializer,
    CatSerializer,
    DogSerializer,
    HorseSerializer,
    RabbitSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(url=user.url)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.get(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class OwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(owner=user)

class CatViewSet(OwnedModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    @action(
        detail=False, 
        methods=["get"],
        permission_classes=[permissions.IsAdminUser]
    )
    def orange_thieves(self, request):
        qs = self.get_queryset().filter(
            is_orange_cat=True,
            steals_food=True,
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class DogViewSet(OwnedModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class HorseViewSet(OwnedModelViewSet):
    queryset = Horse.objects.all()
    serializer_class = HorseSerializer


class RabbitViewSet(OwnedModelViewSet):
    queryset = Rabbit.objects.all()
    serializer_class = RabbitSerializer

class PetsWithSameNameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        name = request.query_params.get("name")
        if not name:
            return Response({"error": "name query param required"}, status=400)

        user = request.user

        pets = {
            "cats": Cat.objects.filter(name=name, owner=user).values(),
            "dogs": Dog.objects.filter(name=name, owner=user).values(),
            "horses": Horse.objects.filter(name=name, owner=user).values(),
            "rabbits": Rabbit.objects.filter(name=name, owner=user).values(),
        }

        return Response(pets)
