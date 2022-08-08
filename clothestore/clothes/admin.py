from django.contrib import admin
from .models import ClothingType, Pledge, Brand

# Register your models here.

admin.site.register(
    [
        ClothingType,
        Pledge,
        Brand
    ]
)