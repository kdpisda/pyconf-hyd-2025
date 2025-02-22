from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from todo.views import ItemViewSet
from todo.views import ListViewSet

router = DefaultRouter()
router.register("lists", ListViewSet, basename="list")
router.register("items", ItemViewSet, basename="item")

urlpatterns = [
    path("", include(router.urls)),
]
