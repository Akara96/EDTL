from rest_framework import serializers
from app.models import (
    Tekniku, Feeder, KordinatFeeder, Trafo,
    Cliente, RejistuKontadorFoun, Selu, Survey, Imajen, Contador
)

class TeknikuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tekniku
        fields = '__all__'

class FeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeder
        fields = '__all__'

class KordinatFeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = KordinatFeeder
        fields = '__all__'

class TrafoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trafo
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class RejistuKontadorFounSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejistuKontadorFoun
        fields = '__all__'

class SeluSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selu
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class ImajenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imajen
        fields = '__all__'

class ContadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contador
        fields = '__all__'
