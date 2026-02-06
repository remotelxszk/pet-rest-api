from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="pets",
        on_delete=models.CASCADE,
    )
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default="")
    weight = models.FloatField()
    is_female = models.BooleanField()

    class Meta:
        ordering = ["added"]

class Cat(Pet):
    jump_height = models.FloatField()
    reacts_to_name = models.BooleanField()
    steals_food = models.BooleanField()
    is_orange_cat = models.BooleanField()
    
class Dog(Pet):
    does_fetch = models.BooleanField()
    knows_how_to_sit = models.BooleanField()

class Horse(Pet):
    speed = models.FloatField()
    is_race_horse = models.BooleanField()

class Rabbit(Pet):
    eats_carrots = models.BooleanField()