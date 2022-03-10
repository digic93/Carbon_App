from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

class Sector (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Company(models.Model):
    name = models.CharField(max_length=100)
    nit = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    sector = models.ForeignKey(Sector, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('date published')

class BranchOffice (models.Model):
    name = models.CharField(max_length=100)
    Observation = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    created_at = models.DateTimeField('date published')
