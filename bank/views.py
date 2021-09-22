from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login,update_session_auth_hash
from .forms import password_chang_form
import random
from .models import account,history,vrf,email_token
from django.db import IntegrityError,transaction
from . otpfile import otp,token_send,sender,resever,tem_email
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import datetime

def home(request):
    # dt = User.objects.get(pk = request.user.id)
    # print(dt.email)
    # tem_email()

    return render(request,'banking.html')

def customers(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request,'loging.html')

def employee(request):
    return render(request,'employee.html')

def singup(request):
    if request.method == "POST":
        user = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=user).exists():
            messages.error(request,'this user name is alredy taken please enter other user name')
            return render(request, 'singup.html')
        # if User.objects.filter(email=email).exists():
        #     messages.error(request,'this email id  is alredy taken please enter other email id')
        #     return render(request, 'singup.html')
        if pass1 != pass2:
            messages.error(request,f'passwprs is not same both {pass1} and {pass2},please enter same password')
            return render(request, 'singup.html')
        myuser = User.objects.create_user(user, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'User created now ......')
        return redirect('singin')
    else:
        return render(request,'singup.html')

def singin(request):
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['pass']
        log = authenticate(username=user,password=password)
        if log:
            login(request,log)
            messages.success(request,'login successfully......')
            if account.objects.filter(user=request.user).exists():
                return redirect('profile')
            else:
                return redirect('emailotp')
        else:
            messages.error(request,f'This User > {user} and password > {password} is not match in database...')
    return render(request,'loging.html')

def user_logout(request):
    logout(request)
    messages.success(request,'user logout....')
    return redirect('/')

def email_otp(request):
    if request.user.is_authenticated:
        g = random.randint(11000, 19000)
        o = g * 5
        dt = User.objects.get(pk=request.user.id)
        send_mail(
            'otp for verifactions',
            str(o),
            settings.EMAIL_HOST_USER,
            [dt.email],
            fail_silently=False
        )
        messages.success(request,'OTP send your Register Email id......')
        return render(request, 'emailotp.html',{'otp':o})
    else:
        return redirect('singin')

def email_vfr(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            otp = request.POST['eotp']
            print(id)
            print(otp)
            print(type(id))
            print(type(otp))
            if otp == id:
                if vrf.objects.filter(name=request.user).exists():
                    return redirect('openaccount')
                vf = vrf(user=request.user,name=request.user,vf=True)
                vf.save()
                messages.success(request,'OTP match now your email id is verified....')
                return redirect('openaccount')
            else:
                messages.error(request, 'OTP is not match please try again..... ')
                return redirect('emailotp')

        else:
            messages.error(request,'Something  is wrong please try again..... ')
            return redirect('emailotp')
    else:
        return redirect('singin')

def send_money(request, ot):
    if request.user.is_authenticated:
        if request.method == 'POST':
            acnd = int(request.POST['acn'])
            amonut = request.POST['amount']
            otp = int(request.POST['otp'])
            ac = account.objects.get(user=request.user)
            if acnd == ac.acn:
                messages.error(request,'your are sending in your accpunt please enter other user account')
                return redirect('moneyotp')
            if account.objects.filter(acn=acnd).exists():
                with transaction.atomic():
                    if ot == otp:
                        trf_obj = account.objects.get(acn=acnd)
                        user_obj = account.objects.get(user=request.user)
                        his =history(user=user_obj.user,acn=trf_obj.acn,dev=amonut,action='complate')
                        his.save()
                        user_obj.amount -= int(amonut)
                        user_obj.save()

                        rhis = history(user=trf_obj.user, acn=user_obj.acn, crid=amonut,action='complate')
                        rhis.save()
                        trf_obj.amount += int(amonut)
                        trf_obj.save()
                        time = datetime.datetime.now()
                        sender_uk = user_obj.user.id
                        resever_uk = trf_obj.user.id
                        user_email = User.objects.get(pk=sender_uk)
                        resever_email = User.objects.get(pk=resever_uk)
                        resever(resever_email.email, user_email.first_name, user_email.last_name, amonut, acnd, time, 'Done')
                        sender(user_email.email,resever_email.first_name,resever_email.last_name,amonut,user_obj.acn,time,'Done')
                        messages.success(request, f'{amonut} rupees send successfully......')
                        return redirect('history')

                    else:
                        tr = account.objects.get(acn=acnd)
                        pr = account.objects.get(user=request.user)

                        his = history(user=pr.user, acn=tr.acn, dev=amonut, action='faild')
                        his.save()


                        rhis = history(user=tr.user, acn=pr.acn, crid=amonut, action='faild')
                        rhis.save()
                        messages.error(request,'somthing is wrong please enter right informations....')
                    return redirect('moneyotp')
            else:
                messages.info(request,'your are entered wrong account number , please enter right account number')
                return redirect('moneyotp')
        else:
            return redirect('moneyotp')
    else:
        return redirect('singin')

def money_otp(request):
    if request.user.is_authenticated:
        if account.objects.filter(user=request.user).exists():
            ml = User.objects.get(pk=request.user.id)
            mail = ml.email
            p = otp(mail)
            messages.success(request,'OTP send your register email id.....')
            return render(request, 'sendmoney.html',{'o':p})
        else:
            messages.error(request, "you can't send money now first please create your account...")
            return redirect('emailotp')

def his(request):
    if request.user.is_authenticated:
        hs = history.objects.filter(user=request.user).reverse()
        ct = hs.count()
        return render(request,'his.html',{'hs':hs,'conut':ct})
    return redirect('singin')

def open_account(request):
    if request.user.is_authenticated:
        if vrf.objects.filter(name=request.user).exists() and account.objects.filter(user=request.user).exists():
            return redirect('profile')
        else:
            g = random.randint(44444444, 99999999)
            ac = g * 5
            if request.method == 'POST':
                phone = request.POST['phone']
                addres = request.POST['addres']
                city = request.POST['city']
                state = request.POST['state']
                print(phone,addres,city,state)
                acd = account(user=request.user,phone=phone,addres=addres,city=city,state=state,acn=ac,amount=1000)
                acd.save()
                messages.success(request,'created successfully your account.....')
                return redirect('profile')
            if vrf.objects.filter(name=request.user).exists():
                return render(request,'ao.html')
            else:
                messages.info(request,'Your must verified your email with otp.....')
                return redirect('emailotp')
    return redirect('singin')

def user_profile(request):
    if request.user.is_authenticated:
        if account.objects.filter(user=request.user).exists():
            pr = account.objects.get(user=request.user)
            us = User.objects.get(pk = request.user.id)
            return render(request,'profile.html',{'pr':pr,'us':us})
        else:
            messages.info(request,'your account is not exists please create your account...')
            return redirect('emailotp')
    else:
        return redirect('singin')

def password_chang(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            ps = password_chang_form(user=request.user,data=request.POST)
            if ps.is_valid():
                ps.save()
                update_session_auth_hash(request,ps.user)
                messages.success(request, 'Password changed.....')
                return redirect('profile')
            else:
                messages.info(request,'something is wrong informations..')
        ps = password_chang_form(user=request.user)
        return render(request,'pch.html',{'form':ps})
    return redirect('singin')

def forget_password(request):
    if request.method == "POST":
        user = request.POST['user']
        if User.objects.filter(username=user).exists():
            user_obj = User.objects.get(username=user)
            ts = email_token.objects.filter(name=user).exists()
            if ts:
                dl = email_token.objects.filter(name=user)
                dl.delete()
            token = str(uuid.uuid4())
            print("now catching.....")
            profile_obj = email_token(user=user_obj,forget_token=token,name=user)
            profile_obj.save()
            token_send(user_obj.email,token,user_obj.username)
            print("email send you ")
            return render(request,'sentmail.html',{'msg':'you can reset your password just click on link the link had sent your mail id'})
        else:
            messages.info(request,f'{user} is not exists please enter exists user.....')
            return redirect('forgetpassword')
    else:
        return render(request,'forgetpass.html')

def changing_password(request,token):

    obj = email_token.objects.filter(forget_token=token).first()
    if request.method == "POST":
        new_pss = request.POST['pass1']
        new_pss2 = request.POST['pass2']
        user_id = request.POST['user_id']
        if new_pss != new_pss2:
            messages.info(request,f'password is not same{new_pss} and {new_pss2}')
            return redirect(f'resetpassword/{token}/')
        if user_id is None:
            return redirect(f'resetpassword/{token}/')
        user_obj = User.objects.get(pk= user_id)
        user_obj.set_password(new_pss)
        user_obj.save()
        messages.success(request,'Password reset successfully.....')
        dt = email_token.objects.get(forget_token=token)
        dt.delete()
        return redirect('singin')
    user_id = obj.user.id
    return render(request, 'changing.html',{'user_id':user_id})

