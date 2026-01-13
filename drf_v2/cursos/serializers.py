from rest_framework import serializers
from .models import Curso, Avaliacao

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'url', 'ativo']

class AvaliacaoSerializer(serializers.HyperlinkedModelSerializer):
    curso = serializers.HyperlinkedRelatedField(
        view_name='curso-detail',
        queryset=Curso.objects.all()
    )

    class Meta:
        model = Avaliacao   
        fields = ['id', 'curso', 'nome', 'email', 'comentario', 'avaliacao', 'ativo']
