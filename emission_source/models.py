from django.db import models
from company.models import Country, BranchOffice


class UnitMeasurement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class GreenhouseGas(models.Model):
    name = models.CharField(max_length=100)
    unit_measurement = models.ForeignKey(UnitMeasurement, on_delete=models.RESTRICT)

class EmissionSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class EmissionFactor(models.Model):
    value = models.FloatField()
    emission_source = models.ForeignKey(EmissionSource, on_delete=models.RESTRICT)
    greenhouse_gas = models.ForeignKey(GreenhouseGas, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    created_at = models.DateTimeField('date published')

class HistoryEmissionFactor(models.Model):
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date published')
    
class CarbonFootprint(models.Model):
    value = models.FloatField()
    year = models.PositiveIntegerField()
    emission_source = models.ForeignKey(EmissionSource, on_delete=models.RESTRICT)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.RESTRICT)
    created_at = models.DateTimeField('date published')
    
