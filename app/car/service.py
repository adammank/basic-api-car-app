import requests


class CarService:
    """Based on 2 passed variables (car_make_name & car_model_name),
    checks if the given car exists in the external API."""

    def __init__(self, car_make_name, car_model_name):
        self.car_make_name = car_make_name
        self.car_model_name = car_model_name

    def model_exists(self):
        car_list = self._get_car_list()

        # Each car in the car list is a separate dictionary.
        for car_model in car_list:
            car_model_name = car_model.get('Model_Name')
            if self.car_model_name == car_model_name:
                return True
        return False

    def _get_car_list(self):
        car_list = requests.get(
            url=f'https://vpic.nhtsa.dot.gov/api/vehicles/'
                f'GetModelsForMake/{self.car_make_name}?format=json'
        ).json()

        # Returned dict has car list as a value for the key "Results".
        return car_list.get('Results')
