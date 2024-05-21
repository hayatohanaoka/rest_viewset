from django.db import models

# Create your models here.
class Facility(models.Model):
    class Meta:
        db_table = 'tbl_facilities'
    
    name = models.CharField(max_length=100)
    detail = models.TextField(max_length=500)

    def __str__(self):
        return self.name
