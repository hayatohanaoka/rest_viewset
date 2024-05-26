from django.db import models

from user.models import CustomUser

# Create your models here.
class Recipe(models.Model):
    class Meta:
        db_table = 'tbl_recipes'
    
    title = models.CharField(max_length=100)
    instruction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')


class Ingredient(models.Model):
    class Meta:
        db_table = 'tbl_ingredients'
    
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='quantities')
