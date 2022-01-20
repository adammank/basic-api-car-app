from django.db import transaction
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.response import Response

from car.models import CarModel, CarModelRate
from car.serializers import CarModelSerializer, CarModelAndMakeCreateSerializer, CarModelRateSerializer
from car.service import CarService
from car.constants import ResponseData


class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create method uses different serializer_class beacuse of its task:
        it first has to create or get the instance of the parent model (CarMake),
        to be able to create or get the demanded instance of the CarModel.
        """

        make = request.data.get('make')
        model = request.data.get('model')

        serializer = CarModelAndMakeCreateSerializer(data=request.data)
        if serializer.is_valid():
            car_service = CarService(make=make, model=model)
            if car_service.model_exists():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=ResponseData.CAR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        """Returns CarModel objects ordered by the
        number of the associated CarModelRate instances."""

        qs = super().get_queryset()
        return qs.annotate(number_of_rates=Count('rates')).order_by(
            '-number_of_rates')


class CarModelRateViewSet(viewsets.ModelViewSet):
    queryset = CarModelRate.objects.all()
    serializer_class = CarModelRateSerializer