# Python
import operator
import collections
from functools import reduce

# Django
from django.db.models import QuerySet, Q
from django.core.exceptions import FieldError

# My apps
from clothes.models import PledgeColorSet

# this app
from .functions import remove_duplicates

class Filter:
    """
    Makes a new queryset from fields sended to filter.
    """

    def __are_fields_filled(self, fields: dict):
        """
        returns if a dict with fields is filled or not
        """
        for field in fields.values():
            if field:
                return True
        return False

    def __get_Q_queries_in_AND(self, fields: dict):
        """
        returns a Q object with the complete Q query necesary to filter the queryset, with AND operator
        """
        if self.__are_fields_filled(fields):
            Qs = [Q( (field, fields[field]) ) for field in fields.keys() if fields[field]]

            return reduce(operator.and_, Qs)

        raise ValueError("It cannot make a queryset with empty fields")


    def get_queryset_filtered(self, queryset: QuerySet, fields: dict, order=None):
        """
        It is just needed to invoque this method to make the filter.
        The arg 'fields' needs to have in its keys the complete name of the query, for example: if you want 
        a brand from a respective clothe, you'd have to send 'brand__name' as the key, and then the value
        after the key
        The arg 'order' needs a name of the field in a string to order the queryset, it is optional
        """
        if self.__are_fields_filled(fields=fields):
            if order:
                try:
                    return queryset.filter(self.__get_Q_queries_in_AND(fields)).order_by(order)
                except FieldError:
                    pass
            return queryset.filter(self.__get_Q_queries_in_AND(fields)).order_by("-pub_date")
        elif order:
            return queryset.order_by(order)
        else:
            return queryset


# No scalable
class QuantityOfAField:
    """
    logic to pick how many products with X fields are in a queryset
    Example:
        if there are three sets in color blue, two in color green and another in yellow, plus their sizes
        the result would be like this
        {
            "colors":{
                "blue": 3,
                "green": 2,
                "yellow": 1
            },
            "sizes": {
                "X": 1,
                "L": 4,
                "XXL": 1
            }
        }
        This class is not scalable, it only works to filter sets in this project. It can be taken as
        reference but not copy paste
    """
    
    def __get_list_with_repeated_color_names(self, sets: QuerySet, selected_color, selected_size):
        """
        Receives a queryset of pledgecolorsets and returns a list with all the color names the sets have
        """
        # pledge_color_sets = self.__get_pledgecolorset_instances(sets, selected_color, selected_size)
        return  [set.color.name for set in sets]

    def __get_color_names_counter(self, sets: QuerySet, selected_color, selected_size):
        """
        Returns a counter with all the names of the colors in the pledgecolorsets
        """
        return dict(collections.Counter(self.__get_list_with_repeated_color_names(sets, selected_color, selected_size)))

    ############################### 
    # Getting sizes
    def __get_size_names(self, sizes: QuerySet):
        """
        Receives a queryset of sizes and returns their names in a list 
        """
        return [instance.name for instance in sizes]

    def __get_complete_list_with_repeated_size_names(self, sets: QuerySet, selected_color, selected_size):
        """
        It returns an extended list with all the repeated sizes names.
        """
        final_list = []

        for set in sets:
            final_list.extend(
                self.__get_size_names(set.sizes.all())
            )
        return final_list

    def __get_size_names_counter(self, sets: QuerySet, selected_color, selected_size):
        """
        Returns a counter with all the names of the sizes in the pledgecolorsets
        """
        return dict(collections.Counter(self.__get_complete_list_with_repeated_size_names(sets, selected_color, selected_size)))
    
    def get_quantity_of_each_field(self, queryset: QuerySet, selected_color: str | None, selected_size: str | None) -> dict:   
        return {
            "colors": self.__get_color_names_counter(queryset, selected_color, selected_size),
            "sizes": self.__get_size_names_counter(queryset, selected_color, selected_size),
        }