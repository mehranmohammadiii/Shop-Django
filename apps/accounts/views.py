from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from .forms import SignupForm,VerifyForm,LoginForm,RecoveryForm,ChangePasswordForm
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate
import utils
from django.contrib import messages
from . models import CustomUser
from django.views import View
from .mixins import RedirectLoggedInUserMixin
# ------------------------------------------------------------------------------------------------------------------------------------
class SignUpView(CreateView,RedirectLoggedInUserMixin):

    form_class = SignupForm
    success_url = reverse_lazy('accounts:verify')
    template_name = 'accounts/signup.html'
    context_object_name = 'form'
    # ------------------------
    def form_valid(self, form):

        user = form.save(commit=False)
        active_code = utils.create_random_code(5)
        user.active_code = active_code
        user.save()

        self.request.session['user_mobile'] = user.mobile_number
        self.request.session['recovery_password'] = False

        utils.send_sms(user.mobile_number,f'کد فعالسازی حساب کاربری شما {active_code} می باشد')

        print(active_code)

        messages.success(self.request,'کد فعالسازی برای شما ارسال شد','success')  
        return super().form_valid(form)
# ----------------------------------------------------------------------------------------------------------------------------------------
class verifyCodeView(View):

    form_class = VerifyForm
    template_name = 'accounts/verify_code.html'

    def get(self, request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})
    # ------------------------
    def post(self,request):

        try :
            mobile = self.request.session['user_mobile']
        except :
            messages.error(self.request,'خطایی رخ داده لطفا دوباره امتحان کنید','danger')
            return redirect('accounts:signup',)

        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('active_code')
            try :
                user = CustomUser.objects.get(mobile_number=mobile)
                if user.active_code == code:
                    if request.session['recovery_password'] :
                        active_code = utils.create_random_code(5)
                        user.active_code = active_code
                        user.save()
                        return redirect("accounts:cahange-password")
                    else:
                        user.is_active=True
                        active_code = utils.create_random_code(5)
                        user.active_code = active_code
                        user.save()
                        login(request, user)
                        messages.success(request,'  حساب شما با موفقیت ثبت شد ','success')  
                        return redirect('main:index')
                else:
                    messages.error(request, 'کد وارد شده صحیح نمی‌باشد.', 'danger')
            except CustomUser.DoesNotExist:
                messages.error(request,'کاربری با این شماره موبایل یافت نشد','danger')
        return render(request, self.template_name, {'form': form})
# ---------------------------------------------------------------------------------------------------------------------------------------------
class LoginView(View,RedirectLoggedInUserMixin):

    form_class = LoginForm
    template_name = 'accounts/login.html'
    # ------------------------
    def get(self, request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    # ------------------------
    def post(self,request):

        form = self.form_class(request.POST)
        if form.is_valid() :
            mobile = form.cleaned_data.get('mobile_number')
            password = form.cleaned_data.get('password')
            # user = authenticate(request,username=mobile,password=password)
            try:
                user = CustomUser.objects.get(mobile_number=mobile)
                if user.check_password(password):
                    if user.is_active :
                        if not user.is_staff :
                            login(request,user)
                            messages.success(request, 'با موفقیت وارد شدید.', 'success')
                            return redirect('main:index')
                        else :
                            messages.error(request, 'شما نمیتوانید به این صفحه وارد شوید', 'danger')

                    else:
                        messages.warning(request, 'حساب کاربری شما هنوز فعال نشده است.', 'warning')
                        return render(request,self.template_name,{'form':form,'inactive_user_mobile':user.mobile_number})

                else:
                    messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.', 'danger')

            except CustomUser.DoesNotExist:
                    messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.', 'danger')

        return render(request, self.template_name, {'form': form})
# ------------------------------------------------------------------------------------------------------------------------------------------
class ResendCodeView(View):

    def get(self,request,mobile):
        user = get_object_or_404(CustomUser,mobile_number=mobile,is_active=False)
        active_code = utils.create_random_code(5)
        user.active_code = active_code
        user.save()
        utils.send_sms(user.mobile_number,f'کد فعالسازی حساب کاربری شما {active_code} می باشد')
        print(active_code)
        request.session['user_mobile'] = user.mobile_number
        messages.success(request, 'کد فعال‌سازی جدید برای شما ارسال شد.', 'success')
        return redirect('accounts:verify')
# ----------------------------------------------------------------------------------------------------------------------------------------------
class RecoveryPasswordView(View,RedirectLoggedInUserMixin):

    form_class = RecoveryForm
    template_name = 'accounts/recovery.html'
    # ------------------------
    def get(self, request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    # ------------------------  
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile_number')
            try :
                user = CustomUser.objects.get(mobile_number=mobile,is_active=True)
                active_code = utils.create_random_code(5)
                user.active_code = active_code
                user.save()
                utils.send_sms(user.mobile_number,f'کد فعالسازی حساب کاربری شما {active_code} می باشد')
                print(active_code)
                request.session['user_mobile'] = user.mobile_number
                request.session['recovery_password'] = True

                messages.success(request, 'کد فعال‌سازی جدید برای شما ارسال شد.', 'success')
                return redirect('accounts:verify')
            except :
                    messages.success(request, '  کاربری با این شماره یافت نشد.', 'danger')
                    return redirect('accounts:recovery')
            
        messages.success(request, '  کاربری با این شماره یافت نشد.', 'danger')
        return redirect('accounts:recovery')
# --------------------------------------------------------------------------------------------------------------------------------------------
class UserPanelView(View):
    pass
# -------------------------------------------------------------------------------------------------------------------------------------------
class ChangePasswordView(View):

    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'
# ------------------------
    def get(self, request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    # ---------------------  
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
                user = CustomUser.objects.get(mobile_number=request.session.get('user_mobile'))
                user.set_password(form.cleaned_data.get('password_1'))
                user.save()
                messages.success(request, ' رمز عبور شما با موفقیت تغییر کرد.', 'success')
                return redirect('accounts:login')

        messages.success(request, ' خطایی رخ داده لظفا دوباره امتحان کنید .', 'danger')
        return redirect('accounts:login')
# --------------------------------------------------------------------------------------------------------------------------------------------
