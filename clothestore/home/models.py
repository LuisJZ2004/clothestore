# Django
from django.db import models
from django.utils import timezone

# My apps
from clothes.models import Pledge

class HomeSet(models.Model):
    """
    Set of products that will be in the main page
    """
    name = models.CharField(max_length=60, unique=True, blank=False, null=False)
    pub_date = models.DateTimeField(default=timezone.now(), blank=False, null=False)

    pledges = models.ManyToManyField(to=Pledge)

    def __str__(self) -> str:
        return self.name