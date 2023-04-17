# Django
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

# My apps
from clothes.models import PledgeColorSet, IpAddress

def make_pagination(queryset: QuerySet, page_number: int, pagination_number: int):
    """
    Paginates a queryset
    """
    assert page_number != 0, "you can't paginate from zero"
    return queryset[pagination_number*(page_number-1):(pagination_number*(page_number-1)+pagination_number)]

def get_pagination_numbers(queryset: list, pagination_number: int):
    """
    How many pages a queryset is divided
    """
    final_number = 0
    i = 1
    while True:
        if make_pagination(queryset, i, pagination_number):
            final_number += 1
            i += 1
        else:
            break

    return final_number

def remove_duplicates(queryset: list):
    final_list = []

    for element in queryset:
        if element not in final_list:
            final_list.append(element)

    return final_list

def add_view(set: PledgeColorSet, remote_addr):
    """
    Add a view to a pledgeset using ip addresses
    """
    try:
        set.pledgecolorsetvisualisation_set.get(ip__ip_address=remote_addr)
    except ObjectDoesNotExist:
        try:
            ip = IpAddress.objects.get(ip_address=remote_addr)
        except ObjectDoesNotExist:
            ip = IpAddress.objects.create(ip_address=remote_addr)

        set.pledgecolorsetvisualisation_set.create(ip=ip)