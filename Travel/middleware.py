from dataclasses import dataclass
import re
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

def GetCurrentUserMiddleware(get_response):
    
    def middleware(request):
        user = get_current_user(request)
        if user:
            request.user = user
        print(request.user)
        
        return get_response(request)

    return middleware


def get_current_user(request):
    user = None
    try:
        curr_auth = JWTAuthentication()
        header = curr_auth.get_header(request)
        print(header)
        raw_token= curr_auth.get_raw_token(header)
        print(raw_token)
        validated_token = curr_auth.get_validated_token(raw_token)
        user = curr_auth.get_user(validated_token)
        print(user)
    except:
        print("hmmm")

    return user

