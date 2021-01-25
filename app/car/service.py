import requests
from . import constants


class CarService:
    """Based on 2 passed variables (car_make_name & car_model_name),
    checks if the given car exists in the external API."""

    def __init__(self, car_make_name, car_model_name):
        self.car_make_name = car_make_name
        self.car_model_name = car_model_name

    def check_if_the_model_exists_in_the_external_api(self):
        car_list = self._get_car_list()

        # Each car in the car list is a separate dictionary.
        for car_model in car_list:
            car_model_name = car_model.get('Model_Name')
            if self.car_model_name == car_model_name:
                return True
        return False

    def _get_car_list(self):
        car_list = requests.get(
            url=constants.external_car_api_url(self.car_make_name)
        ).json()

        # Returned dict has car list as a value for the key "Results".
        return car_list.get('Results')
