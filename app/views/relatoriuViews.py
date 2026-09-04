from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum
from app.models import Munisipiu, Feeder, Trafo, Contador, Selu, Cliente
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id
from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def showForm(request):
    current_year = datetime.now().year
    years = list(range(2020, current_year + 1))

    fulan = [
        {'name': 'Janeiru', 'value': 1},
        {'name': 'Fevereiru', 'value': 2},
        {'name': 'Marsu', 'value': 3},
        {'name': 'Abril', 'value': 4},
        {'name': 'Maiu', 'value': 5},
        {'name': 'Juniu', 'value': 6},
        {'name': 'Jullu', 'value': 7},
        {'name': 'Agostu', 'value': 8},
        {'name': 'Setembru', 'value': 9},
        {'name': 'Outubru', 'value': 10},
        {'name': 'Novembru', 'value': 11},
        {'name': 'Dezembru', 'value': 12}
    ]

    context = {
        'act':'show',
        'munisipius': Munisipiu.objects.all(),
        'feeders': Feeder.objects.all(),
        'trafos': Trafo.objects.all(),
        'contadors': Contador.objects.all(),
        'years': years,
        'months': fulan,
    }
    return render(request, 'admins/page/relatoriu.html', context)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def showFeeder(request):
    if request.method == 'GET':
        feeders = Feeder.objects.all()
        feeder_list = [{'id': feeder.id, 'naran_feeder': feeder.naran_feeder, 'munisipiu': feeder.munisipiu.munisipiu} for feeder in feeders]
        return JsonResponse(feeder_list, safe=False)


@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def getDetailFeeders(request):
    munid = request.GET.get('munisipiu')
    if munid:
        feeders = Feeder.objects.filter(munisipiu__id=munid)
        feeder_list = [{'id': feeder.id, 'feeder': feeder.naran_feeder} for feeder in feeders]
        return JsonResponse(feeder_list, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def getTrafos(request):
    feeders = Trafo.objects.all()
    trafo_list = [{'id': trafo.id, 'zona': trafo.zona} for trafo in feeders]
    return JsonResponse(trafo_list, safe=False)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def getDetailTrafos(request):
    feederid = request.GET.get('feeder')
    if feederid:
        trafos = Trafo.objects.filter(feeder__id=feederid)
        trafo_list = [{'id': trafo.id, 'zona': trafo.zona} for trafo in trafos]
        return JsonResponse(trafo_list, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def getContadors(request):
    contadors = Contador.objects.all()
    contador_list = [{'id': contador.id, 'naran_kontador': contador.nu_kontador} for contador in contadors]  # FIXED: naran_kontador -> nu_kontador
    return JsonResponse(contador_list, safe=False)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def getDetailContadors(request):
    trafoid = request.GET.get('trafo')
    if trafoid:
        contadors = Contador.objects.filter(trafo__id=trafoid)
        contador_list = [{'id': contador.id, 'nu_kontador': contador.nu_kontador} for contador in contadors]
        return JsonResponse(contador_list, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='app:login')
@allowed_users(allowed_roles=['admin'])
def imprimeRelatoriu(request):
    if request.method == 'POST':
        munisipiu_id = request.POST.get('munisipiu')
        feeder_id = request.POST.get('feeder')
        trafo_id = request.POST.get('trafo')
        contador_id = request.POST.get('contador')
        tinan = request.POST.get('tinan')
        fulan = request.POST.get('fulan')
        
        # Start building the query
        filters = Q()
        
        if munisipiu_id and munisipiu_id != "Hotu":
            filters &= Q(trafo__feeder__munisipiu_id=munisipiu_id)
        
        if feeder_id and feeder_id != "Hotu":
            filters &= Q(trafo__feeder_id=feeder_id)
        
        if trafo_id and trafo_id != "Hotu":
            filters &= Q(trafo_id=trafo_id)
        
        if contador_id and contador_id != "Hotu":
            filters &= Q(id=contador_id)
        
        # Get Contador with related data
        contadors = Contador.objects.filter(filters).select_related(
            'cliente',
            'trafo',
            'trafo__feeder',
            'trafo__feeder__munisipiu'
        )
        
        # Apply date filters
        if tinan and tinan != "":
            contadors = contadors.filter(created_at__year=int(tinan))
        
        if fulan and fulan != "":
            contadors = contadors.filter(created_at__month=int(fulan))
        
        # Get unique client IDs
        cliente_ids = contadors.exclude(cliente__isnull=True).values_list('cliente_id', flat=True).distinct()
        
        # Initialize payment dictionary
        payment_dict = {}
        
        # Get all payments for these clients
        if cliente_ids:
            payments = Selu.objects.filter(cliente_id__in=cliente_ids).values('cliente_id').annotate(
                total_payment=Sum('montante')
            )
            payment_dict = {p['cliente_id']: (p['total_payment'] or Decimal('0.00')) for p in payments}
        
        # Prepare data for template
        data_list = []
        total_pendapatan = Decimal('0.00')
        
        for contador in contadors:
            # Basic information
            cliente = contador.cliente
            cliente_nome = cliente.naran if cliente else "-"
            
            # Location information
            munisipiu_nome = "-"
            feeder_nome = "-"
            trafo_nome = "-"
            
            if contador.trafo:
                trafo = contador.trafo
                trafo_nome = trafo.zona if trafo.zona else f"Trafo {trafo.id}"
                
                if trafo.feeder:
                    feeder = trafo.feeder
                    feeder_nome = feeder.naran_feeder if feeder.naran_feeder else "-"
                    
                    if feeder.munisipiu:
                        munisipiu_nome = feeder.munisipiu.munisipiu if feeder.munisipiu.munisipiu else "-"
            
            # Get payment amount
            # Di dalam loop, konversi payment ke Decimal
            if cliente:
                payment_value = payment_dict.get(cliente.id, 0.00)
                # Konversi float ke Decimal
                total_payment = Decimal(str(payment_value)) if payment_value else Decimal('0.00')
            else:
                total_payment = Decimal('0.00')

            total_pendapatan += total_payment
            
            data_list.append({
                'nu_kontador': contador.nu_kontador or "-",
                'naran_kliente': cliente_nome,
                'munisipiu': munisipiu_nome,
                'feeder': feeder_nome,
                'trafo': trafo_nome,
                'status': "Ativu",
                'montante': f"{total_payment:,.2f}"
            })
        
        # Get filter objects for display
        munisipiu = None
        feeder = None
        trafo = None
        contador_single = None
        
        try:
            if munisipiu_id and munisipiu_id != "Hotu":
                munisipiu = Munisipiu.objects.filter(id=munisipiu_id).first()
            
            if feeder_id and feeder_id != "Hotu":
                feeder = Feeder.objects.filter(id=feeder_id).first()
            
            if trafo_id and trafo_id != "Hotu":
                trafo = Trafo.objects.filter(id=trafo_id).first()
            
            if contador_id and contador_id != "Hotu":
                contador_single = Contador.objects.filter(id=contador_id).first()
        except Exception as e:
            print(f"Error getting filter objects: {e}")
        
        # Month names
        month_names = {
            '1': 'Janeiru', '2': 'Fevereiru', '3': 'Marsu', '4': 'Abril',
            '5': 'Maiu', '6': 'Junhu', '7': 'Julhu', '8': 'Augustu',
            '9': 'Setembru', '10': 'Outubru', '11': 'Novembru', '12': 'Dezembru'
        }
        
        fulan_nome = month_names.get(fulan, '') if fulan else ''
        
        # Safe attribute access
        munisipiu_name = munisipiu.munisipiu if munisipiu and hasattr(munisipiu, 'munisipiu') else "Hotu"
        feeder_name = feeder.naran_feeder if feeder and hasattr(feeder, 'naran_feeder') else "Hotu"
        trafo_name = trafo.zona if trafo and hasattr(trafo, 'zona') else "Hotu"
        contador_name = contador_single.nu_kontador if contador_single and hasattr(contador_single, 'nu_kontador') else "Hotu"

        print("Total Pendapatan:", total_pendapatan)
        
        context = {
            'data': data_list,
            'total_data': len(data_list),
            'total_pendapatan': f"{total_pendapatan:,.2f}",
            'munisipiu': munisipiu_name,
            'feeder': feeder_name,
            'trafo': trafo_name,
            'contador': contador_name,
            'tinan': tinan if tinan else "Hotu",
            'fulan': fulan_nome if fulan_nome else "Hotu",
        }
        
        return render(request, 'admins/report/imprimeRelatoriu.html', context)