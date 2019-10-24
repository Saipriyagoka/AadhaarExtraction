from rest_framework import serializers
from Aadhaar_app.models import Movie_detail

class AadhaarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aadhaar_detail
        fields = '__all__'
