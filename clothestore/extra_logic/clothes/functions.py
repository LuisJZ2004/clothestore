from django.db.models import QuerySet

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