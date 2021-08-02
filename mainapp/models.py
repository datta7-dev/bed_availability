# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Hospitaldata(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_name = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    area_code = models.CharField(max_length=10)
    contact = models.BigIntegerField()
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=20)

    def __int__(self):
        return self.hospital_id

    class Meta:
        managed = True
        db_table = 'hospitaldata'


class Facility(models.Model):
    hospital = models.ForeignKey(
        'Hospitaldata', db_column='hospital_id', on_delete=models.CASCADE)
    total_oxygen_bed = models.IntegerField()
    available_oxygen_bed = models.IntegerField()
    total_general_bed = models.IntegerField()
    available_general_bed = models.IntegerField()
    updated_on = models.DateTimeField()

    def __int__(self):
        return self.hospital

    class Meta:
        managed = True
        db_table = 'facility'
