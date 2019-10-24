from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Aadhaar_detail
from .forms import *
from Aadhaar_app.Aadhaar_extraction import *

import urllib
import pandas as pd
import numpy as np
from pytesseract import image_to_string
import cv2
import os
import face_recognition

# Create your views here.
def index(request):
    return render(request , 'Aadhaar_app/search.html')

def AadhaarList(request):
    if request.method == 'POST':
        file = request.FILES['Aadhaar_Image']
        filename = file.name.split('.')[0]
        #Build a numpy array using the uploaded data. Decode this array using cv2.
        image = cv2.imdecode(np.fromstring(file.read(), dtype="uint8"), cv2.IMREAD_UNCHANGED)
        keyList = ["Name", "Date_of_birth" , "Gender" , "Aadhaar_Number"]
        ex_dict={key: None for key in keyList}
        final_dict=brighten(image,ex_dict)
        if final_dict['Aadhaar_Number']:
            Aadhaar_detail.objects.get_or_create(name=final_dict['Name'] , year_of_birth=final_dict['Date_of_birth'] , gender=final_dict['Gender'] , Aadhaar_num=final_dict['Aadhaar_Number'] ,Aadhaar_Image = file, image_name = filename)[0]
            return redirect('Pass_info' , pk = final_dict['Aadhaar_Number'])
        else:
            return redirect('Try_again')
    return render(request, 'Aadhaar_app/search.html')

def Pass_info(request,pk):
    details = Aadhaar_detail.objects.filter(Aadhaar_num = pk)
    if request.method == 'POST':
        return redirect('AadhaarList')
    else:
        return render(request, 'Aadhaar_app/search.html', {"details" : details} )

def Try_again(request, template_name='Aadhaar_app/search.html'):
    args = {}
    text = "Please upload a high quality Picture...."
    args['mytext'] = text
    return TemplateResponse(request, template_name, args)

