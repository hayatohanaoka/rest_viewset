from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TODO(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_tasks'


class Column(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_columns'
