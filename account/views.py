from rest_framework.views import APIView
from .serializers import OTPSerializer, UserLoginSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
from .otp_verification_handler import OTPVerifcation
from .models import User
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

params=[openapi.Parameter(name="OTP",
                            required=True,
                            type="integer",
                            in_="path",
                            description="OTP to be verified")                           
]

# Create your views here.

'''
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class UserRegisterApiView(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    
class LoginUserApiView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)


    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        print(user)
        login(request, serializer.data)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return request.Response()

'''

@method_decorator(name="post", decorator=swagger_auto_schema(request_body=OTPSerializer))
class OTPAPIView(APIView):

    def post(self, *args, **kwargs):
        """Verify The Inputed OTP"""
       
        otp = self.request.data
        serializer = OTPSerializer(data=otp)
        serializer.is_valid(raise_exception=True)
        phone_number = self.kwargs.get("phone_number")
        try:
            user = User.objects.get(phone_number=phone_number)
        except:
            return Response({"error":"No user with this phone number"}, status=status.HTTP_404_NOT_FOUND)
        otp_response = OTPVerifcation(phone_number=phone_number, send=False)
        if otp_response.response.json()["verified"] == "True":
            user.phone_number_verify = True
            user.save()
            return Response(data=otp_response.json(), status=status.HTTP_202_ACCEPTED)
        return Response(data=otp_response.json(), status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """Send OTP to User"""
        number = kwargs.get("phone_number")
        otp_response = OTPVerifcation(phone_number=number, send=True)
        return Response(otp_response.response.json())
        