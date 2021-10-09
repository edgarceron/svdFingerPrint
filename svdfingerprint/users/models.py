from django.db import models
from django.contrib.postgres.fields import ArrayField
from numpy import empty

# Create your models here.
class Users(models.Model):
    """"Modelo para los usuarios del sistema"""
    name = models.CharField(max_length=50)
    figerprints1 = ArrayField(ArrayField(models.IntegerField()))
    figerprints2 = ArrayField(ArrayField(models.IntegerField()))
    figerprints3 = ArrayField(ArrayField(models.IntegerField()))
    figerprints4 = ArrayField(ArrayField(models.IntegerField()))
    figerprints5 = ArrayField(ArrayField(models.IntegerField()))

class Config(models.Model):
    key = models.CharField(max_length=30, null=False)
    value = models.CharField(max_length=255, null=False)


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class UploadImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)

