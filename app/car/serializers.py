from django.db.models import Avg
from rest_framework import serializers

from .models import CarMake, CarModel, CarModelRate


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['make_name']


class CarModelSerializer(serializers.ModelSerializer):
    make = serializers.SlugRelatedField(
        slug_field='make_name',
        queryset=CarMake.objects.all()
    )
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['make', 'model_name', 'average_rate']

    def get_average_rate(self, car_model_instance):
        """Counts an average value of all rates
        associated to a certain CarModel instance."""

        return car_model_instance.rates.aggregate(
            Avg('model_rate')).get('model_rate__avg')


class CarModelRateSerializer(serializers.ModelSerializer):
    model = serializers.SlugRelatedField(
        slug_field='model_name',
        queryset=CarModel.objects.all()
    )

    class Meta:
        model = CarModelRate
        fields = ['model', 'model_rate']
