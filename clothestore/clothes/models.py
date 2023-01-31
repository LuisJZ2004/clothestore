from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from brands.models import Brand

# Create your models here.

class ClothingType(models.Model):
    name = models.CharField(max_length=25, blank=False, unique=True)
    slug = models.SlugField(editable=False)
    image = models.ImageField(null=False)
    gender = models.CharField(choices= (
        ('M','Man'),
        ('W', 'Woman'),
    ), max_length=10, blank=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Pledge(models.Model):
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE, null=True)
    clothing_type = models.ForeignKey(to=ClothingType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(choices= (
        ('M','Man'),
        ('W', 'Woman'),
    ), max_length=10, blank=False)
    pub_date = models.DateField(default=timezone.now().date())
    description = models.TextField(max_length=1000, blank=False, null=True)

    def __str__(self) -> str:
        return self.name

class PledgeColorSet(models.Model):
    pledge = models.ForeignKey(to=Pledge, on_delete=models.CASCADE)
    color = models.ForeignKey(to="Color", on_delete=models.CASCADE)

    price = models.FloatField(blank=False)
    image = models.ImageField(null=False)

    sizes = models.ManyToManyField(to="Size")

    def __str__(self) -> str:
        return f" '{self.pledge.name}' in color '{self.color.name}' "

class Size(models.Model):
    name = models.CharField(max_length=3, unique=True, blank=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

class Color(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    image = models.ImageField(null=False)

    def __str__(self) -> str:
        return self.name