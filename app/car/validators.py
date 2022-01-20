from rest_framework.serializers import ValidationError


def string_validator(value):
    if not isinstance(value, str):
        raise ValidationError("Provided value is not a string type.")
    if value.isdigit():
        raise ValidationError("Provided value can not be a digit.")
