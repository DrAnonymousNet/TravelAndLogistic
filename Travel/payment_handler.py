from dataclasses import dataclass
import datetime
import json
import math
import random
import re
from urllib import response
from django.urls import reverse
from rest_framework.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, resolve_url
import requests
from django.core.cache import cache
from decouple import config
from .models import Ticket, TransactionTx
from .serializers import TransactionSerializer


import environ

env = environ.Env()

environ.Env.read_env()


@dataclass
class TicketPayment:
    ticket : Ticket = None
    request : HttpRequest = None
    link : str = None
    response : json = None
    def __post_init__(self):
        response = self.get_payment_link()
        #if link:
        #    self.link = link
        self.response = response
            

    
    def generate_tx(self):
        date = datetime.date.today()
        tx_val = "" + str(math.floor(1000000 + random.random()*90000000))
        tx = TransactionTx(ticket=self.ticket, tx_signed_val = tx_val, date = date)
        tx.save()
        return tx_val


    def get_flutterwave_data(self, url, headers={}, data = None):
        headers["Content-Type"] = 'application/json'
        headers["Authorization"] = config("FLUTTER_KEY")
        print(headers)
        response = requests.post(url, headers=headers, json=data )
        return response


    def assemble_payment_detail(self):
        user = self.ticket.user
        data = { "tx_ref": self.generate_tx() ,
                "amount": str(self.ticket.price),
                "currency""": "NGN",
                "redirect_url": reverse("ticket-payment-verify",kwargs = {"pk":self.ticket.id}), #f"http://127.0.0.1:8000/tickets/{self.ticket.id}/payment-verify",
                "meta": {
                    "consumer_id": f"{user.id}",

                },
                "customer": {
                    "email": str(user.email),
                    "phonenumber": str(user.phone_number),
                    "name": str(user._get_full_name())
                },
                "customizations": {
                    "title": "Pied Piper Payments",
                    "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
                }
            }
        return data

    def get_payment_link(self):
        #env = environ.Environ()
        #environ.Env.read_env()
        data = self.assemble_payment_detail()
        url ="https://api.flutterwave.com/v3/payments"
        response = self.get_flutterwave_data(url=url, data=data)
        #print(response.json())
        return response.json()
        


    

def verify_transaction(request, ticket):
    transaction_id = request.GET.get("transaction_id")
    url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
    headers = {}
    headers["Content-Type"] = 'application/json'
    headers["Authorization"] = config("FLUTTER_KEY")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        
        response = response.json()
        status = response.get("status")
        tx_ref = response["data"].get("tx_ref")
        amount = response["data"].get("amount")
        currency = response["data"].get("currency")
        if status == "successful":
            try:
                tx_obj = get_object_or_404(TransactionTx, {"tx_signed_val":tx_ref})
                tx_obj.status = 1
                tx_obj.save()
            except:
                return False
        elif status == "error":
            return False
        if currency != "NGN":
            return False
        expected_amount = ticket.price
        if amount != expected_amount:
            if amount > expected_amount:
                return True
            elif amount < expected_amount:
                return False
        return True
    return False
    

        



    
         

