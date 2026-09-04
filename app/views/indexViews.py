from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from app.models import Aldeia, RejistuKontadorFoun, Munisipiu, Contador, Keixa
from django.db.models import Count
from datetime import date
from django.contrib import messages

def index(request):
    if request.method == "POST":
        name = request.POST.get('naran')
        numeru = request.POST.get('numeru')
        email = request.POST.get('email')
        aldeia_id = request.POST.get('aldeia')
        aldeia_instance = get_object_or_404(Aldeia, pk=aldeia_id)

        # 🔍 cek apakah sudah ada request hari ini dari email yang sama
        exists_today = RejistuKontadorFoun.objects.filter(
            email=email,
            data_pedidu=date.today()
        ).exists()

        if exists_today:
            messages.error(request, "Ita-boot halo ona pedidu ohin loron no ami-nia ekipa sei kontaktu ita-boot liuhusi email")
        else:
            RejistuKontadorFoun.objects.create(
                naran_kliente=name,
                numeru=numeru,
                email=email,
                aldeia=aldeia_instance,
                data_pedidu=date.today(),
                status=1,
            )
            messages.success(request, "Pedidu Haruka ona ho Susesu")
            return redirect('app:index')

    munisipiu = Munisipiu.objects.annotate(
        num_contadors=Count('feeder__trafo__contador')
    ).values('munisipiu', 'num_contadors')

    print(list(munisipiu))

    labels = []
    data = []
    
    # Inisialisasi variabel untuk max dan min
    max_value = 0
    min_value = 0
    max_munisipiu = ""
    min_munisipiu = ""

    # Iterasi untuk mengumpulkan data dan mencari max/min
    for idx, m in enumerate(munisipiu):
        labels.append(m['munisipiu'])
        data.append(m['num_contadors'])
        
        # Cari nilai max
        if idx == 0 or m['num_contadors'] > max_value:
            max_value = m['num_contadors']
            max_munisipiu = m['munisipiu']
        
        # Cari nilai min
        if idx == 0 or m['num_contadors'] < min_value:
            min_value = m['num_contadors']
            min_munisipiu = m['munisipiu']

    context = {
        'data': Aldeia.objects.all(),
        'munisipiu_data': list(munisipiu),
        'chart_labels': labels,
        'chart_data': data,
        'total_contador': sum(data),
        'max_value': max_value,
        'max_munisipiu': max_munisipiu,
        'min_value': min_value,
        'min_munisipiu': min_munisipiu,
        'num_munisipiu': len(labels)  # Jumlah total munisipiu
    }
    
    print(f"Max: {max_munisipiu} = {max_value}")
    print(f"Min: {min_munisipiu} = {min_value}")
    
    return render(request, 'vizitor/vizitor.html', context)

def gmail_login(request):
    """
    Redirects the user to Google's OAuth 2.0 server for authentication.
    """
    # Note: You need to configure GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI in your settings.py
    # You also need to create a callback view to handle the response from Google.
    import urllib.parse

    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    params = {
        "response_type": "code",
        "client_id": '154642807373-s1gish81oqtq0d1m9rbgmk00r5mbarbq.apps.googleusercontent.com',
        "redirect_uri": 'http://127.0.0.1:8000/auth/google/callback',
        "scope": scope,
        "access_type": "offline",
        "include_granted_scopes": "true",
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


def google_callback(request):
    """
    Handles the callback from Google's OAuth 2.0 server after user authentication.
    """
    code = request.GET.get('code')
    if not code:
        # Handle the error case where no code is provided
        return redirect('app:index')

    # Exchange authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": '154642807373-s1gish81oqtq0d1m9rbgmk00r5mbarbq.apps.googleusercontent.com',
        "client_secret": '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',  # Store this in your settings.py
        "redirect_uri": 'http://127.0.0.1:8000/auth/google/callback',
        "grant_type": "authorization_code",
    }
    
    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()  # Raise an exception for bad status codes
        token_json = token_response.json()
    except requests.exceptions.RequestException as e:
        # Handle error in token exchange
        # You might want to log this error
        return redirect('app:index')

    access_token = token_json.get('access_token')
    if not access_token:
        return redirect('app:index')

    # Use the access token to get user information
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()
    except requests.exceptions.RequestException as e:
        # Handle error in fetching user info
        return redirect('app:index')

    email = user_info.get('email')
    if not email:
        return redirect('app:index')

    # Get or create the user in your database
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Create a new user if one doesn't exist
        username = email.split('@')[0]
        # Ensure username is unique
        if User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count()}"
            
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=user_info.get('given_name', ''),
            last_name=user_info.get('family_name', '')
        )
        user.set_unusable_password()
        user.save()

    # Log the user in
    login(request, user)

    return redirect('app:index')

def husu_keixa(request):
    if request.method == "POST":
        nu_kontador = request.POST.get('nu_kontador')
        kategoria = request.POST.get('kategoria')
        deskrisaun = request.POST.get('deskrisaun')
        foto = request.FILES.get('foto')

        # Find the customer by meter number
        try:
            contador = Contador.objects.get(nu_kontador=nu_kontador)
            cliente = contador.cliente

            # Create Keixa
            keixa = Keixa.objects.create(
                cliente=cliente,
                kategoria=kategoria,
                deskrisaun=deskrisaun,
                foto=foto,
                status='pendente'
            )
            
            # Generate ID
            keixa.kodigu_keixa = f"KX-{keixa.id:04d}"
            keixa.save()

            messages.success(request, f"Keixa haruka ona ho susesu! Ita-nia numeru tiket mak: {keixa.kodigu_keixa}")
            return redirect('app:husu_keixa')

        except Contador.DoesNotExist:
            messages.error(request, "Numeru Kontador la rona iha sistema. Favor verifika fali.")
            return redirect('app:husu_keixa')
            
    # For GET request
    kategoria_choices = Keixa.KATEGORIA_CHOICES
    
    context = {
        'kategoria_choices': kategoria_choices
    }
    return render(request, 'vizitor/keixa.html', context)