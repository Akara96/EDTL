from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import Trafo, Feeder
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def showDadus(request):
    trafos = Trafo.objects.all()
    context = {
        'title':'Trafo',
        'act':'show',
        'dadus': trafos,
        'current_tab': 'tab_trafo',
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addDadus(request):
    if request.method == 'POST':
        
        zona = request.POST.get('zona')
        feeder = request.POST.get('feeder')
        kordinat = request.POST.get('kordinat')

        Trafo.objects.create(zona=zona, feeder=Feeder.objects.get(id=feeder), kordinat=kordinat)
        messages.success(request, 'Dadus Trafo Adisiona ho Susesu')
        return redirect('app:trafo')

    context = {
        'title':'Add Trafo',
        'act':'inputtrafo',
        'feeder':Feeder.objects.all(),
        'current_tab': 'tab_trafo',
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTrafo(request, id):
    try:
        decode = decode_id(id)
        trafo = Trafo.objects.get(id=decode)
    except ObjectDoesNotExist:
        messages.error(request, 'Trafo La Hetan!')
        return redirect('app:trafo')

    if request.method == 'POST':
        zona = request.POST.get('zona')
        feeder = request.POST.get('feeder')
        kordinat = request.POST.get('kordinat')

        trafo.zona = zona
        trafo.feeder = Feeder.objects.get(id=feeder)
        trafo.kordinat = kordinat
        trafo.save()

        messages.success(request, 'Dadus Trafo Hasai ho Susesu')
        return redirect('app:trafo')

    context = {
        'title':'Edit Trafo',
        'act':'edittrafo',
        'data': trafo,
        'feeder':Feeder.objects.all(),
        'current_tab': 'tab_trafo',
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def detailTrafo(request, id):
    try:
        decode = decode_id(id)
        trafo = Trafo.objects.get(id=decode)
    except ObjectDoesNotExist:
        messages.error(request, 'Trafo La Hetan!')
        return redirect('app:trafo')

    context = {
        'title':'Detail Trafo',
        'act':'detailtrafo',
        'data': trafo,
        'current_tab': 'tab_trafo',
    }
    return render(request, 'admins/page/feeder.html', context)