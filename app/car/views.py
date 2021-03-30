from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count

from .models import CarMake, CarModel, CarModelRate
from .serializers import CarModelSerializer, CarModelRateSerializer
from .service import CarService


class CarListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    def create(self, request, *args, **kwargs):
        """Based on the retrived values, checks if the car exists in the external API.
        If yes - creates two instances: CarMake & CarModel,
                 responds with 201 Created status.
        If no - responds with 404 Not Found status."""

        make_name = request.data.get('make')
        model_name = request.data.get('model_name')
        car_service = CarService(
            car_make_name=make_name, car_model_name=model_name)

        if car_service.model_exists():

            car_make_instance, created = CarMake.objects.get_or_create(
                make_name=make_name)

            data = {
                'make': car_make_instance.make_name,
                'model_name': model_name
            }
            car_model_serializer = super().get_serializer(data=data)

            if car_model_serializer.is_valid():
                car_model_serializer.save()
                return Response(car_model_serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(car_model_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CarPopularListAPIView(generics.ListAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    def get_queryset(self):
        """Returns CarModel objects ordered by
        number of associated CarModelRate instances."""

        qs = super().get_queryset()
        return qs.annotate(number_of_rates=Count('rates')).order_by(
            '-number_of_rates')


class CarModelRateViewSet(viewsets.ModelViewSet):
    queryset = CarModelRate.objects.all()
    serializer_class = CarModelRateSerializer