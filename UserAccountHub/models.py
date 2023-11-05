from django.db import models
from django.utils import timezone






class DateTimeUTCField(models.DateTimeField):
    def pre_save(self):
        return timezone.now()

# Create your models here.
class User ():

    Status_Choices = [
        (0,"Active"),
        (1 ,"In Active"),
        (2, "Suspended")
    ]

    Gender_Choices =[
        (0 ,"Male"),
        (1,"Female")
    ]


    id = models.AutoField(primary_key=True)
    server_DateTime = models.DateTimeField(auto_now=True)
    DateTime_UTC =models.DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    Update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    username = models.CharField(max_length=60 ,unique=True)
    email =models.EmailField (verbose_name="email" ,max_length=180,unique=True) 
    #Django's default behavior is to use UTF-8 encoding, which is suitable for handling Unicode characters and siutablle for "NVARCHAR" stands for "National Variable Character.
    firstName =models.CharField(max_length= 40)
    lastName = models.CharField (max_length=60)
    status =models.IntegerField(choices = Status_Choices ,default=0 )
    gender = models.IntegerField (choices=Gender_Choices ,default=0)
    date_of_Birth = models.DateTimeField ()
    


class Account (models.Model):
    id = models.AutoField (primary_key=True)
    server_DateTime = models.DateTimeField(auto_now=True)
    dateTime_UTC =models.DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    
