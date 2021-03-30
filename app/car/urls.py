from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'rates', views.CarModelRateViewSet, basename='rates')

urlpatterns = [
    path('', include(router.urls)),

    path('popular',
         views.CarPopularListAPIView.as_view()),

    path('rate',
         views.CarModelRateCreateAPIView.as_view()),
]
