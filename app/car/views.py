from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Count

from .models import CarModel, CarModelRate
from .serializers import CarModelSerializer, CarModelRateSerializer
from .service import CarService
from .utils import create_car_make_instance
from .constants import CAR_NOT_FOUND


class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Based on the retrieved values, checks if the car exists in the external API.
        It yes - creates two instances: CarMake & CarModel,
                 responds with 201 Created status.
        If no - responds with 404 Not Found status."""

        car_make_name = request.data.get('make')
        car_model_name = request.data.get('model')

        car_service = CarService(
            car_make_name=car_make_name,
            car_model_name=car_model_name
        )

        if car_service.model_exists():
            create_car_make_instance(car_make_name)
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                data=CAR_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        """Returns CarModel objects ordered by
        number of associated CarModelRate instances."""

        qs = super().get_queryset()
        return qs.annotate(number_of_rates=Count('rates')).order_by(
            '-number_of_rates')


class CarModelRateViewSet(viewsets.ModelViewSet):
    queryset = CarModelRate.objects.all()
    serializer_class = CarModelRateSerializer