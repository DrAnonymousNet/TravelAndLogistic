from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import jwt
from rest_framework import serializers


# Create your models here.


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)



class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not phone_number:
            raise ValueError("User must have a phone number")
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,**kwargs
        )
        print(kwargs)

        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,**kwargs
        )
        user.staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
            """
            Creates and saves a staff user with the given email and password.
            """
            user = self.create_user(
                email,
                password=password,
            )
            user.staff = True
            user.save(using=self._db)
            return user


    def create_testuser(self, email, password, kwargs = {"phone_number":"08058755200",
                                                           "firstname":"Ahmad", "lastname":"Ayo"     
                                                                   }):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,**kwargs
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not phone_number:
            raise ValueError("User must have a phone number")
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,**kwargs
        )
        print(kwargs)

        user.set_password(password)
        
        user.save(using=self._db)
        return user




class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = models.CharField(blank= False, max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    phone_number_verify = models.BooleanField(default=False)
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone_number", "firstname", "lastname"] # Email & Password are required by default.

    def _get_full_name(self):
        return f"{self.firstname} {self.lastname}"


    def __str__(self):
        return self._get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def full_name(self):
        return self._get_full_name
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    

