from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import RejistuKontadorFoun, Cliente, Aldeia, Contador, Munisipiu, Imajen
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id
from email.message import EmailMessage
import smtplib
from EDTL import settings

from django_q.tasks import async_task

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def showKliente(request):

    kliente = RejistuKontadorFoun.objects.select_related(
        'aldeia__suku__postu__munisipiu'
    ).all()

    context = {
        'title':'Kliente',
        'act':'show',
        'dadus': kliente,
        'tab':'klientepedidu',
    }

    return render(request, 'admins/page/kliente.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def showKlientePedidu(request):

    kliente = RejistuKontadorFoun.objects.all()

    context = {
        'title':'Kliente',
        'act':'show',
        'dadus': kliente,
        'tab':'klientepedidu',
    }

    return render(request, 'admins/page/kliente.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def showKlienteFinal(request):
    kliente = Cliente.objects.all()

    context = {
        'title':'Kliente',
        'act':'show',
        'dadus': kliente,
        'tab':'klientefinal',
    }

    return render(request, 'admins/page/kliente.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def editKlientefinal(request, id):
    if request.method == 'POST':
        naran = request.POST.get('naran')
        id_identidade = request.POST.get('id_identidade')
        naran_kompanhia = request.POST.get('naran_kompanhia')
        kategoria_kliente = request.POST.get('kategoria_kliente')
        hela_fatin = request.POST.get('hela_fatin')
        no_tlf = request.POST.get('no_tlf')
        aldeia = request.POST.get('aldeia')

        try:
            kliente = Cliente.objects.get(id=decode_id(id))
            kliente.naran = naran
            kliente.id_identidade = id_identidade
            kliente.naran_kompanhia = naran_kompanhia
            kliente.kategoria_kliente = kategoria_kliente
            kliente.hela_fatin = hela_fatin
            kliente.no_tlf = no_tlf
            kliente.aldeia_id = aldeia
            kliente.save()

            messages.success(request, 'Kliente final updated successfully.')
        except ObjectDoesNotExist:
            messages.error(request, 'Kliente final not found.')

        return redirect('app:klienteFinal')

    context = {
        'dadus': Cliente.objects.get(id=decode_id(id)),
        'aldeias': Aldeia.objects.all(),
        'title':'Edit Kliente Final',
        'act': 'editklientefinal',
        'tab':'klientefinal',
    }
    return render(request, 'admins/page/kliente.html', context)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def KlientefinalKontador(request, id):
    kontador = Contador.objects.filter(cliente_id=decode_id(id))
    munisipiu = Munisipiu.objects.all()


    print(kontador)

    context = {
        'title':'Kliente Final Kontador',
        'act':'klientekontador',
        'dadus': kontador,
        'munisipiu': munisipiu,
        'id':id,
        'tab':'klientefinal',
    }

    return render(request, 'admins/page/kliente.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def KlientefinalKontadorImajen(request, id):
    imajenkontador = Imajen.objects.filter(cliente_id=decode_id(id))

    context = {
        'title':'Kliente Final Kontador Imajen',
        'act':'klientekontadorimajen',
        'imajens': imajenkontador,
        'id':id,
        'tab':'klientefinal',
    }

    return render(request, 'admins/page/kliente.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin','administrasaun'])
def sendEmail(request, id):
    try:
        decode = decode_id(id)
        kliente = RejistuKontadorFoun.objects.get(id=decode)
    except RejistuKontadorFoun.DoesNotExist:
        messages.error(request, 'Kliente la iha!')
        return redirect('app:kliente')


    if request.method == 'POST':
        email = request.POST.get('email')
        mensajen = request.POST.get('mensajen')

        # sendEmailToKliente('Informasaun Kontador', mensajen, email)
        async_task(sendEmailToKliente, "Informasaun Kontador", mensajen, email)

        kliente.status = "0"
        kliente.save()

        messages.success(request, 'Email sent successfully to {}'.format(kliente.email))
        return redirect('app:kliente')

    context = {
        'title':'Send Email',
        'act':'send',
        'kliente': kliente,
        'tab':'klientepedidu',
    }

    return render(request, 'admins/page/kliente.html', context)


def sendEmailToKliente(sTitle, sdekrip, semail):
    deskrisaun = f'''
    <html>
        <head>
            <title>Informasaun Kontador</title>
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