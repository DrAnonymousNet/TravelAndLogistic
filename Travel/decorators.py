
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

def swagger_multiple_wrapper(name, description, serializer=None):
    def inner_func(*args, **kwargs):
        print(kwargs, args)
        return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name=name,
                            required=True,
                            type="integer",
                            in_="path",
                            description=description)
        ],
        
        request_body=serializer)
    return inner_func


def FilterSearchPaginate(filterset_fields=None, search_fields=None):
    class decorator:
        def __init__(self, cls) -> None:
            self.cls = cls
            self.cls.filter_backends = [DjangoFilterBackend, SearchFilter]
            self.cls.filterset_fields=filterset_fields
            self.cls.search_fields = search_fields
            self.cls.pagination_class = LimitOffsetPagination
        def __call__(self, *args, **kwds):
            def wrapper(*args, **kwds):
                return self.cls
            return wrapper
        def as_view(self, *args,**kwargs):
            return self.cls.as_view(*args,**kwargs)
    return decorator