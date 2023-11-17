from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from django.conf import settings 
from rest_framework.authtoken.models import Token

from django.dispatch import receiver 






class DateTimeUTCField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

# Create your models here.
from enum import IntEnum

class UserStatus(IntEnum):
    ACTIVE = 0
    IN_ACTIVE = 1
    SUSPENDED = 2
    DELETED = 3

class Gender(IntEnum):
    MALE = 0
    FEMALE = 1


class UserManager(BaseUserManager):
    def create_user(self ,email,username,password =None,**extra_fields):
        if not email :
            raise ValueError ("Users Must have an email")
        if not username :
            raise ValueError ("Users Must have username")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            **extra_fields,
                          )
        user.set_password(password)
        user.save(using =self._db)
        return user
    
    def create_superuser(self ,email,username,password):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password =password,
            username = username)
        user.is_admin =True
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using =self._db)
        return user 



class User (AbstractBaseUser):


    id = models.AutoField(primary_key=True)
    # user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    server_DateTime = models.DateTimeField(auto_now=True)
    DateTime_UTC =DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    Update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    username = models.CharField(max_length=60 ,unique=True)
    email =models.EmailField (verbose_name="email" ,max_length=180,unique=True) 
    #Django's default behavior is to use UTF-8 encoding, which is suitable for handling Unicode characters and siutablle for "NVARCHAR" stands for "National Variable Character.
    firstName =models.CharField(max_length= 40 )
    lastName = models.CharField (max_length=60 )
    status = models.IntegerField(choices=[(status.value, status.name) for status in UserStatus], default=UserStatus.ACTIVE)
    gender = models.IntegerField(choices=[(gender.value, gender.name) for gender in Gender], default=Gender.MALE)
    date_of_Birth = models.DateTimeField (blank=True ,null=True)
    password = models.CharField(max_length=128, default='default_password')

    is_admin =models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS =["username"]

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm (self , perm , obj =None):
        return self.is_admin
    
    def has_module_perms (self,app_label):
        return True
    
    






class Account (models.Model):
    Currency_Choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('JOD' ,'Jordanian Dinar')
    ]
    Active =0
    In_Active =1
    Suspended=2
    Deleted = 3

    Account_Status_Choices =[
        (Active ,"Active"),
        (In_Active,"In_Active"),
        (Suspended ,"Suspended"),
        (Deleted ,"Deleted")
    ]
    id = models.AutoField (primary_key=True)
    user_id = models.ForeignKey(User ,on_delete=models.CASCADE)
    server_DateTime = models.DateTimeField(auto_now=True)
    dateTime_UTC =DateTimeUTCField(auto_now = True ,null=True ,blank =True)
    update_DateTime_UTC = DateTimeUTCField(auto_now=True)
    accountNumber =models.CharField (max_length=30)
    balance =models.DecimalField(max_digits=7 ,decimal_places=2 ,validators=[MinValueValidator(0.01)])
    currency = models.CharField(choices=Currency_Choices ,max_length=15, default="USD")

    status = models.IntegerField (choices=Account_Status_Choices ,default = Active)

    def __str__(self):
        return f"{self.username} - Status: {self.get_status_display()}"
    
@receiver(post_save , sender =settings.AUTH_USER_MODEL)

def create_token(sender, instance, created, **kwargs):
    if created:
        try:
            Token.objects.create(user=instance)
        except Exception as e:
            print(f"Error creating token: {e}")