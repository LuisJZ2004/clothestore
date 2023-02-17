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
            # tuples_in_Qs = []

            # for field in fields.keys():
            #     if fields[field]:
            #         tuples_in_Qs.append(
            #             (field, fields[field],)
            #         )
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
            return queryset.filter(self.__get_Q_queries_in_AND(fields))
        elif order:
            return queryset.order_by(order)
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
        This class is not scalable, it only works to filter pledges in this project. It can be taken as
        reference but not copy paste
    """
    def __get_pledgecolorset_instances(self, pledges: QuerySet, selected_color: str | None, selected_size: str | None):
        """
        Gets all the PledgeColorSet from a sended queryset with pledges. This is the main class we will need to
        get the final result.
        It returns a list with all the PledgeColorSet querysets 
        """
        
        instances_list = []
        
        # We'll consider a selected_size and selected_color picked by the user and It makes queries in base to
        # that
        if selected_size and selected_color:
            for pledge in pledges:
                instances_list.append(
                    pledge.pledgecolorset_set.filter(sizes__name=selected_size, color__name=selected_color)
                )
            
        elif selected_size:
            for pledge in pledges:
                instances_list.append(
                    pledge.pledgecolorset_set.filter(sizes__name=selected_size)
                )
        elif selected_color:
            for pledge in pledges:
                instances_list.append(
                    pledge.pledgecolorset_set.filter(color__name=selected_color)
                )
        else:
            for pledge in pledges:
                instances_list.append(
                    pledge.pledgecolorset_set.all()
                )
        return instances_list

    # Getting colors

    def __get_color_names(self, pledge_color_set: list):
        """
        Receives a list of PledgeColorSet querysets and returns a list with all the names of the colors in the
        PledgeColorSets. It is an independant method, doesn't need any other method to work
        """
        return [instance.color.name for instance in pledge_color_set]

    def __get_complete_list_with_repeated_color_names(self, pledges: QuerySet, selected_color, selected_size):
        """
        Receives a pledges queryset, selected_color and selected_size. First it gets the pledgecolorsets with the 
        method "__get_pledgecolorset_instances()" than, with the method "__get_color_names()" it'll send each 
        pledgecolorset to get all their names in a list, and last it will extend the names into a final_list to return
        it, no matter the repeated name
        """
        pledge_color_sets = self.__get_pledgecolorset_instances(pledges, selected_color, selected_size)
        final_list = []

        for set in pledge_color_sets:
            final_list.extend(
                self.__get_color_names(set)
            )
        return final_list

    def __get_color_names_counter(self, pledges: QuerySet, selected_color, selected_size):
        """
        Returns a counter with all the names of the colors in the pledgecolorset gotten, with the times their
        are in total through all the sets
        """
        return dict(collections.Counter(self.__get_complete_list_with_repeated_color_names(pledges, selected_color, selected_size)))
    ############################### 
    # Getting sizes
    def __get_size_names(self, sizes: QuerySet):
        """
        Receives a list of sizes querysets and returns a list with all the names of the sizes in the
        queryset. It is an independant method, doesn't need any other method to work
        """
        return [instance.name for instance in sizes]

    def __get_pledgecolorset_instances_separated(self, pledgecolorsets_list: list):
        """
        Receives a list of pledgecolorset querysets, it goes through all the list getting each queryset, turns 
        them in list and extends it in a final list in order to have them separated and return. It is an independant method, 
        doesn't need any other method to work
        """
        final_list = []
        for instance in pledgecolorsets_list:
            final_list.extend(
                list(instance)
            )
        return final_list

    def __get_pledgecolorset_sizes(self, pledges: QuerySet, selected_color, selected_size):
        """
        Receives a pledge queryset, selected_color and selected_size. First it gets pledgecolorset instances, 
        with its received args, than it separates the queryset with the method "__get_pledgecolorset_instances_separated()"
        last, returns a list with the querysets of the sizes in each pledgecolorser
        """
        pledgecolorsets = self.__get_pledgecolorset_instances(pledges, selected_color, selected_size)
        colorsets = self.__get_pledgecolorset_instances_separated(pledgecolorsets)
        
        final_pledge_sizes = {}
        for colorset in colorsets:
            if final_pledge_sizes.get(colorset.pledge.pk):
                final_pledge_sizes[colorset.pledge.pk].extend(list(colorset.sizes.all()))
            else:
                final_pledge_sizes[colorset.pledge.pk] = list(colorset.sizes.all())
        
        for pledge_primary_key, size_list in final_pledge_sizes.items():
            final_pledge_sizes[pledge_primary_key] = remove_duplicates(size_list)

        return  final_pledge_sizes.values()

    def __get_complete_list_with_repeated_size_names(self, pledges: QuerySet, selected_color, selected_size):
        """
        It returns an extended list with all the repeated sizes names. First gets a list with the sizes querysets,
        than it turns each one in a list to extend them in the end 
        """
        sizes = self.__get_pledgecolorset_sizes(pledges, selected_color, selected_size)
        final_list = []

        for size in sizes:
            final_list.extend(
                self.__get_size_names(size)
            )
        return final_list

    def __get_size_names_counter(self, pledges: QuerySet, selected_color, selected_size):
        return dict(collections.Counter(self.__get_complete_list_with_repeated_size_names(pledges, selected_color, selected_size)))
    
    def get_quantity_of_each_field(self, queryset: QuerySet, selected_color: str | None, selected_size: str | None) -> dict: 
        
        
        return {
            "colors": self.__get_color_names_counter(queryset, selected_color, selected_size),
            "sizes": self.__get_size_names_counter(queryset, selected_color, selected_size),
        }