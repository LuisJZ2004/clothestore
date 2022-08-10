from django.db import models
from django.utils.text import slugify

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=25, blank=False, unique=True, default="brand name")
    slug = models.SlugField(editable=False)
    image = models.ImageField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)