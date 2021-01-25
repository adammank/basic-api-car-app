def external_car_api_url(make_name):
    return f'https://vpic.nhtsa.dot.gov/api/vehicles/' \
           f'GetModelsForMake/{make_name}?format=json'
