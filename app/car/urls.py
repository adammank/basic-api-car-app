from django.urls import path, include
from rest_framework.routers import DefaultRouter

from car import views


router = DefaultRouter()
router.register(r'cars', views.CarModelViewSet, basename='cars')
router.register(r'rates', views.CarModelRateViewSet, basename='rates')

urlpatterns = [
    path('', include(router.urls)),
]
