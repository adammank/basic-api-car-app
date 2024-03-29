# Generated by Django 3.1.4 on 2021-03-30 07:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('make', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('model', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='car.carmake')),
            ],
        ),
        migrations.CreateModel(
            name='CarModelRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='car.carmodel')),
            ],
        ),
    ]
