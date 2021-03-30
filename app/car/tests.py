from unittest import mock

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from django.db.models import Count

from .models import CarMake, CarModel, CarModelRate
from .serializers import CarModelSerializer
from .service import CarService


### Only a few cases vere coverage by tests.


class TestUtils:

    car_model_data = {
        'make': 'honda',
        'model': 'Civic'
    }
    car_model_rate_valid_data = {
        'model': 'Civic',
        'rate': 5
    }
    car_model_rate_invalid_data = {
        'model': 'Civic',
        'rate': True
    }

    @staticmethod
    def _create_instances_for_tests(create_rates: bool = True):

        car_make_instance = CarMake.objects.create(make='honda')

        car_model_instance_01 = CarModel.objects.create(
            make=car_make_instance, model='Civic')
        car_model_instance_02 = CarModel.objects.create(
            make=car_make_instance, model='CR85')

        if not create_rates:
            return

        CarModelRate.objects.create(model=car_model_instance_01, rate=5)
        CarModelRate.objects.create(model=car_model_instance_02, rate=1)
        CarModelRate.objects.create(model=car_model_instance_02, rate=2)


class POSTCarTestCase(APITestCase, TestUtils):

    @mock.patch('car.service.CarService.model_exists')
    def test_cars_post__model_not_exists(self, model_exists_mock):
        """
            Test for POST http method onto /cars/ url with assumption, that
            included in view model_exists method will return False.
        """

        model_exists_mock.return_value = False
        response = self.client.post(
            path='/cars/', data=self.car_model_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(0, CarMake.objects.all().count())
        self.assertEqual(0, CarModel.objects.all().count())


    def test_cars_post__model_exists(self):
        """
            Test for POST http method onto /cars/ url with assumption, that
            included in view model_exists method will return True.
        """
        with mock.patch.object(CarService, 'model_exists') as model_exists_mock:
            model_exists_mock.return_value = True
            response = self.client.post(
                path='/cars/', data=self.car_model_data
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(1, CarMake.objects.all().count())
            self.assertEqual(1, CarModel.objects.all().count())


    def test_rate_post__valid_data(self):
        """
            Test for POST http method onto /rate/ url path with the valid data.
        """

        self._create_instances_for_tests(create_rates=False)
        response = self.client.post(
            path='/rates/', data=self.car_model_rate_valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, CarModelRate.objects.all().count())


    def test_rate_post__invalid_data(self):
        """
            Test for POST http method onto /rate/ url path with the invalid data.
        """

        self._create_instances_for_tests(create_rates=False)
        response = self.client.post(
            path='/rates/', data=self.car_model_rate_invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, CarModelRate.objects.all().count())


class GETCarTestCase(APITestCase, TestUtils):

    def test_cars_get(self):
        """
            Test for GET http method onto /cars/ url path.
        """

        self._create_instances_for_tests()

        response = self.client.get('/cars/')
        json_response = response.json()
        json_response_data = JSONRenderer().render(json_response)

        car_models = CarModel.objects.all().annotate(
            number_of_rates=Count('rates')).order_by(
            '-number_of_rates')
        serializer = CarModelSerializer(car_models, many=True)
        json_serializer_data = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response_data, json_serializer_data)


    def test_rates_get(self):
        """
            Test for GET http method onto /rate/ url path.
        """

        self._create_instances_for_tests()

        response = self.client.get('/rates/')
        json_response = response.json()
        json_response_data = JSONRenderer().render(json_response)

        car_rates = CarModelRate.objects.all()
        serializer = CarModelSerializer(car_rates, many=True)
        json_serializer_data = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response_data, json_serializer_data)