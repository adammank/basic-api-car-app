import requests


class CarService:
    """The main goal of this service is to check,
    if the provided car exists in the external API."""

    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

    def model_exists(self) -> bool:
        car_list = self._get_car_list()

        # Each car_model in the car_list is a separate dictionary.
        for car_model in car_list:
            if self.model == car_model.get('Model_Name'):
                return True
        return False

    def _get_car_list(self) -> list:
        try:
            car_dict = requests.get(
                url=f'https://vpic.nhtsa.dot.gov/api/vehicles/'
                    f'GetModelsForMake/{self.make}?format=json'
            ).json()
        except Exception:
            car_dict = dict()

        # Returned dict has a list of the cars (another dicts) under the key "Results".
        return car_dict.get('Results', list())
