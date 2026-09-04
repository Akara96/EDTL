from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count
from app.models import KordinatFeeder, Feeder, Trafo, Munisipiu
from django.core.exceptions import ObjectDoesNotExist
from app.forms import *
from app.utils import decode_id, encode_id
from django.db import connection

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def showDadus(request):

    dadus = KordinatFeeder.objects.select_related("feeder")
    dadus_list = [
        {
            "id": kf.id,
            "kordinat": kf.kordinat,
            "feeder": {
                "feeder_id": encode_id(kf.feeder.id) if kf.feeder else None,
                "naran_feeder": kf.feeder.naran_feeder if kf.feeder else None
            }
        }
        for kf in dadus
    ]

    munisipiu = Munisipiu.objects.all()

    context = {
        'title':'Ligasaun Feeder',
        'act':'show',
        'dadus': dadus_list,
        'munisipiu': munisipiu,
        'current_tab': 'tab_ligasaunfeeder',
    }
    return render(request, 'admins/page/feeder.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def feederDetail(request, id):
    try:
        decode = decode_id(id)
        kordinat_feeder_qs = KordinatFeeder.objects.filter(feeder_id=decode).select_related("feeder")
        kordinat_feeder = [
            {
            "id": kf.id,
            "kordinat": kf.kordinat,
            "feeder": {
                "naran_feeder": kf.feeder.naran_feeder if kf.feeder else None
            }
            }
            for kf in kordinat_feeder_qs
        ]
    except KordinatFeeder.DoesNotExist:
        messages.error(request, 'Kordinat Feeder La Hetan!')
        return redirect('app:ligasaunFeeder')

    feeders = Feeder.objects.get(id=decode)
    
    context = {
        'title':'Ligasaun Feeder',
        'act':'detailligasaun',
        'dadus': feeders,
        'kordinat_feeder': kordinat_feeder,
        'current_tab': 'tab_ligasaunfeeder',
    }

    return render(request, 'admins/page/feeder.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def feederDetails(request, id):
    try:
        decode = decode_id(id)
        kordinat_feeder_qs = KordinatFeeder.objects.filter(feeder_id=decode).select_related("feeder")
        kordinat_feeder = [
            {
            "id": kf.id,
            "kordinat": kf.kordinat,
            "feeder": {
                "naran_feeder": kf.feeder.naran_feeder if kf.feeder else None
            }
            }
            for kf in kordinat_feeder_qs
        ]
    except KordinatFeeder.DoesNotExist:
        messages.error(request, 'Kordinat Feeder La Hetan!')
        return redirect('app:ligasaunFeeder')

    feeders = Feeder.objects.get(id=decode)
    
    context = {
        'title':'Ligasaun Feeder',
        'act':'detailligasaunfeeder',
        'dadus': feeders,
        'kordinat_feeder': kordinat_feeder,
        'current_tab': 'tab_ligasaunfeeder',
    }

    return render(request, 'admins/page/feeder.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addDadus(request):
    feeders = Feeder.objects.all()
    trafos = Trafo.objects.all()
    if request.method == 'POST':
        feeder_id = request.POST.get('feeder')
        kordinat_raw = request.POST.get('kordinat', '').strip()
        if not feeder_id or not kordinat_raw:
            messages.error(request, 'Favor Prienxe Feeder no lista kordinat')
            return redirect('app:ligasaunFeeder')

        try:
            feeder = Feeder.objects.get(id=feeder_id)
        except Feeder.DoesNotExist:
            messages.error(request, 'Feeder Laiha.')
            return redirect('app:ligasaunFeeder')

        # Dukungan input multiline (textarea) berisi banyak baris:
        # -8.634163,125.456432
        # -8.624659,125.769595
        lines = [l.strip() for l in kordinat_raw.replace('\r', '').split('\n') if l.strip()]
        if not lines:
            messages.error(request, 'Laiha Kordinat Validu')
            return redirect('app:ligasaunFeeder')

        created = 0
        skipped = 0
        for line in lines:
            # Expected format: lat,lon
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 2:
                skipped += 1
                continue
            try:
                lat = float(parts[0])
                lon = float(parts[1])
            except ValueError:
                skipped += 1
                continue

            KordinatFeeder.objects.create(
                feeder=feeder,
                kordinat=f"{lat},{lon}"
            )
            created += 1

        if created:
            msg = f'Pontu {created} Adisiona ho Susesu'
            if skipped:
                msg += f' {skipped} linha kordinat (formatu la validu).'
            messages.success(request, msg)
        else:
            messages.error(request, 'Kordinat hotu la validu')
        return redirect('app:ligasaunFeeder')
    
    context = {
        'title': 'Add Ligasaun Feeder',
        'act': 'inputligasaun',
        'dadus': feeders,
    }
    return render(request, 'admins/page/feeder.html', context)



# Konsepnya:

# Koordinat lama (kordinat_tuan) → dari DB, posisi awal.

# Koordinat baru (kordinat) → hasil polyline setelah user drag / add.

# Langkahnya:

# Bandingkan koordinat lama vs koordinat baru per posisi:

# Jika posisi baru beda dari koordinat lama → update di DB.

# Jika posisi baru sama dengan koordinat lama → tidak perlu update.

# Titik baru (kordinat yang tidak ada di kordinat_tuan) → buat entry baru di DB.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editDadus(request, id):
    try:
        decode = decode_id(id)
        kordinat_feeder_qs = KordinatFeeder.objects.filter(feeder_id=decode).select_related("feeder")
        kordinat_feeder = [
            {
            "id": kf.id,
            "kordinat": kf.kordinat,
            "feeder": {
                "naran_feeder": kf.feeder.naran_feeder if kf.feeder else None
            }
            }
            for kf in kordinat_feeder_qs
        ]
    except KordinatFeeder.DoesNotExist:
        messages.error(request, 'Kordinat Feeder La Hetan!')
        return redirect('app:ligasaunFeeder')

    feeders = Feeder.objects.get(id=decode)

    if request.method == 'POST':
        feeder_id = request.POST.get('feeder')
        kordinat_raw = request.POST.get('kordinat', '').strip()
        kordinat_tuan_raw = request.POST.get('kordinat_tuan', '').strip()

        feeder = Feeder.objects.get(id=feeder_id)

        # Parse koordinat baru
        kordinat_new = []
        for line in kordinat_raw.splitlines():
            line = line.strip()
            if not line: continue
            lat, lon = map(float, line.split(','))
            kordinat_new.append((round(lat,6), round(lon,6)))

        # Parse koordinat lama
        kordinat_old = []
        for line in kordinat_tuan_raw.splitlines():
            line = line.strip()
            if not line: continue
            lat, lon = map(float, line.split(','))
            kordinat_old.append((round(lat,6), round(lon,6)))

        created = 0
        updated = 0

        # Update koordinat lama yang diubah
        for idx, old_coord in enumerate(kordinat_old):
            if idx < len(kordinat_new):
                new_coord = kordinat_new[idx]
                if new_coord != old_coord:  # Hanya update kalau di-drag
                    kf = KordinatFeeder.objects.filter(feeder=feeder, kordinat=f"{old_coord[0]},{old_coord[1]}").first()
                    if kf:
                        kf.kordinat = f"{new_coord[0]},{new_coord[1]}"
                        kf.save()
                        updated += 1

        # Tambah koordinat baru yang melebihi jumlah koordinat lama
        for new_coord in kordinat_new[len(kordinat_old):]:
            KordinatFeeder.objects.create(feeder=feeder, kordinat=f"{new_coord[0]},{new_coord[1]}")
            created += 1

        msg = []
        if updated: msg.append(f'Pontu Tuan {updated} Atualiza ho Susesu')
        if created: msg.append(f'Pontu Foun {created} Adisiona ho Susesu')
        messages.success(request, ' | '.join(msg) or 'Laiha Mudansa.')

        return redirect('app:ligasaunFeeder')


    context = {
        'title': 'Edit Ligasaun Feeder',
        'act': 'editligasaun',
        'feeder': feeders,
        'dadus': Feeder.objects.all(),
        'kordinat_feeder': kordinat_feeder,
    }
    return render(request, 'admins/page/feeder.html', context)