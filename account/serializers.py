
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer
from .otp_verification_handler import OTPVerifcation
User = get_user_model()

class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()



class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "password"]

    def perform_create(self, validated_data):
        phone_number  = validated_data.get("phone_number")
        id = validated_data.get("id")
    
        return super().perform_create(validated_data)
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, label = "Password")
    password2 = serializers.CharField(write_only = True, required = True, label = "Confirm Password")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "password2"]

    
    def validate_email(self, data):
        email = data
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise serializers.ValidationError("A User with this Email already exist !")
        return data

    def validate_password(self, value):
        initial = self.get_initial()
        password2 = str(initial.get("password2", None))
        password = value
        if len(password) < 8:
            raise serializers.ValidationError("Length of password should be 8 or more")
        if password.isalnum() and " " not in password:
            raise serializers.ValidationError("Password must contain a special character")
        if password.isalpha():
            raise serializers.ValidationError("Password must contain a Number")
        
        if password != password2:
            raise serializers.ValidationError("Password must match")
        return value

    def create(self, validated_data):
        username = validated_data["email"]
        password2 = validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data,username=username)
        user.set_password(password)
        user.save()
        return validated_data

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    #password = serializers.CharField(write_only=True, required = True)
    class Meta:
        model = User
        fields = ["email", "password"]
   


    def validate(self, data):
        email = data["email"]
        password= data["password"]
        if email and password:
            data["email"] = email.lower()
            user = authenticate(username=email.lower(), password=password)
            if not user:
                raise serializers.ValidationError("Either username or email is not correct")
            data["user"] = user
            
            return data
        else:
            raise serializers.ValidationError("Input both email and password")

