
from enum import unique
from django.db import models
from django.forms import ValidationError
#from django.contrib.gis.db.models import PointField
from .choice import *
from django.db.models import Q 
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()



class Tour(models.Model):
    
    name = models.CharField(max_length=150, blank= False)
    start_date= models.DateField()
    end_date = models.DateField()
    location = models.OneToOneField('Location', on_delete=models.CASCADE)
    price = models.FloatField()
    #agent = models.ForeignKey('Agent')
    travel_option = models.CharField(choices=TRAVEL_CHOICE, max_length=30)

    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    state = models.CharField(max_length=40, choices=STATE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    
    class Meta:
        pass
        #unique_together = ["state", "city", "address"]

    def __str__(self) -> str:
        return f'{self.state} ({self.address})'

    def clean(self) -> None:
        '''
        for field in self._meta.fields:
            value = getattr(self, field.attname)
            if type(value) == str:
                #field.field_object = value.capitalize()
                self.__setattr__(str(field), value.capitalize)
                '''

        return super().clean()


class TransportPrice(models.Model):
    company = models.ForeignKey("TransportCompany", on_delete=models.CASCADE)
    from_location = models.ForeignKey(Location, related_name="from_loc", on_delete=models.CASCADE)
    to_location = models.ForeignKey(Location, related_name="to_loc" ,on_delete=models.CASCADE)
    car_type = models.CharField(choices=CAR_TYPE, max_length=100, default=1)#models.ForeignKey("CarType", on_delete=models.CASCADE)
    price = models.FloatField()

    class Meta:
        unique_together = ["from_location", "to_location", "company","car_type"]

    def __str__(self) -> str:
        return f"{self.company} {self.car_type} {self.from_location} to {self.to_location} {self.price}"
 

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    traveling_mode = models.CharField(max_length=59,choices=TRAVELING_CHOICE)
    date = models.DateField()
    time = models.TimeField()
    reserved_seats = models.IntegerField()
    from_location = models.ForeignKey(Location, related_name="from_location", on_delete=models.CASCADE)
    to_location = models.ForeignKey(Location, related_name="to_location" ,on_delete=models.CASCADE)
    transport_company = models.ForeignKey("TransportCompany", on_delete=models.CASCADE)
    car_type= models.CharField(choices=CAR_TYPE, max_length=50, default=1)#models.ForeignKey("TransportPrice", on_delete=models.CASCADE)
    
    price = models.FloatField(editable= False)
    paid = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.date}"

    def clean(self) -> None:
        try:
            price = TransportPrice.objects.get(from_location = self.from_location,
                                                to_location = self.to_location,
                                                car_type = self.car_type,
                                                company = self.transport_company
                                                                    ).price
        except:
            raise ValidationError("The price for this trip is not set")
        self.price = price * self.reserved_seats
        return super().clean()

    
class TransportCompany(models.Model):
    name = models.CharField(max_length=100)
    park = models.ManyToManyField(Location)
    lugage_policy = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"

   
'''
class CarType(models.Model):
    type = models.CharField(max_length=30)
    help_text = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.type}({self.help_text})"

'''

class Review(models.Model):
    content = models.TextField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.IntegerField(choices=INTEGER_CHOICE)
    company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{self.content}"

class TransactionTx(models.Model):
    date = models.DateField()
    tx_signed_val = models.CharField(max_length=100)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.CharField(choices=[("Successful","Successful"),
                                       ("Failed", "Failed"),
                                       ("None", "None")
                                       ], max_length=20, default="None", null=True)
    def __str__(self) -> str:
        return f"{self.tx_signed_val}"
