from django.urls import path

from . import views


urlpatterns = [

    path('cars',
         views.CarListCreateAPIView.as_view()),

    path('popular',
         views.CarPopularListAPIView.as_view()),

    path('rate',
         views.CarModelRateCreateAPIView.as_view()),
]
