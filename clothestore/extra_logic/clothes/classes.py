# Django
from django.db.models import QuerySet

# My apps

class Filter:
    def get_queryset_filtered(self, queryset: QuerySet, fields: dict):
        pass