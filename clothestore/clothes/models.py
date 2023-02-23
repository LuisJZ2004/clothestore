from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist, FieldError

from brands.models import Brand

# Create your models here.

class ClothingType(models.Model):
    """
    clothing type, like 'shoes', 'shirts', 'pants' all that get in here
    """
    name = models.CharField(max_length=25, blank=False)
    slug = models.SlugField(editable=False)
    image = models.ImageField(null=False)
    gender = models.CharField(choices= (
        ('M','Man'),
        ('W', 'Woman'),
    ), max_length=10, blank=False)

    def __str__(self) -> str:
        return f"{self.gender} {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        try:
            ClothingType.objects.get(name=self.name, gender=self.gender, image=self.image)
            raise FieldError("Object already in data")
        except ObjectDoesNotExist:
            pass

        super().save(*args, **kwargs)


class Pledge(models.Model):
    # With 'pledge' I wanted to say 'clothe', this was because I had translated 'clothe' long time ago and 
    # I got 'pledge'. In the end it was too late. 
    
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE, null=True)
    clothing_type = models.ForeignKey(to=ClothingType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(choices= (
        ('M','Man'),
        ('W', 'Woman'),
    ), max_length=10, blank=False)
    description = models.TextField(max_length=1000, blank=False, null=True)

    def __str__(self) -> str:
        return self.name

class PledgeColorSet(models.Model):
    """
    Every clothe has several colors with different sizes and prices depending of the color, the PledgeColorSet
    is the final showed and sold product per se
    """
    pledge = models.ForeignKey(to=Pledge, on_delete=models.CASCADE)
    color = models.ForeignKey(to="Color", on_delete=models.CASCADE)

    price = models.FloatField(blank=False)
    image = models.ImageField(null=False)
    pub_date = models.DateTimeField(default=timezone.now())

    sizes = models.ManyToManyField(to="Size")

    def __str__(self) -> str:
        return f" '{self.pledge.name}' in color '{self.color.name}' "


class Size(models.Model):
    """
    Sizes of the clothes
    """
    name = models.CharField(max_length=4, unique=True, blank=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

class Color(models.Model):
    """
    Color of the clothes or anything that needs it
    """
    name = models.CharField(max_length=30, unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=False, null=True, editable=False)
    image = models.ImageField(null=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)