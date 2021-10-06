from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Users(models.Model):
    """"Modelo para los usuarios del sistema"""
    name = models.CharField(max_length=50)
    figerprint1 = ArrayField(models.IntegerField())
    figerprint2 = ArrayField(models.IntegerField())
    figerprint3 = ArrayField(models.IntegerField())
    figerprint4 = ArrayField(models.IntegerField())
    figerprint5 = ArrayField(models.IntegerField())
