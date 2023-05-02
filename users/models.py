from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.dispatch import receiver

import re


# Create your models here.
class UserCustomManager(BaseUserManager):
    def create_superuser(self,phone_number,user_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned is_superuser=True')
       
        return self.create_user(phone_number,user_name,password,**other_fields)
        

    def create_user(self,phone_number,user_name,password,**other_fields):
        #logger = logging.getLogger(__name__)

         
        
        if not phone_number:
            raise ValueError(_('You must provide an phone number'))
        #logger.info(f"Normalized phone number: {phone_number}")
        user = self.model(
            phone_number = self.normalize_phone_number(phone_number),
            user_name  = user_name,
            **other_fields
        )

        user.set_password(password)
        user.save()
        #logger.info(f"New user created with phone number: {phone_number}")

        return user
    
    def normalize_phone_number(self,phone_number):

        #remove any non-numeric character
        phone_number = re.sub('[^0-9]','',phone_number)

        # Format the phone number
        if len(phone_number) == 12:
            return phone_number[:7]
        
        # Invalid phone number
        else:
            raise ValueError(f'Invalid phone number AGAIN,')
   


class NewUsers(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=150,unique=True)
    start_date = models.DateTimeField(default = timezone.now)
    about = models.TextField(_("about"),max_length=150,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']

    objects = UserCustomManager()

    def __str__(self) -> str:
        return self.user_name 