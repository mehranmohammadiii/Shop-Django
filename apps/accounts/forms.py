from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import re
# -----------------------------------------------------------------------------------------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    
    password_1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    class Meta :
        model = CustomUser
        fields = ('mobile_number', 'email', 'first_name', 'last_name')
    # ---------------------
    def clean_password_2(self):

        data = self.cleaned_data
        if data.get('password_1') and data.get('password_2') and data.get('password_1')!=data.get('password_2'):
            raise ValidationError('رمز و تکرار آن مطابقت ندارد')
        return data.get('password_2')
    # ---------------------
    def save(self, commit = True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password_1'))
        if commit :
            user.save()
        return user
# ------------------------------------------------------------------------------------------------------------------------------------------
class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label='Password',help_text = 'برای تغییر رمز عبور روی این <a href="../password/">لینک</a> کلیک کنید')

    class Meta :
        model = CustomUser
        fields = ('mobile_number', 'email', 'first_name', 'last_name', 'gender', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
# ----------------------------------------------------------------------------------------------------------------------------------------------
class MobileValidationMixin:
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not re.match(r'^09\d{9}$', mobile):
            raise ValidationError('شماره موبایل وارد شده صحیح نمی‌باشد.')
        return mobile

class PasswordValidationMixin:
    def clean_password_2(self):
        data = self.cleaned_data
        if data.get('password_1') and data.get('password_2') and data.get('password_1') != data.get('password_2'):
            raise ValidationError('رمز و تکرار آن مطابقت ندارد')
        return data.get('password_2')
# -----------------------------------------------------------------------------------------------------------------------------------------------
class SignupForm(ModelForm,MobileValidationMixin,PasswordValidationMixin) :

    password_1 = forms.CharField(label='رمز عبور ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    password_2 = forms.CharField(label='تکرار رمز عبور ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}))

    class Meta :
        model = CustomUser
        fields = ('mobile_number',)
        widgets = {
            'mobile_number' : forms.TextInput(attrs={'class':'form-control','placeholder':' شماره باید با 09 شروع شود   '}),
        } 
    # --------------------- 
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password_1'))
        if commit :
            user.save()
        return user
# ----------------------------------------------------------------------------------------------------------------------------------------------
class VerifyForm(forms.Form) :

    active_code = forms.CharField(
        label='کد دریافتی :',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کد دریافتی را وارد کنید'}),
    )
# ----------------------------------------------------------------------------------------------------------------------------------------------
class LoginForm(forms.Form,MobileValidationMixin) :

    mobile_number = forms.CharField(
        max_length=11,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره موبایل  را وارد کنید'}),
    )

    password = forms.CharField(
        max_length=10,
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'رمز عبور را وارد کنید'}),
    )
# ----------------------------------------------------------------------------------------------------------------------------------------------
class RecoveryForm(forms.Form,MobileValidationMixin) :

    mobile_number = forms.CharField(
        max_length=11,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره موبایل  را وارد کنید'}),
    )
# ----------------------------------------------------------------------------------------------------------------------------------------------
class ChangePasswordForm(forms.Form,PasswordValidationMixin) :

    password_1 = forms.CharField(label='رمز عبور ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    password_2 = forms.CharField(label='تکرار رمز عبور ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}))
# ----------------------------------------------------------------------------------------------------------------------------------------------
