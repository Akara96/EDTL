from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import Feeder, Munisipiu
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def showFeeder(request):
    feeders = Feeder.objects.all()
    munisipiu = Munisipiu.objects.all()
    context = {
        'title':'Feeder',
        'act':'show',
        'dadus': feeders,
        'munisipiu': munisipiu,
        'current_tab': 'tab_feeder',
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addFeeder(request):
    if request.method == 'POST':
        munisipiu = request.POST.get('munisipiu')
        naran_feeder = request.POST.get('naran')
        marka = request.POST.get('marka')
        deskrisaun_zona = request.POST.get('deskrisaun_zona')
        Feeder.objects.create(munisipiu=Munisipiu.objects.get(id=munisipiu), naran_feeder=naran_feeder, marka=marka, deskrisaun_zona=deskrisaun_zona)
        messages.success(request, 'Feeder added successfully.')
        return redirect('app:feeder')
    
    context = {
        'title': 'Add Feeder',
        'act': 'input',
        'munisipiu': Munisipiu.objects.all(),
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editFeeder(request, id):
    feeder_id = decode_id(id)
    try:
        feeder = Feeder.objects.get(id=feeder_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Feeder not found.')
        return redirect('app:feeder')

    if request.method == 'POST':
        munisipiu = request.POST.get('munisipiu')
        naran_feeder = request.POST.get('naran')
        marka = request.POST.get('marka')
        deskrisaun = request.POST.get('deskrisaun_zona')
        feeder.munisipiu = Munisipiu.objects.get(id=munisipiu)
        feeder.naran_feeder = naran_feeder
        feeder.marka = marka
        feeder.deskrisaun_zona = deskrisaun
        feeder.save()
        messages.success(request, 'Feeder updated successfully.')
        return redirect('app:feeder')

    context = {
        'title': 'Edit Feeder',
        'act': 'edit',
        'munisipiu': Munisipiu.objects.all(),
        'data': feeder,
    }
    return render(request, 'admins/page/feeder.html', context)