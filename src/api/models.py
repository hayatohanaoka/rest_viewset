from django.db import models

# Create your models here.
class Facility(models.Model):
    class Meta:
        db_table = 'tbl_facilities'
    
    name = models.CharField(max_length=100)
    detail = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    class Meta:
        db_table = 'tbl_equipments'
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name='equipments')

    def __str__(self):
        return f'{self.facility.name}: {self.nama}({self.quantity})'


class FacilityType(models.Model):
    class Meta:
        db_table = 'tbl_facility_types'
    type = models.CharField(max_length=100)
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name='facility_types')
    
    def __str__(self):
        return f'{self.facility.name}: {self.type}'
