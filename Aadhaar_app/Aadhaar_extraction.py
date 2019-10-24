from urllib.request import urlretrieve
from urllib.error import HTTPError
import pandas as pd
import numpy as np
from pytesseract import image_to_string
import cv2
import os
import face_recognition


def process(image):
    #black and white image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #extracting text from geay image using image_to_string
    temp=image_to_string(gray,lang='eng')
    #creating list from extracted text
    extrated_list =temp.split('\n\n')
    extrated_list =temp.split('\n')
    #removing white space
    extrated_list = [x.replace(' ', '') for x in extrated_list]
    extrated_list = [i for i in extrated_list if i]
    return extrated_list

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def extract_info(image,ex_dict):
    extrated_list=process(image)
    #Gender
    for i in extrated_list:
        if ('MALE') in i:
            ex_dict['Gender'] = 'MALE'
        elif ('Male') in i:
            ex_dict['Gender'] = 'Male'

    #DOB
    for i in extrated_list:
        if ('DOB:') in i:
            DOB = i[i.index('DOB:'):]
            DOB = list(DOB.split(':'))
            ex_dict['Date_of_birth']=DOB[1]
        elif ('YearofBirth') in i:
            DOB = i[i.index('YearofBirth'):]
            if ':' in DOB:
                DOB = list(DOB.split(':'))
                ex_dict['Date_of_birth']=DOB[1]
            elif ';' in DOB:
                DOB = list(DOB.split(';'))
                ex_dict['Date_of_birth']=DOB[1]

    #Aadhaar
    if ex_dict['Gender']:
        for i in extrated_list:
            if (ex_dict['Gender']) in i:
                index = extrated_list.index(i)+1
                while index <= len(extrated_list)-1:
                    req = extrated_list[index]
                    #if aadhar is mixed with some char
                    if hasNumbers(req):
                        rl = list(req)
                        temp = ("".join(list(filter(lambda x : (x.isdigit()) ,rl))))
                        if len(temp)==12:
                            ex_dict['Aadhaar_Number']= temp
                    #not mixed up with char
                    elif req.isdigit():
                        ex_dict['Aadhaar_Number']= req
                    index+=1
            if ('YourAadhaarNo') in i:
                num=extrated_list[extrated_list.index(i)+1]
                ex_dict['Aadhaar_Number']=num

    #Name
    if ex_dict['Date_of_birth']:
        for i in extrated_list:
            if (ex_dict['Date_of_birth']) in i:
                req = extrated_list.index(i)-1
                ex_dict['Name']= extrated_list[req]
    return ex_dict

def brighten(image,ex_dict):
    alpha=2
    for beta in range(0,-500,-25):
        bright_image=cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)
        ex_dict=extract_info(bright_image,ex_dict)
        if any(x == None for x in ex_dict.values()):
            continue
        else:
            break
    return ex_dict

def rotate(image,file):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ## (2) threshold
    adap_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 5)
    ## (3) minAreaRect on the nozeros
    pts = cv2.findNonZero(adap_thresh)
    ret = cv2.minAreaRect(pts)
    (cx,cy), (w,h), ang = ret
    if h>w:
        h,w = w,h
        ang += 90
    ## (4) Find rotated matrix, do rotation
    M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
    rotated_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    out_path = r"C:\Users\saipriya\Desktop\Priya\ImageProcessing\Aadhaar_Card\After_rotate"
    cv2.imwrite(os.path.join(out_path,file+'.jpg'), rotated_image)
    return rotated_image
    #found = face_search(rotated_image)
    #if not found:
     #   rotate(rotated_image,file)

def face_search(image):
    #searching for the face
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    facecascade = cv2.CascadeClassifier(r'C:\Users\saipriya\opencv\data\haarcascades_cuda\haarcascade_frontalface_default.xml')
    faces = facecascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    return len(faces)
