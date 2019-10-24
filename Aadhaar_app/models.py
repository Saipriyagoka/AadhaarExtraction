from django.db import models

# Create your models here.
class Aadhaar_detail(models.Model):
    name              = models.CharField(max_length = 264 ,null=True)
    year_of_birth     = models.CharField(max_length = 264 , null=True)
    gender            = models.CharField(max_length = 264 , null=True)
    Aadhaar_num       = models.IntegerField(default=0)
    Aadhaar_Image     = models.ImageField(upload_to='Aadhaar_images/')
    image_name        = models.CharField(max_length = 264,default='')

    def __str__(self):
        return self.image_name
