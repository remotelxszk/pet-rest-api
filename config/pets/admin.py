from django.contrib import admin
from .models import Cat, Dog, Horse, Rabbit

# Register your models here.

admin.site.register(Cat)
admin.site.register(Dog)
admin.site.register(Horse)
admin.site.register(Rabbit)