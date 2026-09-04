from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.models import Cliente, Aldeia, Tekniku, Survey, Contador, Trafo
from EDTL_API.serializers import ClienteSerializer, SurveySerializer
from app.models import Imajen
from django.utils import timezone

# View for Login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            try:
                tekniku = Tekniku.objects.get(user_id=user.id)
                tekniku_id = tekniku.id_tekniku
            except Tekniku.DoesNotExist:
                tekniku_id = None

            return Response({
                'success': True,
                'token': token.key,
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': tekniku.email,
                    'numeru': tekniku.no_tlf,
                    'enderesu':tekniku.enderesu,
                    'tekniku_id': str(tekniku_id),
                    'idtek':str(tekniku.id),
                }
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UmaView(APIView):
    def get(self, request):
        user = request.GET.get('user')
        try:
            tekniku = Tekniku.objects.get(user_id=user)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_404_NOT_FOUND)

        total_cliente = Cliente.objects.filter(tekniku=tekniku).count()
        total_contador = Contador.objects.filter(tekniku=tekniku).count()

        return Response({
            'total_cliente': total_cliente,
            'total_contador': total_contador
        }, status=status.HTTP_200_OK)

class ClienteDetailView(APIView):
    def get(self, request):
        tekniku_id = request.GET.get('tekniku_id')
        menu = request.GET.get('menu')
        try:
            if menu == 'uma':
                clientes = Cliente.objects.filter(tekniku_id=tekniku_id)[:3]
            elif menu == 'kontador':
                clientes = Cliente.objects.filter(tekniku_id=tekniku_id)
            data = []
            for cliente in clientes:
                data.append({
                    'id': cliente.id,
                    'naran': cliente.naran,
                    'id_identidade': cliente.id_identidade,
                    'naran_kompanhia': cliente.naran_kompanhia,
                    'kategoria_kliente': cliente.kategoria_kliente,
                    'hela_fatin': cliente.hela_fatin,
                    'no_tlf': cliente.no_tlf,
                    'aldeia': cliente.aldeia.naran_aldeia if cliente.aldeia else None,
                    'data_rejistu': cliente.data_rejistu,
                })
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({'success': False, 'error': 'Cliente not found'}, status=status.HTTP_404_NOT_FOUND)


# view for Aldeia
class AldeiaView(APIView):
    def get(self, request):
        aldeias = Aldeia.objects.all().order_by('naran_aldeia')
        data = [
            {
                'id': a.id,
                'naran_aldeia': a.naran_aldeia,
            }
            for a in aldeias
        ]
        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

# view for trafo
class TrafoView(APIView):
    def get(self, request):
        trafos = Trafo.objects.all().order_by('zona')
        data = [
            {
                'id': t.id,
                'zona': t.zona,
            }
            for t in trafos
        ]
        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

# View for Cliente
class ClienteView(APIView):
    def get(self, request):
        clientes = Cliente.objects.all().order_by('-created_at')
        data = []

        for c in clientes:
            data.append({
                'id': c.id,
                'naran': c.naran,
                'id_identidade': c.id_identidade,
                'naran_kompanhia': c.naran_kompanhia,
                'kategoria_kliente': c.kategoria_kliente,
                'hela_fatin': c.hela_fatin,
                'kordinat': c.kordinat,
                'no_tlf': c.no_tlf,
                'aldeia': c.aldeia.id if c.aldeia else None,
                'tekniku': c.tekniku.id if c.tekniku else None,
                'data_rejistu': c.data_rejistu,
                'created_at': c.created_at,
                'updated_at': c.updated_at,
            })

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

        try:

            # print(request.data)

            aldeia_id = request.data.get('aldeia')
            tekniku_id = request.data.get('tekniku')

            aldeia = Aldeia.objects.get(id=aldeia_id) if aldeia_id else None
            tekniku = Tekniku.objects.get(id=tekniku_id) if tekniku_id else None

            Cliente.objects.create(
                naran=request.data.get('naran'),
                id_identidade=request.data.get('id_identidade'),
                naran_kompanhia=request.data.get('naran_kompanhia'),
                kategoria_kliente=request.data.get('kategoria_kliente'),
                hela_fatin=request.data.get('hela_fatin'),
                no_tlf=request.data.get('no_tlf'),
                aldeia=aldeia,
                tekniku=tekniku,
                data_rejistu=timezone.now(),
            )

            return Response({
                'success': True,
                'message': 'Kliente kria ho susesu!',
            }, status=status.HTTP_201_CREATED)

        except Aldeia.DoesNotExist:
            return Response({'error': 'Aldeia not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# view for kontador
class KontadorView(APIView):
    def get(self, request):
        contadors = Contador.objects.all().order_by('-created_at')
        data = []

        for c in contadors:
            data.append({
                'id': c.id,
                'nu_kontador': c.nu_kontador,
                'phase': c.phase,
                'disjuntor_jeral': c.disjuntor_jeral,
                'medida_kabu': c.medida_kabu,
                'numeru_trafo': c.numeru_trafo,
                'numeru_pole': c.numeru_pole,
                'konta_tuan': c.konta_tuan,
                'ligasaun_arde': c.ligasaun_arde,
                'kordinat': c.kordinat,
                'cliente': c.cliente.id if c.cliente else None,
                'trafo': c.trafo.id if c.trafo else None,
                'tekniku': c.tekniku.id if c.tekniku else None,
            })

        return Response(data, status=status.HTTP_200_OK)

# View for Kontador By Cliente
class KontadorByClienteView(APIView):
    def get(self, request):
        cliente_id = request.GET.get('cliente_id')
        contadors = Contador.objects.filter(cliente_id=cliente_id).order_by('-created_at')
        data = []

        for c in contadors:
            data.append({
                'id': c.id,
                'nu_kontador': c.nu_kontador,
                'phase': c.phase,
                'disjuntor_jeral': c.disjuntor_jeral,
                'medida_kabu': c.medida_kabu,
                'numeru_trafo': c.numeru_trafo,
                'numeru_pole': c.numeru_pole,
                'konta_tuan': c.konta_tuan,
                'ligasaun_arde': c.ligasaun_arde,
                'kordinat': c.kordinat,
                'cliente': c.cliente.naran if c.cliente else None,
                'trafo': c.trafo.zona if c.trafo else None,
                'tekniku': c.tekniku.naran if c.tekniku else None,
            })

        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            # print(data)
            cliente = None
            trafo = None
            tekniku = None

            cliente_id = data.get('cliente')
            trafo_id = data.get('trafo')
            tekniku_id = data.get('tekniku')

            if cliente_id:
                cliente = Cliente.objects.get(id=cliente_id)
            if trafo_id:
                trafo = Trafo.objects.get(id=trafo_id)
            if tekniku_id:
                tekniku = Tekniku.objects.get(id=tekniku_id)

            contador = Contador.objects.create(
                nu_kontador=data.get('nu_kontador'),
                phase=data.get('phase'),
                disjuntor_jeral=data.get('disjuntor_jeral'),
                medida_kabu=data.get('medida_kabu'),
                numeru_trafo=data.get('numeru_trafo'),
                numeru_pole=data.get('numeru_pole'),
                konta_tuan=data.get('konta_tuan'),
                ligasaun_arde=data.get('ligasaun_arde'),
                kordinat=data.get('kordinat'),
                cliente=cliente,
                trafo=trafo,
                tekniku=tekniku,
            )

            return Response({
                'success': True,
                'message': 'Kontador kria ho susesu!',
            }, status=status.HTTP_201_CREATED)

        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Trafo.DoesNotExist:
            return Response({'error': 'Trafo not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for Survey
class SurveyView(APIView):
    def get(self, request):
        surveys = Survey.objects.all().order_by('-created_at')
        data = []

        for s in surveys:
            data.append({
                'id': s.id,
                'cliente': s.cliente.id if s.cliente else None,
                'tipu_ligasaun': s.tipu_ligasaun,
                'feeder': s.feeder,
                'nu_trafo': s.nu_trafo,
                'data_survey': s.data_survey,
                'deskrisaun_instalasaun': s.deskrisaun_instalasaun,
                'tekniku': s.tekniku.id if s.tekniku else None,
                'created_at': s.created_at,
                'updated_at': s.updated_at,
            })

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        try:
            cliente_id = data.get('cliente')
            tekniku_id = data.get('tekniku')

            cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None
            tekniku = Tekniku.objects.get(id=tekniku_id) if tekniku_id else None

            survey = Survey.objects.create(
                cliente=cliente,
                tipu_ligasaun=data.get('tipu_ligasaun'),
                feeder=data.get('feeder'),
                nu_trafo=data.get('nu_trafo'),
                data_survey=data.get('data_survey'),
                deskrisaun_instalasaun=data.get('deskrisaun_instalasaun'),
                tekniku=tekniku,
            )

            return Response({
                'success': True,
                'message': 'Survey kria ho susesu!',
                'survey': {
                    'id': survey.id,
                    'cliente': survey.cliente.id if survey.cliente else None,
                    'tipu_ligasaun': survey.tipu_ligasaun,
                    'feeder': survey.feeder,
                    'nu_trafo': survey.nu_trafo,
                    'data_survey': survey.data_survey,
                    'deskrisaun_instalasaun': survey.deskrisaun_instalasaun,
                    'tekniku': survey.tekniku.id if survey.tekniku else None,
                    'created_at': survey.created_at,
                    'updated_at': survey.updated_at,
                }
            }, status=status.HTTP_201_CREATED)

        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# View for Imajen
class ImajenView(APIView):
    def get(self, request):
        imajens = Imajen.objects.all().order_by('-created_at')
        data = [
            {
                'id': i.id,
                'foto': request.build_absolute_uri(i.foto.url) if i.foto else None,
                'cliente': i.cliente.id if i.cliente else None,
                'created_at': i.created_at,
                'updated_at': i.updated_at,
            }
            for i in imajens
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            cliente_id = request.data.get('cliente')
            foto = request.FILES.get('foto')

            if not foto:
                return Response({'error': 'Field "foto" wajib diisi.'}, status=status.HTTP_400_BAD_REQUEST)

            cliente = None
            if cliente_id:
                try:
                    cliente = Cliente.objects.get(id=cliente_id)
                except Cliente.DoesNotExist:
                    return Response({'error': 'Dadus Kliente Laiha.'}, status=status.HTTP_404_NOT_FOUND)

            imajen = Imajen.objects.create(foto=foto, cliente=cliente)

            return Response({
                'success': True,
                'message': 'Dadus Rejistu ho Susesu!',
                'imajen': {
                    'id': imajen.id,
                    'foto': request.build_absolute_uri(imajen.foto.url) if imajen.foto else None,
                    'cliente': imajen.cliente.id if imajen.cliente else None,
                    'created_at': imajen.created_at,
                    'updated_at': imajen.updated_at,
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# view for kontador
class ContadorView(APIView):
    def get(self, request):
        contadors = Contador.objects.all().order_by('-created_at')
        data = []

        for c in contadors:
            data.append({
                'id': c.id,
                'nu_kontador': c.nu_kontador,
                'phase': c.phase,
                'disjuntor_jeral': c.disjuntor_jeral,
                'medida_kabu': c.medida_kabu,
                'numeru_trafo': c.numeru_trafo,
                'numeru_pole': c.numeru_pole,
                'konta_tuan': c.konta_tuan,
                'ligasaun_arde': c.ligasaun_arde,
                'kordinat': c.kordinat,
                'cliente': c.cliente.id if c.cliente else None,
                'trafo': c.trafo.id if c.trafo else None,
                'tekniku': c.tekniku.id if c.tekniku else None,
                'created_at': c.created_at,
                'updated_at': c.updated_at,
            })

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        try:
            cliente = None
            trafo = None
            tekniku = None

            cliente_id = data.get('cliente')
            trafo_id = data.get('trafo')
            tekniku_id = data.get('tekniku')

            if cliente_id:
                cliente = Cliente.objects.get(id=cliente_id)
            if trafo_id:
                trafo = Trafo.objects.get(id=trafo_id)
            if tekniku_id:
                tekniku = Tekniku.objects.get(id=tekniku_id)

            contador = Contador.objects.create(
                nu_kontador=data.get('nu_kontador'),
                phase=data.get('phase'),
                disjuntor_jeral=data.get('disjuntor_jeral'),
                medida_kabu=data.get('medida_kabu'),
                numeru_trafo=data.get('numeru_trafo'),
                numeru_pole=data.get('numeru_pole'),
                konta_tuan=data.get('konta_tuan'),
                ligasaun_arde=data.get('ligasaun_arde'),
                kordinat=data.get('kordinat'),
                cliente=cliente,
                trafo=trafo,
                tekniku=tekniku,
            )

            return Response({
                'success': True,
                'message': 'Kontador kria ho susesu!',
                'contador': {
                    'id': contador.id,
                    'nu_kontador': contador.nu_kontador,
                    'phase': contador.phase,
                    'disjuntor_jeral': contador.disjuntor_jeral,
                    'medida_kabu': contador.medida_kabu,
                    'numeru_trafo': contador.numeru_trafo,
                    'numeru_pole': contador.numeru_pole,
                    'konta_tuan': contador.konta_tuan,
                    'ligasaun_arde': contador.ligasaun_arde,
                    'kordinat': contador.kordinat,
                    'cliente': contador.cliente.id if contador.cliente else None,
                    'trafo': contador.trafo.id if contador.trafo else None,
                    'tekniku': contador.tekniku.id if contador.tekniku else None,
                    'created_at': contador.created_at,
                    'updated_at': contador.updated_at,
                }
            }, status=status.HTTP_201_CREATED)

        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Trafo.DoesNotExist:
            return Response({'error': 'Trafo not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for Survey By Cliente
class SurveyByClienteView(APIView):
    def get(self, request):
        cliente_id = request.GET.get('cliente_id')
        surveys = Survey.objects.filter(cliente_id=cliente_id).order_by('-created_at')
        data = []

        for s in surveys:
            data.append({
                'id': str(s.id),
                'tipu_ligasaun': s.tipu_ligasaun,
                'feeder': s.feeder,
                'nu_trafo': s.nu_trafo,
                'data_survey': s.data_survey,
                'deskrisaun_instalasaun': s.deskrisaun_instalasaun,
                'cliente': s.cliente.naran if s.cliente else None,
                'tekniku': s.tekniku.naran if s.tekniku else None,
            })

        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            cliente = None
            tekniku = None

            cliente_id = data.get('cliente')
            tekniku_id = data.get('tekniku')

            if cliente_id:
                cliente = Cliente.objects.get(id=cliente_id)
            if tekniku_id:
                tekniku = Tekniku.objects.get(id=tekniku_id)

            survey = Survey.objects.create(
                cliente=cliente,
                tipu_ligasaun=data.get('tipu_ligasaun'),
                feeder=data.get('feeder'),
                nu_trafo=data.get('nu_trafo'),
                data_survey=data.get('data_survey'),
                deskrisaun_instalasaun=data.get('deskrisaun_instalasaun'),
                tekniku=tekniku,
            )

            return Response({
                'success': True,
                'message': 'Survey kria ho susesu!',
            }, status=status.HTTP_201_CREATED)

        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Tekniku.DoesNotExist:
            return Response({'error': 'Tekniku not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for Imajen Kontador By Cliente
class ImajenKontadorByClienteView(APIView):
    def get(self, request):
        cliente_id = request.GET.get('cliente_id')
        imajens = Imajen.objects.filter(cliente_id=cliente_id).order_by('-created_at')
        data = []

        for i in imajens:
            data.append({
                'id': str(i.id),
                'foto': request.build_absolute_uri(i.foto.url) if i.foto else None,
                'cliente': i.cliente.naran if i.cliente else None,
            })

        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            cliente_id = request.data.get('cliente')
            foto = request.FILES.get('foto')

            if not foto:
                return Response({'error': 'Field "foto" wajib diisi.'}, status=status.HTTP_400_BAD_REQUEST)

            cliente = None
            if cliente_id:
                try:
                    cliente = Cliente.objects.get(id=cliente_id)
                except Cliente.DoesNotExist:
                    return Response({'error': 'Dadus Kliente Laiha.'}, status=status.HTTP_404_NOT_FOUND)

            imajen = Imajen.objects.create(foto=foto, cliente=cliente)

            return Response({
                'success': True,
                'message': 'Dadus Rejistu ho Susesu!',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

