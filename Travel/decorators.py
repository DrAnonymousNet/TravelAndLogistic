from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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