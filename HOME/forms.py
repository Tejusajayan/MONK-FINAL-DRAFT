from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django import forms

class userform(UserCreationForm):
    mobile=forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex = r'^(0)?[6-9]\d{9}$',
                code='Invalid Mobile Number'
            )
        ]
    )
    class Meta:
        model=User
        fields=['username','email','password1','password2','is_active','mobile','is_staff']

class shippdet(forms.Form):
    number=forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex = r'^(0)?[6-9]\d{9}$',
                message='Invalid Mobile Number'
            )
        ]
    )
    name = forms.CharField(max_length=100)
    doorno_street_area = forms.CharField(max_length=200)
    landmark = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=6)