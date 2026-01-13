from rest_framework import generics
from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import AvaliacaoPagination

# ============================== API V1 ==============================


# CRUD de Cursos - GET e POST
class CursosAPIView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Restante do CRUD de Cursos - GET, PUT, DELETE
class CursoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AvaliacoesAPIView(generics.ListCreateAPIView):
    # Define o conjunto base de dados para as avaliações
    queryset = Avaliacao.objects.all()

    # validar dados de entrada
    # transformar objetos em JSON
    serializer_class = AvaliacaoSerializer

    # Filtra as avaliações pelo curso, se o curso_pk for fornecido na URL
    def get_queryset(self):
        if self.kwargs.get('curso_pk'):
            return self.queryset.filter(curso_id=self.kwargs.get('curso_pk'))
        return self.queryset.all()

class AvaliacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    # Esse método define qual objeto específico será retornado.
    def get_object(self):
        if self.kwargs.get('curso_pk'):
            return get_object_or_404(self.get_queryset(), curso_id=self.kwargs.get('curso_pk'), pk=self.kwargs.get('avaliacao_pk'))    
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
    

# ============================== API V2 ==============================
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    # O decorator @action cria rotas extras dentro de um ViewSet.
    @action(detail=True, methods=['get'], pagination_class=AvaliacaoPagination) # Só essa rota usa essa paginação.
    # Nome do método vira o nome da rota e pk é o ID do curso 
    def avaliacoes(self, request, pk=None): 

        # Pagination
        avaliacoes = Avaliacao.objects.filter(curso_id=pk) # Me dá todas as avaliações do curso 3
        page = self.paginate_queryset(avaliacoes) 

        if page is not None:
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        # Pega todas as avaliações relacionadas ao curso  
        serializer = AvaliacaoSerializer(avaliacoes.all(), many=True) # Many=True diz que isso é uma lista
        return Response(serializer.data)

''' VIEWSET PADRAO
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
'''

# VIEWSET CUSTOMIZADO - Somente list, create, retrieve, update, destroy
class AvaliacaoViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer      
