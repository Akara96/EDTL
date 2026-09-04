from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group 
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id
from email.message import EmailMessage
import smtplib
from EDTL import settings
from django.contrib.auth import logout

from django_q.tasks import async_task

@login_required
@allowed_users(allowed_roles=['admin'])
def showUser(request):
    try:
        dadus_group2 = Group.objects.get(name='admin')
        dadus = User.objects.filter(
            (Q(is_superuser=0) | Q(groups=dadus_group2)) &
            ~Q(id=request.user.id),  # Exclude the currently logged-in user
            groups__isnull=False
        ).distinct()
    except ObjectDoesNotExist:
        dadus = None
    context = {
        'act':'show',
        'dadus':dadus,
    }
    return render(request,'admins/page/user.html',context)


@login_required
@allowed_users(allowed_roles=['admin'])
def setPermission(request):
    id = request.POST.get('hash')
    status = request.POST.get('status')
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    user.is_active = status
    user.save()
    messages.success(request,'User Permission Updated Successfully')
    return redirect('app:user')


@login_required
@allowed_users(allowed_roles=['admin'])
def addUser(request):
    if request.method == 'POST':
        user = User(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            is_active=True,
            is_staff=True,
        )
        # user.password = make_password(form.cleaned_data['password'])
        user.save()
        
        lastid = User.objects.all().last()
        user1 = User.objects.get(id=lastid.id)
        groupuser = Group.objects.get(id=request.POST.get('group'))
        user1.groups.add(groupuser)
        messages.success(request,'User Created Succesfully')
        return redirect('app:user')
    
    group = Group.objects.exclude(name__iexact='admin')
    context = {
        'act': 'input',
        'dadus_group':group,
    }
    return render(request, 'admins/page/user.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def setPassword(request, id):
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user.password = make_password(password)
            user.save()

            
            # background service
            async_task(
                sendEmailToAdmin, 
                "Password Foun", 
                f"Your password has been created '{password}'. Please use it to log in.",
                user.email)

            messages.success(request, 'Password Set Successfully')
            return redirect('app:user')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('app:setPassword', id=id)
    
    context = {
        'act': 'setpassword',
        'user': user,
    }
    return render(request, 'admins/page/user.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def editUser(request, id):
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        
        user.groups.clear()
        groupuser = Group.objects.get(id=request.POST.get('group'))
        user.groups.add(groupuser)
        messages.success(request, 'User Updated Successfully')
        return redirect('app:user')

    group = Group.objects.exclude(name__iexact='admin')

    dadus = User.objects.get(id=dekrip)
    user_groups = dadus.groups.all()
    for groups in user_groups:
        print("GROUP: ",groups.name)

    context = {
        'act': 'edit',
        'user': user,
        'dadus_group': group,
        'user1':groups.name,
    }
    return render(request, 'admins/page/user.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def resetPassword(request, id):
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    if request.method == 'POST':
        user.password = make_password("mpgtls2023")
        user.save()

        # ezekuta funsaun haruka email ba user nia password reset iha background
        async_task(
            sendEmailToAdmin,
            "Password Foun",
            "Your password has been reset to the default password 'edtlep#2026'. Please use it to logging in.",
            user.email
        )

        messages.success(request, 'Password Reset Successfully')

        return redirect('app:user')

@login_required
@allowed_users(allowed_roles=['admin','administrasaun','tekniku'])
def changePassword(request, id):
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    if request.method == 'POST':
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password != confirm_password:
            messages.error(request, 'Password Foun ho Password Foun Konfirma la hanesan.')
            return redirect('app:changePassword', id=id)

        user.password = make_password(new_password)
        user.save()
        logoutUser(request)
        return redirect('app:login')

    context = {
        'act': 'changepw',
        'user': user,
    }
    return render(request, 'admins/page/user.html', context)

@login_required
@allowed_users(allowed_roles=['admin','administrasaun','tekniku'])
def showKontaUser(request, id):
    dekrip = decode_id(id)
    user = User.objects.get(id=dekrip)
    context = {
        'act': 'konta',
        'user': user,
    }
    return render(request, 'admins/page/user.html', context)

def sendEmailToAdmin(sTitle, sdekrip, semail):
    deskrisaun = f'''
    <html>
        <head>
            <title>User Information</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #258391;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .custom-button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #258391;
                    color: white !important;
                    text-decoration: none;
                    border-radius: 8px;
                    border: 2px solid #1c6775;
                    font-weight: bold;
                    text-align: center;
                    margin: 20px auto;
                    display: block;
                    width: fit-content;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .custom-button:hover {{
                    background-color: #1c6775;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                    color: white;
                }}
                .custom-button:active {{
                    transform: translateY(1px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 14px;
                    line-height: 1.6;
                }}
                .highlight {{
                    color: #258391;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{sTitle}</h1>
                <p>{sdekrip}</p>
                <div class="footer">
                    <p>
                        <span class="highlight">EDTL, E.P.</span><br>
                        <span class="highlight">Direcção de Operasional</span><br>
                        Emal: <span class="highlight">administrasaun@edtl-ep.tl</span><br>
                        Web-Site: <span class="highlight">https://www.edtl-ep.tl</span>
                    </p>
                </div>
            </div>
        </body>
    </html>
    '''

    em = EmailMessage()
    em['From'] = settings.EMAIL_USER
    em['To'] = semail
    em['Subject'] = 'Sistema Rejistu Kontador'
    em['Importance'] = 'High'
    em['X-Priority'] = '1'
    em['X-MSMail-Priority'] = 'High'
    em['X-Auto-Response-Suppress'] = 'All'

    em.add_alternative(deskrisaun, subtype='html')

    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    s.starttls()
    s.login(settings.EMAIL_USER, settings.EMAIL_PW)
    s.sendmail(settings.EMAIL_USER, semail, em.as_string())
    s.quit()

def logoutUser(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request,'Successfuly logged out')
    return redirect('app:login')