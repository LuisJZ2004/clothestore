# Django
from django.test import TestCase

# My apps
from clothes.models import Size

# This app
from .clothes.functions import make_pagination

class MakePaginationTests(TestCase):

    def setUp(self) -> None:
        SIZES = (
            "x",
            "xx",
            "l",
            "xxl",
            "xl",
            "m",
            "40",
            "41",
            "44",
            "39",
        )

        for size in SIZES:
            Size.objects.create(name=size)

        self.sizes = Size.objects.all()
        return super().setUp()
    
    def test_sizes_pagination(self):
        sizes_list = list(self.sizes.order_by("name"))[0:5]
        self.assertEqual(list(make_pagination(self.sizes.order_by("name"),1,5)), sizes_list)

        half_sizes = list(self.sizes.order_by("name")[5:10])
        self.assertEqual(list(make_pagination(self.sizes.order_by("name"),2,5)), half_sizes)

        seven_sizes = list(self.sizes.order_by("name")[0:7])
        self.assertEqual(list(make_pagination(self.sizes.order_by("name"),1,7)), seven_sizes)

        print(self.sizes.order_by("name"))