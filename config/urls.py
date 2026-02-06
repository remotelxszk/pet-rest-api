from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .pets.views import UserViewSet, GroupViewSet, CatViewSet, DogViewSet, HorseViewSet, RabbitViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"cats", CatViewSet)
router.register(r"dogs", DogViewSet)
router.register(r"horses", HorseViewSet)
router.register(r"rabbits", RabbitViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('login/', views.obtain_auth_token),
]

