from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView
app_name='accounts'

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('verify/',views.verifyCodeView.as_view(),name='verify'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('resend-code/<str:mobile>/',views.ResendCodeView.as_view(),name='resend-code'),
    path('recovery/',views.RecoveryPasswordView.as_view(),name='recovery'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('change-password/',views.ChangePasswordView.as_view(),name='cahange-password')

]