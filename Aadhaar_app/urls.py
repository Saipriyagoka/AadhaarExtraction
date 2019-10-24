from django.urls import path
from Aadhaar_app.views import *


app_name = 'Aadhaar_app'

urlpatterns=[
    path('Image_upload', Image_upload, name = 'Image_upload'),
    path('AadhaarList/(?P<pk1>\w+)/(?P<pk2>\w+)/$', AadhaarList, name = 'AadhaarList'),
    path('Pass_info/<int:pk>/', Pass_info, name = 'Pass_info'),
    path('Try_again', Try_again, name = 'Try_again'),
]
