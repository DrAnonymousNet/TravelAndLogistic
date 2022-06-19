from dataclasses import dataclass
from django.shortcuts import get_object_or_404, redirect, resolve_url
import requests
from django.core.cache import cache


import environ

env = environ.Env()

environ.Env.read_env()
'''
def AddJwtHeaderMiddleware(get_response):
    
    def middleware(request):
        if "login" not in str(request.get_full_path()):
            access_token = cache.get(request.session.get("username"))
            print("This" , access_token)
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
            #print(request.META)

            response = get_response (request)
            response["Authorization"] = f"Bearer {access_token}"
            return response
        response = get_response(request)
        return response
    return middleware
 '''         

def login(request, user_data):
    base_url = request.get_host()
    url = resolve_url('token_obtain_pair')
    full_url = f"http://{base_url}{url}"
    response = requests.post(full_url, json=user_data)
    
    print(type(response.status_code))
    if response.status_code == 200:
        request.session.get("username",user_data["username"])
        print(request.session.get("username"))
        token = response.json()["access"]
        
        cache.set(request.session["username"], token)

        print(cache.__getattribute__)
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return request

def logout(request):
    username = request.session.get("username")
    cache.delete(username)

@dataclass    
class OTPVerifcation:
    send : bool = True
    phone_number : str =""
    otp: str = ""
    response : requests.Response = None
    def __post_init__(self):
        self.phone_number = self.processnumber()
        print(self.phone_number)
        if self.send:
            response = self.send_otp()
        else:
            response = self.verify_otp()
        print(response.json(), "ckjckckcokc")
        self.response = response

    def send_otp(self):
        
        pay_load = self.generate_payload()
        url = "https://api.ng.termii.com/api/sms/otp/send"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url,headers=headers, json=pay_load)
        return response
    
    def verify_otp(self):
        url = "https://api.ng.termii.com/api/sms/otp/verify"
        payload = self.generate_payload()
        headers = {
        'Content-Type': 'application/json',
            }
        response = requests.post(url, headers=headers, json=payload)
        return response

    def generate_payload(self):
    
        payload = {
            "api_key" : env("TERMI_KEY"),
            "message_type" : "NUMERIC",
            "to" : self.phone_number,
            "from" : "Travel",
            "channel" : "generic",
            "pin_attempts" : 10,
            "pin_time_to_live" :  5,
            "pin_length" : 6,
            "pin_placeholder" : "<1234>",
            "message_text" : f"Your OTP is ",
            "pin_type" : "NUMERIC"
        }
        if not self.send:
            payload = {
             "api_key": env("TERMI_KEY"),
                "pin_id": "NUMERIC",
                "pin": self.otp,
                          }
        return payload

    def processnumber(self):
        phone_number = "+234" + self.phone_number[1:]
        return phone_number

'''
def genrate_otp(self):
        hotp = pyotp.HOTP('base32secret3232')
        return hotp.at(self.user_id)

def verify_otp(self, input_otp):
    hotp = pyotp.HOTP('base32secret3232')
    if input_otp == hotp.at(self.user_id):
        return True
    return False
'''