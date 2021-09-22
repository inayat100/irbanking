from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django import forms
from django.contrib.auth.models import User

class password_chang_form(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')


# class password_reset_form(SetPasswordForm):
#     new_password1 =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
#     new_password2 =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
#     class Meta:
#         model = User
#         fields = ('new_password1','new_password2')