from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import now as tz_now
from pytz import timezone as pytz_timezone

def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect('app:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Favor prienxe lai username no password')
            return render(request, 'admins/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['id_user'] = user.id
            request.session['username'] = user.username
            login(request, user)
            return redirect('app:home')
        else:
            messages.error(request, 'Username no Password laloos.')
            return render(request, 'admins/login.html')

    return render(request, 'admins/login.html')

@login_required
def home(request):
    """
    Renders the admin dashboard with optional filters.
    """
    # Ambil filter dari GET
    data = request.GET.get('data')        # format: YYYY-MM-DD
    tinan = request.GET.get('tinan')      # year
    fulan = request.GET.get('fulan')      # month

    dili_tz = pytz_timezone('Asia/Dili')
    current_dt = tz_now().astimezone(dili_tz)

    # Default filter
    year = int(tinan) if tinan and tinan.isdigit() else current_dt.year
    month = int(fulan) if fulan and fulan.isdigit() else current_dt.month

    # Filter Contador berdasarkan tanggal atau tahun/bulan
    contador_qs = Contador.objects.all()

    if data:
        # Filter by specific date
        contador_qs = contador_qs.filter(created_at__date=data)
    else:
        # Filter by year and month
        contador_qs = contador_qs.filter(
            created_at__year=year,
            created_at__month=month
        )

    # Total Montajen berdasarkan filter
    total_montajen = contador_qs.count()

    # Total Kliente tetap seluruh data
    total_kliente = Cliente.objects.count()

    # Kontador by Munisipiu
    kontadorbymapa = contador_qs.values(
        'trafo__feeder__munisipiu__id',
        'trafo__feeder__munisipiu__munisipiu',
        'trafo__feeder__munisipiu__area',
        'trafo__feeder__munisipiu__kodigu',
        'trafo__feeder__munisipiu__inline_color',
        'trafo__feeder__munisipiu__outline_color'
    ).annotate(
        kontador_count=Count('id')
    )

    listatinan = Contador.objects.dates('created_at', 'year', order='DESC').distinct().values_list('created_at__year', flat=True)

    listafulan = [
        ("01", "Janeiru"),
        ("02", "Fevereiru"),
        ("03", "Marsu"),
        ("04", "Abril"),
        ("05", "Maiu"),
        ("06", "Junhu"),
        ("07", "Julhu"),
        ("08", "Agostu"),
        ("09", "Setembru"),
        ("10", "Outubru"),
        ("11", "Novembru"),
        ("12", "Dezembru"),
    ]

    context = {
        'totalKliente': total_kliente,
        'totalMontajen': total_montajen,
        'kontadorbymapa': list(kontadorbymapa),
        'filter_data': data,
        'filter_year': year,
        'filter_month': month,
        'listaTinan':listatinan,
        'listaFulan':list(listafulan),
    }

    return render(request, 'admins/main.html', context)


@login_required
def countPediduByStatus(request):
    """
    Returns JSON with counts of Kliente Pedidu by status.
    """
    dili_tz = pytz_timezone('Asia/Dili')
    today = tz_now().astimezone(dili_tz).date()
    count = RejistuKontadorFoun.objects.filter(created_at__date=today, status=1).count()
    return JsonResponse({'count': count})


@login_required
def kontadorByMun(request, id):
    """
    Returns JSON with coordinates of Kontador filtered by munisipiu id.
    """
    dili_tz = pytz_timezone('Asia/Dili')
    now = timezone.now().astimezone(dili_tz)
    
    # Get all contador for the selected munisipiu
    kontador_list = Contador.objects.filter(
        trafo__feeder__munisipiu__id=id,
        created_at__year=now.year,
        created_at__month=now.month
    ).select_related(
        'cliente',
        'trafo__feeder__munisipiu',
        'tekniku'
    ).prefetch_related(
        'cliente__aldeia__suku__postu',
        'cliente__imajen_set'  # Prefetch semua gambar kliente
    )

    print(f"Found {kontador_list.count()} contadores for munisipiu id {id}")

    coordinates = []
    for k in kontador_list:
        if k.kordinat is not None:
            # Get related cliente data
            cliente_data = {}
            if k.cliente:
                cliente_data = {
                    "naran": k.cliente.naran,
                    "id_identidade": k.cliente.id_identidade,
                    "naran_kompanhia": k.cliente.naran_kompanhia,
                    "kategoria_kliente": k.cliente.kategoria_kliente,
                    "hela_fatin": k.cliente.hela_fatin,
                    "no_tlf": k.cliente.no_tlf,
                    "email": k.cliente.email if hasattr(k.cliente, 'email') else '',
                    "data_rejistu": k.cliente.data_rejistu.strftime('%Y-%m-%d') if k.cliente.data_rejistu else '',
                }
                
                # Get aldeia hierarchy
                if k.cliente.aldeia:
                    aldeia = k.cliente.aldeia
                    suku = aldeia.suku if aldeia.suku else None
                    postu = suku.postu if suku else None
                    
                    cliente_data.update({
                        "aldeia": aldeia.naran_aldeia if aldeia else '',
                        "suku": suku.suku if suku else '',
                        "postu": postu.postu if postu else '',
                        "endereco": f"{aldeia.naran_aldeia if aldeia else ''}, "
                                   f"{suku.suku if suku else ''}, "
                                   f"{postu.postu if postu else ''}",
                    })
            
            # Get contador data
            contador_data = {
                "nu_kontador": k.nu_kontador,
                "phase": k.phase,
                "disjuntor_jeral": k.disjuntor_jeral,
                "medida_kabu": k.medida_kabu,
                "numeru_trafo": k.numeru_trafo,
                "numeru_pole": k.numeru_pole,
                "konta_tuan": k.konta_tuan,
                "ligasaun_arde": k.ligasaun_arde,
                "kordinat": k.kordinat,
            }
            
            # Get tekniku data
            tekniku_data = {}
            if k.tekniku:
                tekniku_data = {
                    "tekniku_naran": k.tekniku.naran,
                    "tekniku_endereco": k.tekniku.enderesu,
                    "tekniku_email": k.tekniku.email,
                    "tekniku_telefone": k.tekniku.no_tlf,
                }
            
            # Get trafo data
            trafo_data = {}
            if k.trafo:
                trafo_data = {
                    "trafo_zona": k.trafo.zona,
                    "trafo_kordinat": k.trafo.kordinat,
                }
            
            # Get ALL imajen data for this cliente
            imajen_data = []
            try:
                # Get all images for this cliente
                imajens = Imajen.objects.filter(cliente=k.cliente)
                for imajen in imajens:
                    if imajen.foto:
                        imajen_data.append({
                            "id": imajen.id,
                            "imajen_url": imajen.foto.url,
                            "imajen_nome": imajen.foto.name,
                            "imajen_filename": imajen.foto.name.split('/')[-1] if '/' in imajen.foto.name else imajen.foto.name,
                            "created_at": imajen.created_at.strftime('%Y-%m-%d %H:%M:%S') if imajen.created_at else '',
                            "observasaun": f"Imajen {len(imajen_data) + 1} husi cliente {k.cliente.naran}" if k.cliente else f"Imajen {len(imajen_data) + 1}",
                        })
            except Exception as e:
                print(f"Error loading images for cliente {k.cliente.id if k.cliente else 'N/A'}: {e}")
            
            # Check if cliente has survey
            survey_data = {}
            try:
                survey = Survey.objects.filter(cliente=k.cliente).first()
                if survey:
                    survey_data = {
                        "tipu_ligasaun": survey.tipu_ligasaun,
                        "feeder": survey.feeder,
                        "nu_trafo": survey.nu_trafo,
                        "data_survey": survey.data_survey.strftime('%Y-%m-%d') if survey.data_survey else '',
                        "deskrisaun_instalasaun": survey.deskrisaun_instalasaun,
                        "kalkulasaun": survey.kalkulasaun(),
                    }
            except Exception as e:
                print(f"Error loading survey for cliente {k.cliente.id if k.cliente else 'N/A'}: {e}")
            
            # Combine all data
            coordinate_data = {
                "id": k.id,
                "contador": contador_data,
                "cliente": cliente_data,
                "tekniku": tekniku_data,
                "trafo": trafo_data,
                "imajen": imajen_data,  # Sekarang berupa array/list
                "survey": survey_data,
                "created_at": k.created_at.strftime('%Y-%m-%d %H:%M:%S') if k.created_at else '',
                "total_imajen": len(imajen_data),  # Menambahkan jumlah total gambar
            }
            
            coordinates.append(coordinate_data)

    response = {
        "munisipiu_id": id,
        "munisipiu_name": kontador_list.first().trafo.feeder.munisipiu.munisipiu if kontador_list and kontador_list.first().trafo.feeder.munisipiu else '',
        "total": len(coordinates),
        "coordinates": coordinates
    }

    return JsonResponse(response, safe=False)


def logoutUser(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request,'Successfuly logged out')
    return redirect('app:login')
