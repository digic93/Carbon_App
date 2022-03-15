from django.db import models
from django.utils import timezone
from company.models import Country, BranchOffice

class TypeUnitMeasurement(models.Model):
    name = models.CharField(max_length=300, unique=True )

class UnitMeasurement(models.Model):
    name = models.CharField(max_length=100, unique=True )
    unit = models.CharField(max_length=100, unique=True )
    type_unit = models.ForeignKey(TypeUnitMeasurement, on_delete=models.CASCADE)
    description = models.TextField()

class GreenhouseGas(models.Model):
    name = models.CharField(max_length=100, unique=True)

class EmissionSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

class EmissionFactor(models.Model):
    value = models.FloatField()
    emission_source = models.ForeignKey(EmissionSource, on_delete=models.RESTRICT)
    greenhouse_gas = models.ForeignKey(GreenhouseGas, on_delete=models.RESTRICT)
    unit_measurement = models.ForeignKey(UnitMeasurement, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        date_now = timezone.now()

        if self.created_at is None:
            self.created_at = date_now

        self.updated_at = date_now
        
        super().save(*args, **kwargs)
        
        HistoryEmissionFactor.objects.create(
            value = self.value,
            emission_factor = self,
            created_at = date_now
        )


class HistoryEmissionFactor(models.Model):
    value = models.FloatField()
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    

class CarbonFootprint(models.Model):
    value = models.FloatField()
    year = models.PositiveIntegerField()
    emission_source = models.ForeignKey(EmissionSource, on_delete=models.RESTRICT)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.RESTRICT)
    created_at = models.DateTimeField('date published')
    
