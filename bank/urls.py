from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('customers/',views.customers,name='customers'),
    path('employee/',views.employee,name='employee'),
    path('forgetpassword/',views.forget_password,name='forgetpassword'),
    path('resetpassword/<token>/',views.changing_password,name='resetpassword'),
    path('singup/',views.singup,name='singup'),
    path('singin/',views.singin,name='singin'),
    path('emailotp/',views.email_otp,name='emailotp'),
    path('emailvfr/<str:id>/',views.email_vfr,name='emailvfr'),
    path('profile/',views.user_profile,name='profile'),
    path('sendmoney/<int:ot>/',views.send_money,name='sendmoney'),
    path('moneyotp/',views.money_otp,name='moneyotp'),
    path('history/',views.his,name='history'),
    path('openaccount/',views.open_account,name='openaccount'),
    path('logout/',views.user_logout,name='logout'),
    path('passwordchang/',views.password_chang,name='passwordchang'),


]