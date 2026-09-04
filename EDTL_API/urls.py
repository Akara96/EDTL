from django.urls import path
from EDTL_API.views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('rejistukliente', ClienteView.as_view(), name='rejistukliente'),
    path('rejistusurvey', SurveyView.as_view(), name='rejistusurvey'),
    path('rejistuimajen', ImajenView.as_view(), name='rejistuimajen'),
    path('rejistukontador', ContadorView.as_view(), name='rejistukontador'),
    path('getUma', UmaView.as_view(), name='getUma'),
    path('getDetailCliente', ClienteDetailView.as_view(), name='getDetailCliente'),
    path('getAldeia', AldeiaView.as_view(), name='getAldeia'),
    path('getKontadorByKliente', KontadorByClienteView.as_view(), name='getKontadorByKliente'),
    path('getTrafo', TrafoView.as_view(), name='getTrafo'),
    path('postKontador', KontadorByClienteView.as_view(), name='postKontador'),
    path('getSurvey', SurveyByClienteView.as_view(), name='getSurvey'),
    path('postSurvey', SurveyByClienteView.as_view(), name='postSurvey'),
    path('getImajenKontador', ImajenKontadorByClienteView.as_view(), name='getImajenKontador'),
    path('postImajenKontador', ImajenKontadorByClienteView.as_view(), name='postImajenKontador'),
]