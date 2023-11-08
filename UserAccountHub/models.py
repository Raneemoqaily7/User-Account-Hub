from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator






class DateTimeUTCField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

# Create your models here.
class User (models.Model):

    User_Status_Choices = [
        (0,"Active"),
        (1 ,"In Active"),
        (2, "Suspended"),
        (3 ,"Deleted")
    ]

    Gender_Choices =[
        (0 ,"Male"),
        (1,"Female")
    ]


    id = models.AutoField(primary_key=True)
    server_DateTime = models.DateTimeField(auto_now=True)
    DateTime_UTC =DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    Update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    username = models.CharField(max_length=60 ,unique=True)
    email =models.EmailField (verbose_name="email" ,max_length=180,unique=True) 
    #Django's default behavior is to use UTF-8 encoding, which is suitable for handling Unicode characters and siutablle for "NVARCHAR" stands for "National Variable Character.
    firstName =models.CharField(max_length= 40)
    lastName = models.CharField (max_length=60)
    status =models.IntegerField(choices = User_Status_Choices ,default=0 )
    gender = models.IntegerField (choices=Gender_Choices ,default=0)
    date_of_Birth = models.DateTimeField ()

    is_admin =models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS =["username"]

    def __str__(self) :
        return self.username


class Account (models.Model):
    Currency_Choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('JOD' ,'Jordanian Dinar')
    ]
    Account_Status_Choices =[
        (0 ,"Active"),
        (1,"In Active"),
        (2 ,"Suspended"),
        (3 ,"Deleted")
    ]
    id = models.AutoField (primary_key=True)
    user_id = models.ForeignKey(User ,on_delete=models.CASCADE)
    server_DateTime = models.DateTimeField(auto_now=True)
    dateTime_UTC =DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    accountNumber =models.CharField (max_length=30)
    balance =models.DecimalField(max_digits=7 ,decimal_places=2 ,validators=[MinValueValidator(0.01)])
    currency = models.CharField(choices=Currency_Choices ,max_length=15, default="USD")

    status = models.IntegerField (choices=Account_Status_Choices ,default = 0)

    def __str__(self):
        return f"Account {self.accountNumber} for {self.user_id.username}"