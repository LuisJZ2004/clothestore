# Python
import operator
import collections
from functools import reduce

# Django
from django.db.models import QuerySet, Q
from django.core.exceptions import FieldError

# My apps
from clothes.models import PledgeColorSet

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
            Qs = []

            for field in fields.keys():
                if fields[field]:
                    Qs.append(
                        Q((field, fields[field]))
                    )
            
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

            return queryset.filter(self.__get_Q_queries_in_AND(fields))
        else:
            return queryset


# No scalable
class QuantityOfAField:
    """
    logic to pick how many products with X fields are in a queryset
    Example:
        if there are three pledges in color blue, two in color green and another in yellow, plus their sizes
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
    """

    def __get_pledgecolorset_instances(self, pledges: QuerySet):
        instances_list = []
        
        for pledge in pledges:
            instances_list.append(
                pledge.pledgecolorset_set.all()
            )
        return instances_list

    # def __get_instances_counter(self, pledges: QuerySet):
    #     return dict(collections.Counter(self.__get_pledgecolorset_instances(pledges)))

    def __get_color_names(self, pledge_color_set: list):
        names_list = []
        
        for instance in pledge_color_set:
            names_list.append(
                instance.color.name
            )
        return names_list

    def __get_complete_list_with_repeated_color_names(self, pledges: QuerySet):
        pledge_color_sets = self.__get_pledgecolorset_instances(pledges)
        final_list = []

        for set in pledge_color_sets:
            final_list.extend(
                self.__get_color_names(set)
            )
        return final_list

    def __get_color_names_counter(self, pledges: QuerySet):
        return dict(collections.Counter(self.__get_complete_list_with_repeated_color_names(pledges)))

    def get_quantity_of_each_field(self, queryset: QuerySet):        
        return self.__get_color_names_counter(queryset)