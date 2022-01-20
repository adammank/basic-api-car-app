from django.db.models import Avg
from rest_framework import serializers

from car.models import CarMake, CarModel, CarModelRate
from car.validators import string_validator


class CarModelSerializer(serializers.ModelSerializer):

    average_rate = serializers.SerializerMethodField(
        method_name=r"get_average_rate"
    )

    class Meta:
        model = CarModel
        fields = ['make', 'model', 'average_rate']

    def get_average_rate(self, car_model_instance):
        """Counts an average value of all rates
        associated to a certain CarModel instance."""

        return car_model_instance.rates.aggregate(
            Avg('rate')).get('rate__avg')


class CarModelAndMakeCreateSerializer(serializers.Serializer):

    make = serializers.CharField(
        max_length=20, allow_null=False,
        allow_blank=False, validators=[string_validator]
    )
    model = serializers.CharField(
        max_length=20, allow_null=False,
        allow_blank=False, validators=[string_validator]
    )

    def create(self, validated_data):
        car_make_instance, created = CarMake.objects.get_or_create(
            make=validated_data.get('make'))
        car_model_instance, created = CarModel.objects.get_or_create(
            make=car_make_instance, model=validated_data.get('model'))
        return car_model_instance


class CarModelRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModelRate
        fields = ['model', 'rate']
