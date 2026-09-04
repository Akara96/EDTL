from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import Munisipiu
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id

@login_required
@allowed_users(allowed_roles=['admin'])
def showMunisipiu(request):
    try:
        dadus = Munisipiu.objects.all()
    except ObjectDoesNotExist:
        dadus = None
    context = {
        'act':'show',
        'dadus':dadus,
        'tab': request.GET.get('tab', 'tab_mundadus')
    }
    return render(request,'admins/page/munisipiu.html',context)


@login_required
@allowed_users(allowed_roles=['admin'])
def addMunisipiu(request):
    if request.method == 'POST':
        munisipiu = request.POST.get('munisipiu')
        kodigu = request.POST.get('kodigu')
        area = request.POST.get('area')
        kor_inline = request.POST.get('kor_inline')
        kor_outline = request.POST.get('kor_outline')

        fahe = area.replace('[', '').replace(']', '').replace('"lat"', '').replace('"lng"', '').replace(':', '')
        fahe1 = fahe.replace('{', '[')
        fahe2 = fahe1.replace('}', ']')

        Munisipiu.objects.create(
            munisipiu=munisipiu,
            kodigu=kodigu,
            area=fahe2,
            inline_color=kor_inline,
            outline_color=kor_outline
        )
        messages.success(request, 'Munisipiu Added Successfully')
        return redirect('app:munisipiu')

    context = {
        'act': 'input',
    }
    return render(request, 'admins/page/munisipiu.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def editMunisipiu(request, id):
    decoded_id = decode_id(id)
    try:
        dadus = Munisipiu.objects.get(id=decoded_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Munisipiu not found')
        return redirect('app:munisipiu')

    if request.method == 'POST':
        munisipiu = request.POST.get('munisipiu')
        kodigu = request.POST.get('kodigu')
        area = request.POST.get('area')
        kor_inline = request.POST.get('kor_inline')
        kor_outline = request.POST.get('kor_outline')

        fahe = area.replace('[', '').replace(']', '').replace('"lat"', '').replace('"lng"', '').replace(':', '')
        fahe1 = fahe.replace('{', '[')
        fahe2 = fahe1.replace('}', ']')

        dadus.munisipiu = munisipiu
        dadus.kodigu = kodigu
        dadus.area = fahe2
        dadus.inline_color = kor_inline
        dadus.outline_color = kor_outline
        dadus.save()

        messages.success(request, 'Munisipiu Updated Successfully')
        return redirect('app:munisipiu')

    context = {
        'act': 'edit',
        'data': dadus,
    }
    return render(request, 'admins/page/munisipiu.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def detailMunisipiu(request, id):
    decoded_id = decode_id(id)
    try:
        dadus = Munisipiu.objects.get(id=decoded_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Munisipiu not found')
        return redirect('app:munisipiu')

    context = {
        'act': 'detail',
        'data': dadus,
    }
    return render(request, 'admins/page/munisipiu.html', context)