from django.db.models import Avg
from rest_framework import serializers

from .models import CarMake, CarModel, CarModelRate


class CarMakeSerializer(serializers.Serializer):

    make = serializers.CharField(
        max_length=20,  allow_null=False, allow_blank=False,
    )

    def create(self, validated_data):
        car_make_instance, created = CarMake.objects.get_or_create(
            make=validated_data.get('make'))
        return car_make_instance


class CarModelSerializer(serializers.ModelSerializer):

    average_rate = serializers.SerializerMethodField(
        method_name=r"get_average_rate"
    )
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['make', 'model', 'average_rate']

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
