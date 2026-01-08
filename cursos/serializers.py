from rest_framework import serializers
from .models import Curso, Avaliacao

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'url', 'ativo']

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'curso': {'write_only': True}
        }
        model = Avaliacao   
        fields = ['id', 'curso', 'nome', 'email', 'comentario', 'avaliacao', 'ativo']
