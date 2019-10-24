# forms.py
from django import forms
from .models import *

class AadhaarForm(forms.ModelForm):

    class Meta:
        model = Aadhaar_detail
        fields = ['Aadhaar_Image']
