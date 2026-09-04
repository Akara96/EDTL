from django.urls import path
from app.views import indexViews, viewsAdmin, userViews, munisipiuViews, teknikuViews, klienteViews, feederViews, ligasaunFeederViews, trafoViews, kontadorViews, seluViews, relatoriuViews, aiViews

app_name = 'app'

urlpatterns = [
    # VIZITOR
    path('', indexViews.index, name='index'),
    path('gmaillogin', indexViews.gmail_login, name='logingmail'),
    path('auth/google/callback/', indexViews.google_callback, name='google_callback'),
    path('keixa/', indexViews.husu_keixa, name='husu_keixa'),
    
    # API Públiku
    path('api/public-chat/', aiViews.public_chat_api, name='public_chat_api'),
    # VIZITOR

    # ADMIN
    path('login/', viewsAdmin.login_view, name='login'),
    path('home/', viewsAdmin.home, name='home'),
    path('pediducount/', viewsAdmin.countPediduByStatus, name='pediducount'),
    path('kontadorByMunisipiu/<int:id>/', viewsAdmin.kontadorByMun, name='kontadorByMunisipiu'),

    path('user/', userViews.showUser, name='user'),
    path('permisaun/', userViews.setPermission, name='permisaun'),
    path('addUser/', userViews.addUser, name='addUser'),
    path('setPassword/<str:id>/', userViews.setPassword, name='setPassword'),
    path('editUser/<str:id>/', userViews.editUser, name='editUser'),
    path('resetPassword/<str:id>/', userViews.resetPassword, name='resetPassword'),
    path('changePassword/<str:id>/', userViews.changePassword, name='changePassword'),
    path('konta/<str:id>/', userViews.showKontaUser, name='konta'),

    path('munisipiu/', munisipiuViews.showMunisipiu, name='munisipiu'),
    path('addMunisipiu/', munisipiuViews.addMunisipiu, name='addMunisipiu'),
    path('editMunisipiu/<str:id>/', munisipiuViews.editMunisipiu, name='editMunisipiu'),
    path('detailMunisipiu/<str:id>/', munisipiuViews.detailMunisipiu, name='detailMunisipiu'),

    path('tekniku/', teknikuViews.showDadus, name='tekniku'),
    path('addTekniku/', teknikuViews.addTekniku, name='addTekniku'),
    path('editTekniku/<str:id>/', teknikuViews.editTekniku, name='editTekniku'),

    
    
    path('kliente/', klienteViews.showKliente, name='kliente'),
    path('kliente/pedidu', klienteViews.showKlientePedidu, name='klientePedidu'),
    path('sendEmail/<str:id>', klienteViews.sendEmail, name='sendEmail'),
    path('kliente/final', klienteViews.showKlienteFinal, name='klienteFinal'),
    path('editKlientefinal/<str:id>', klienteViews.editKlientefinal, name='editKlientefinal'),
    path('klientefinalKontador/<str:id>', klienteViews.KlientefinalKontador, name='klientefinalKontador'),
    path('klientefinalKontadorImajen/<str:id>', klienteViews.KlientefinalKontadorImajen, name='klientefinalKontadorImajen'),    
    

    path('feeder/', feederViews.showFeeder, name='feeder'),
    path('addFeeder/', feederViews.addFeeder, name='addFeeder'),
    path('editFeeder/<str:id>/', feederViews.editFeeder, name='editFeeder'),
    path('detailLigasaunFeeder/<str:id>/', ligasaunFeederViews.feederDetails, name='detailLigasaunFeeder'),
    

    path('ligasaunFeeder/', ligasaunFeederViews.showDadus, name='ligasaunFeeder'),
    path('addLigasaun/', ligasaunFeederViews.addDadus, name='addLigasaun'),
    path('editLigasaun/<str:id>/', ligasaunFeederViews.editDadus, name='editLigasaun'),
    path('detailLigasaun/<str:id>/', ligasaunFeederViews.feederDetail, name='detailLigasaun'),
    path('editLigasaun/<str:id>/', ligasaunFeederViews.editDadus, name='editLigasaun'),

    path('trafo/', trafoViews.showDadus, name='trafo'),
    path('addTrafo/', trafoViews.addDadus, name='addTrafo'),
    path('editTrafo/<str:id>/', trafoViews.editTrafo, name='editTrafo'),
    path('detailTrafo/<str:id>/', trafoViews.detailTrafo, name='detailTrafo'),

    path('kontador/', kontadorViews.showDadus, name='kontador'),

    path('pagamento/', seluViews.showDadus, name='pagamento'),
    path('addPagamentu/', seluViews.addDadus, name='addPagamentu'),    
    path('editPagamentu/<str:id>',seluViews.editDadus, name='editPagamentu'),
    path('getSurveyData/<str:id>',seluViews.getSurvey, name='getSurveyData'),
    path('imprimePagemento/<str:id>',seluViews.imprimePaga, name='imprimePagemento'),

    path('relatoriu/', relatoriuViews.showForm, name='relatoriu'),
    path('getFeeder/', relatoriuViews.showFeeder, name='getFeeder'),
    path('getDetailFeeder/', relatoriuViews.getDetailFeeders, name='getDetailFeeder'),
    path('getTrafo/', relatoriuViews.getTrafos, name='getTrafo'),
    path('getDetailTrafo/', relatoriuViews.getDetailTrafos, name='getDetailTrafo'),
    path('getContador/', relatoriuViews.getContadors, name='getContador'),
    path('getDetailContador/', relatoriuViews.getDetailContadors, name='getDetailContador'),
    path('imprimeRelatoriu/', relatoriuViews.imprimeRelatoriu, name='imprimeRelatoriu'),
    
    
    path('logout/', viewsAdmin.logoutUser, name='logout'),
    
    # ADMIN
]
