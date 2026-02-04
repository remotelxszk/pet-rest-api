from django.db import models

class Pet(models.Model):
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
    doesFetch = models.BooleanField()
    knowsHowToSit = models.BooleanField()


class Horse(Pet):
    speed = models.FloatField()
    is_race_horse = models.BooleanField()