from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from config.pets.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('api-token-auth/', views.obtain_auth_token),
]

