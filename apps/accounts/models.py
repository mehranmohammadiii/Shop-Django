from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self,mobile_number,password=None,**extra_fields):
        if not mobile_number:
            raise ValueError(' وارد کردن شماره موبایل الزامی است')
        user = self.model(
                    mobile_number = mobile_number,
                    **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # ---------------------------------
    def create_superuser(self,mobile_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(mobile_number,password,**extra_fields)
# ----------------------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser,PermissionsMixin) :

    mobile_number = models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل')
    first_name = models.CharField(max_length=30,blank=True,verbose_name='Name')
    last_name = models.CharField(max_length=30,blank=True,verbose_name='Family')
    email = models.EmailField(max_length=100, blank=True, verbose_name='ایمیل')

    GENDER_CHOICES = ((True,'مرد'),(False,'زن'))
    gender = models.BooleanField(choices=GENDER_CHOICES,default=True,null=True,blank=True,verbose_name='جنسیت')

    register_date = models.DateField(auto_now_add=True,verbose_name='تاریخ ثبت')

    is_active = models.BooleanField(default=False,verbose_name='وضعیت')
    active_code = models.CharField(max_length=10,null=True,blank=True,verbose_name='کد دریافتی')

    is_staff = models.BooleanField(default=False,verbose_name='کارمند')
    is_superuser = models.BooleanField(default=False,verbose_name=' ادمین کل')

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return f'{self.mobile_number}/t{self.is_active}'
    
    class Meta :
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

# ----------------------------------------------------------------------------------------------------

