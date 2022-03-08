from django.db import models

class GreenhouseGas(models.Model):
    name = models.CharField(max_length=100)

class EmissionSource(models.Model):
    name = models.CharField(max_length=100)
    
class EmissionFactor(models.Model):
    created_at = models.DateTimeField('date published')

class HistoryEmissionFactor(models.Model):
    created_at = models.DateTimeField('date published')
    
class UnitMeasurement(models.Model):
    name = models.CharField(max_length=100)

class CarbonFootprint(models.Model):
    name = models.CharField(max_length=100)

