# Django
from django.db.models import QuerySet

# My apps

class Filter:
    """
    Makes a new queryset from fields sended to filter.
    """
    def get_queryset_filtered(self, queryset: QuerySet, fields: dict, order: str | None):
        """
        It is just needed to invoque this method to make the filter.
        The arg 'field' needs to have in its keys the complete name of the query, for example: if you want 
        a brand from a respective clothe, you'd have to send 'brand__name' as the key, and then the value
        after the key
        The arg 'order' needs a name of the field in a string to order the queryset, it is optional
        """
        pass