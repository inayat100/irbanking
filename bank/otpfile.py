import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def otp(mail):
    g = random.randint(11000, 19000)
    o = g * 5
    html_content = render_to_string("tem_email.html", {'otp': o})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "otp for verifactions",
        text_content,
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return o

def token_send(email,token,user):
    html_content = render_to_string("tem_email.html", {'token':token ,'name':user,'reset':True})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "otp for verifactions",
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def sender(email,fname,lname,money,account,time,status):
    send = {'fname':fname,'lname':lname,'money':money,'account':account,'time':time,'status':status,'sender':True}
    html_content = render_to_string("tem_email.html",send)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Sent To Rs. {money} From {fname} {lname}',
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def resever(email,fname,lname,money,account,time,status):
    send = {'fname': fname, 'lname': lname, 'money': money, 'account': account, 'time': time, 'status': status,
            'resever': True}
    html_content = render_to_string("tem_email.html", send)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Received Rs. {money} From {fname} {lname}',
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()




def tem_email():
    g = random.randint(11000, 19000)
    o = g * 5
    html_content = render_to_string("tem_email.html",{'otp':o} )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
       "otp for verifactions",
       text_content,
       settings.EMAIL_HOST_USER,
       ['irasool037@gmail.com']
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
