# Django
from django.db import models

# My apps
from clothes.models import Pledge

class HomeSet(models.Model):
    name = models.CharField(max_length=60, unique=True, blank=False, null=False)

    pledges = models.ManyToManyField(to=Pledge)

    def __str__(self) -> str:
        return self.name