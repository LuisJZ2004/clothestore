from django.contrib import admin
from .models import ClothingType, Pledge, Brand, Color, Size, PledgeColorSet

# Register your models here.

admin.site.register(
    [
        ClothingType,
        Pledge,
        Brand, 
        Color, 
        Size, 
        PledgeColorSet
    ]
)