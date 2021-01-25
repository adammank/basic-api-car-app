from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from django.db.models import Count

from .models import CarMake, CarModel, CarModelRate
from .serializers import CarModelSerializer


class CarTestCase(APITestCase):

    def test_cars_post(self):
        """Tests for POST method onto /cars url path."""

        data = {
            'make': 'honda',
            'model_name': 'Civic'
        }
        response = self.client.post('/cars', data)

        len_car_makes = CarMake.objects.all().count()
        len_car_models = CarModel.objects.all().count()

        # Check for status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if exactly one model is created for CarMake & for CarModel
        self.assertEqual(1, len_car_makes)
        self.assertEqual(1, len_car_models)

    def test_cars_get(self):
        """Tests for GET method onto /cars url path."""

        self._create_instances_for_tests()

        response = self.client.get('/cars')
        response_json = response.json()
        real_json_response_data = JSONRenderer().render(response_json)

        car_models = CarModel.objects.all()
        serializer = CarModelSerializer(car_models, many=True)
        serializer_json_data = JSONRenderer().render(serializer.data)

        # Check for status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check equality between data got from server & those fetched here
        self.assertEqual(real_json_response_data, serializer_json_data)

    def test_popular_get(self):
        """Tests for GET method onto /popular url path."""

        self._create_instances_for_tests()

        response = self.client.get('/popular')
        response_json = response.json()
        real_json_response_data = JSONRenderer().render(response_json)

        car_models = CarModel.objects.annotate(
            number_of_rates=Count('rates')).order_by(
            '-number_of_rates')
        serializer = CarModelSerializer(car_models, many=True)
        serializer_json_data = JSONRenderer().render(serializer.data)

        # Check for status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check equality between data got from server & those fetched here
        self.assertEqual(real_json_response_data, serializer_json_data)

    def test_rate_post(self):
        """Tests for POST method onto /rate url path."""

        self._create_instances_for_tests(create_rates=False)

        data = {
            'model': 'Civic',
            'model_rate': 5
        }
        response = self.client.post('/rate', data)

        len_rates = CarModelRate.objects.all().count()

        # Check for status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if exactly one model is created for CarModelRate
        self.assertEqual(1, len_rates)

    @staticmethod
    def _create_instances_for_tests(create_rates=True):

        car_make_instance = CarMake.objects.create(make_name='honda')

        car_model_instance_01 = CarModel.objects.create(
            make=car_make_instance, model_name='Civic')
        car_model_instance_02 = CarModel.objects.create(
            make=car_make_instance, model_name='CR85')

        if not create_rates:
            return

        CarModelRate.objects.create(model=car_model_instance_01, model_rate=5)
        CarModelRate.objects.create(model=car_model_instance_02, model_rate=1)
        CarModelRate.objects.create(model=car_model_instance_02, model_rate=2)