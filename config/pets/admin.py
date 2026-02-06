from django.contrib import admin
from .models import Pet, Cat, Dog, Horse

# Register your models here.

admin.site.register(Pet)
admin.site.register(Cat)
admin.site.register(Dog)
admin.site.register(Horse)