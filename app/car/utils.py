from .serializers import CarMakeSerializer


def create_car_make_instance(make_name):
    serializer = CarMakeSerializer(data={"make": make_name})
    serializer.is_valid(raise_exception=True)
    serializer.save()
