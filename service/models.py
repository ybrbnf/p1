#coding: utf-8
from django.db import models
from django.utils import timezone

class Services(models.Model):
    class Meta():
        db_table = 'services'

    hot_water = models.DecimalField('Hot water', max_digits=10, decimal_places=1)
    cold_water = models.DecimalField('Cold water', max_digits=10, decimal_places=1)
    electricity = models.DecimalField('Electricity', max_digits=10, decimal_places=1)
    gaz = models.DecimalField('Gaz', max_digits=10, decimal_places=1)
    pub_date = models.DateField('Publication date')


class Consumption(models.Model):
    class Meta():
        db_table = 'consumption'

    hot_water = models.DecimalField('Hot water', max_digits=10, decimal_places=1)
    cold_water = models.DecimalField('Cold water', max_digits=10, decimal_places=1)
    electricity = models.DecimalField('Electricity', max_digits=10, decimal_places=1)
    gaz = models.DecimalField('Gaz', max_digits=10, decimal_places=1)
    pub_date = models.DateField('Publication date')

