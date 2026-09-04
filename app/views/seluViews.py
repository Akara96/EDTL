from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q
from app.models import Selu, Cliente, Contador, Survey
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id
from django.http import JsonResponse

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin', 'tekniku','administrasaun'])
def showDadus(request):
    selus = Selu.objects.all()
    context = {
        'act':'show',
        'selu': selus,
    }
    return render(request, 'admins/page/selu.html', context)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['administrasaun'])
def addDadus(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        montante = request.POST.get('montante')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            if Selu.objects.filter(cliente=cliente).exists():
                messages.error(request, 'Kliente refere halo ona pagamentu')
                return redirect('app:addPagamentu')
            new_selu = Selu(
                cliente=cliente,
                montante=montante,
                status=0
            )
            new_selu.save()
            messages.success(request, 'Pagamentu ezekuta ho susesu')
            return redirect('app:pagamento')
        except ObjectDoesNotExist:
            messages.error(request, 'Kliente ne\'e la ekziste.')
            return redirect('app:addPagamentu')

    kontador = Contador.objects.select_related('cliente')
    
    context = {
        'act':'add',
        'dadus': kontador,
    }
    return render(request, 'admins/page/selu.html', context)

def getSurvey(request, id):
    try:
        selu = Survey.objects.get(cliente_id=id)
        survey_data = {
            'tipu_ligasaun': selu.tipu_ligasaun,
            'feeder': selu.feeder,
            'nu_trafo': selu.nu_trafo,
            'data_survey': selu.data_survey,
            'tekniku': selu.tekniku.naran if selu.tekniku else '',
            'montante': selu.kalkulasaun(),
        }
        return JsonResponse({'message': 'success', 'data': survey_data})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'error', 'data': {}})


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['administrasaun'])
def editDadus(request, id):
    decoded_id = decode_id(id)
    try:
        selu = Selu.objects.get(id=decoded_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Dadus la eziste.')
        return redirect('app:pagamento')

    if request.method == 'POST':
        montante = request.POST.get('montante')
        status = request.POST.get('status')

        selu.montante = montante
        selu.status = status
        selu.save()

        messages.success(request, 'Pagamentu atualiza ho susesu.')
        return redirect('app:pagamento')

    kontador = Contador.objects.select_related('cliente')

    context = {
        'act': 'edit',
        'data': selu,
        'dadus': kontador,

    }
    return render(request, 'admins/page/selu.html', context)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin', 'administrasaun'])
def imprimePaga(request, id):
    decoded_id = decode_id(id)
    try:
        selu = Selu.objects.select_related('cliente').get(cliente_id=decoded_id)

        print(selu.montante)
    except ObjectDoesNotExist:
        messages.error(request, 'Dadus la eziste.')
        return redirect('app:pagamento')

    context = {
        'data': selu,
        'montanteselu': int(selu.montante) + 1,
    }
    return render(request, 'admins/page/reportpaga.html', context)