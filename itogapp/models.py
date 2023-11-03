from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe_category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    
    
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    cooking_time = models.CharField(max_length=100)
    picture = models.ImageField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
     
      
class Relationship_of_recipe_and_category(models.Model):
    cat = models.ForeignKey(Recipe_category, on_delete=models.CASCADE)
    rec = models.ManyToManyField(Recipe)
    

    

    


