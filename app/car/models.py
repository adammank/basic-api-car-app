from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarMake(models.Model):

    make_name = models.CharField(
        max_length=20, unique=True, null=False, blank=False)

    def __str__(self):
        return self.make_name


class CarModel(models.Model):

    make = models.ForeignKey(
        to=CarMake, related_name='models',
        on_delete=models.CASCADE, null=False, blank=False)

    model_name = models.CharField(
        max_length=20, unique=True, null=False, blank=False)

    def __str__(self):
        return f"{self.make}, {self.model_name}"


class CarModelRate(models.Model):

    model = models.ForeignKey(
        to=CarModel, related_name='rates',
        on_delete=models.CASCADE, null=False, blank=False)

    model_rate = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Rate {self.model_rate} for model {self.model}"