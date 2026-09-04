from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import Contador, Tekniku, Munisipiu
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def showDadus(request):
    kontador = Contador.objects.select_related(
        'trafo__feeder__munisipiu'
    ).all()
    munisipiu = Munisipiu.objects.all()
    context = {
        'act':'show',
        'dadus': kontador,
        'munisipiu': munisipiu,
    }
    return render(request, 'admins/page/kontador.html', context)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def addTekniku(request):
    if request.method == 'POST':
        
        id_tekniku = request.POST.get('id_tekniku')
        naran = request.POST.get('naran')
        enderesu = request.POST.get('enderesu')
        email = request.POST.get('email')
        no_tlf = request.POST.get('no_tlf')
        user_id = request.POST.get('user')

        Tekniku.objects.create(
            id_tekniku=id_tekniku,
            naran=naran,
            enderesu=enderesu,
            email=email,
            no_tlf=no_tlf,
            user_id=user_id if user_id else None
        )

        messages.success(request, 'Dadus Adisiona ho Susesu!')
        return redirect('app:tekniku')
    users = User.objects.filter(groups__name='tekniku')
    context = {
        'act': 'input',
        'user': users,
    }
    return render(request, 'admins/page/tekniku.html', context)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def editTekniku(request, id):
    try:
        decode = decode_id(id)
        tekniku = Tekniku.objects.get(id=decode)
    except Tekniku.DoesNotExist:
        messages.error(request, 'Tekniku Not Found or Invalid ID!')
        return redirect('app:tekniku')

    if request.method == 'POST':
        tekniku.naran = request.POST.get('naran')
        tekniku.enderesu = request.POST.get('enderesu')
        tekniku.email = request.POST.get('email')
        tekniku.no_tlf = request.POST.get('no_tlf')
        user_id = request.POST.get('user')
        tekniku.user_id = user_id if user_id else None
        tekniku.save()

        messages.success(request, 'Dadus Atualiza ho Susesu!')
        return redirect('app:tekniku')

    users = User.objects.filter(Q(groups__name='tekniku') | Q(id=tekniku.user_id))
    context = {
        'act': 'edit',
        'data': tekniku,
        'user': users,
    }
    return render(request, 'admins/page/tekniku.html', context)

