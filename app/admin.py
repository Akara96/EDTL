from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Munisipiu, Postu, Suku, Aldeia, Tekniku, Feeder, Trafo, Contador, Cliente, RejistuKontadorFoun, Imajen, Keixa

class MunisipiuResource(resources.ModelResource):
    class Meta:
        model = Munisipiu

@admin.register(Munisipiu)
class MunisipiuAdmin(ImportExportModelAdmin):
    resource_class = MunisipiuResource
    list_display = ('id', 'munisipiu')
    search_fields = ('munisipiu',)

class PostuResource(resources.ModelResource):
    class Meta:
        model = Postu

@admin.register(Postu)
class PostuAdmin(ImportExportModelAdmin):
    resource_class = PostuResource
    list_display = ('id', 'postu', 'munisipiu')
    search_fields = ('postu',)
    list_filter = ('munisipiu',)

class SukuResource(resources.ModelResource):
    class Meta:
        model = Suku

@admin.register(Suku)
class SukuAdmin(ImportExportModelAdmin):
    resource_class = SukuResource
    list_display = ('id', 'suku', 'postu')
    search_fields = ('suku',)
    list_filter = ('postu',)

class AldeiaResource(resources.ModelResource):
    class Meta:
        model = Aldeia

@admin.register(Aldeia)
class AldeiaAdmin(ImportExportModelAdmin):
    resource_class = AldeiaResource
    list_display = ('id', 'naran_aldeia', 'suku')
    search_fields = ('naran_aldeia',)
    list_filter = ('suku',)

class MembroResource(resources.ModelResource):
    class Meta:
        model = Tekniku

@admin.register(Tekniku)
class MembroAdmin(ImportExportModelAdmin):
    resource_class = MembroResource
    list_display = ('id_tekniku', 'naran', 'enderesu', 'email', 'no_tlf')
    search_fields = ('naran', 'email')
    list_filter = ('enderesu',)

class FeederResource(resources.ModelResource):
    class Meta:
        model = Feeder

@admin.register(Feeder)
class FeederAdmin(ImportExportModelAdmin):
    resource_class = FeederResource
    list_display = ('id', 'naran_feeder')
    search_fields = ('naran_feeder',)

class TrafoResource(resources.ModelResource):
    class Meta:
        model = Trafo

@admin.register(Trafo)
class TrafoAdmin(ImportExportModelAdmin):
    resource_class = TrafoResource
    list_display = ('id', 'kordinat', 'zona', 'feeder')
    search_fields = ('zona',)
    list_filter = ('feeder',)

class ContadorResource(resources.ModelResource):
    class Meta:
        model = Contador

@admin.register(Contador)
class ContadorAdmin(ImportExportModelAdmin):
    resource_class = ContadorResource
    list_display = ('id', 'nu_kontador', 'phase','disjuntor_jeral')
    search_fields = ('nu_kontador',)
    # list_filter = ('cliente',)

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = ('id', 'naran', 'id_identidade', 'naran_kompanhia', 'kategoria_kliente', 'hela_fatin', 'no_tlf', 'aldeia')
    search_fields = ('naran', 'no_tlf')

class RejistuKontadorFounResource(resources.ModelResource):
    class Meta:
        model = RejistuKontadorFoun

@admin.register(RejistuKontadorFoun)
class RejistuKontadorFounAdmin(ImportExportModelAdmin):
    resource_class = RejistuKontadorFounResource
    list_display = ('id', 'naran_kliente', 'numeru', 'email','aldeia', 'data_pedidu', 'status')
    search_fields = ('naran_kliente',)
    # list_filter = ('contador', 'foun')

class ImajenResource(resources.ModelResource):
    class Meta:
        model = Imajen

@admin.register(Imajen)
class ImajenAdmin(ImportExportModelAdmin):
    resource_class = ImajenResource
    list_display = ('id', 'foto', 'cliente')
    search_fields = ('cliente',)

class KeixaResource(resources.ModelResource):
    class Meta:
        model = Keixa

@admin.register(Keixa)
class KeixaAdmin(ImportExportModelAdmin):
    resource_class = KeixaResource
    list_display = ('kodigu_keixa', 'cliente', 'kategoria', 'status', 'tekniku', 'data_keixa')
    search_fields = ('kodigu_keixa', 'cliente__naran')
    list_filter = ('status', 'kategoria', 'tekniku')