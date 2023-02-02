from django.db.models import QuerySet

def make_pagination(queryset: QuerySet, page_number: int, pagination_number: int):
    assert page_number != 0, "you can't paginate from zero"
    return queryset[pagination_number*(page_number-1):(pagination_number*(page_number-1)+pagination_number)]