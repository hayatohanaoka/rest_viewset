from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Diary(models.Model):
    class Meta:
        ordering = ('pk',)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
