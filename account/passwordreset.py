
from django.core.signing import Signer,TimestampSigner, SignatureExpired, BadSignature
from django.core import signing
from django.template import loader
from django.contrib import messages
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from urllib.parse import urlencode
from django.contrib.auth import get_user_model
from django.views import View
from django.core.mail import send_mail, EmailMessage

User = get_user_model()


def SendResetEmail(message:str, recipient:str):
    subject = "Reset Email Link"

    try:
        send_mail(subject=subject,
                message=message,
                recipient_list=[recipient],
                    fail_silently=False
                                )
    except:
        pass
    

def generate_token(email:str) -> str:
    signer = TimestampSigner()
    sign_val = signer.sign(email).split(":")
    token = sign_val[1] + sign_val[2]
    return token

def couple_token(email:str, token:str)->str:
    token = email+":"+token[:6] + ":"+ token[6:]
    return token
    

def verify_token(request:HttpRequest ,email:str , token:str) -> bool:

    signer = TimestampSigner()
    signed_value = couple_token(email,token)
    try:
        value = signer.unsign(signed_value, max_age=60)

    except SignatureExpired:
        messages.add_message(request,messages.INFO, "This link has expired")
        return False
    except BadSignature:
        messages.add_message(request,messages.INFO, "The link has been tampered with" )
        return False
    

    return True

def construct_link(request:HttpRequest, uuid:str ,token:str) -> str:
    full_url = f'{request.build_absolute_uri()}{uuid}/{token}'
    return full_url

# FORMS
from django import forms
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required= True)

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("new_password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Password must match !")
        return super().clean()

class ResetEmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailField)

    def clean_email(self, *args, **kwargs):
        super(ResetEmailForm, self).clean()
        email = self.cleaned_data.get('email')
        staff = User.objects.filter(email=email).first()

        if email is None:
            self._errors['email'] = self.error_class([
                'Email is required'])

        if staff is not None:
            if not staff.is_active:
                self._errors['email'] = self.error_class([
                    'This account is inactive, contact your company admin'])

        return email.lower()

# View
class PasswordReset(View):

    def get(self, request,email,token, *args, **kwargs):
        if verify_token(request,email,token):
            messages.add_message(request,messages.SUCCESS, "You can now change you password")
            reset_password_form = ResetPasswordForm()
            context = {
                "form":reset_password_form
            }
            template_name = "reset_password.html",
            return render(request,template_name,context)
        
        else:
            return redirect("password-reset-email")
    
    def post(self, request, email, uuid):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            staff = User.objects.get(email=email)
            password = reset_password_form.cleaned_data.get("password")
            staff.set_password(password)
            messages.add_message(request, messages.SUCCESS, "Your Password has been changed successfully, you can now login !")
            return redirect("account:login")
        else:
            if reset_password_form.errors:
                for field in reset_password_form:
                    for error in field.errors:
                        messages.add_message(request, messages.ERROR, error)
            return redirect(request.META.get("HTTP_REFERER"))

class PasswordResetEmailView(View):

    def get(self, request):
        template="account/password_reset_email.html"
        email_form = ResetEmailForm()
        context={
            "form":email_form
         }
        return render(request, template_name=template, context=context)

    def post(self, request):
        email_form  = ResetEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get("email")
            staff = User.objects.filter(email=email).first()
            if staff:
                token = generate_token(email)
                template_name = "account/resetemail.html"

                context = {
                    "link":construct_link(request, email, token)
                }
                message = loader.render_to_string(template_name, context, request)
                SendResetEmail(message, email)
                
                messages.add_message(request, messages.SUCCESS, "An verification link has been sent to your email")
        template="account/password_reset_email.html"
        context={
            "form":email_form
         }
        return render(request, template_name=template, context=context)

# ERRORS



                
                
            
            




        
        

        

