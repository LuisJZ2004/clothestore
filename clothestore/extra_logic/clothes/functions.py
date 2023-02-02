from django.db.models import QuerySet

def make_pagination(queryset: QuerySet, page_number: int):
    assert page_number != 0, "you can't paginate from zero"
    return queryset[5*(page_number-1):(5*(page_number-1)+5)]