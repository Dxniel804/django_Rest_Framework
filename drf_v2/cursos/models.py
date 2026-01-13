from django.db import models

# Create your models here.

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    # “Essa classe NÃO vira tabela no banco.
    # Ela existe só para ser herdada.
    class Meta:
        abstract = True

class Curso(Base):
    titulo = models.CharField(max_length=100)
    url = models.URLField(unique=True)

    # configurações do model, não dados
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']  # ordena por id - GLOBAL 
    
    def __str__(self):
        return self.titulo

class Avaliacao(Base):
    # related_name='avaliacoes' define como você acessa as avaliações a partir do curso
    # on_delete=models.CASCADE define que, se um curso for deletado, todas as suas avaliações também serão
    curso = models.ForeignKey(Curso, related_name='avaliacoes', on_delete=models.CASCADE)  
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    comentario = models.TextField(blank=True, default='')
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1)  # Ex: 4.5
    ordering = ['id']

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        unique_together = ('curso', 'email')  # Um usuário só pode avaliar um curso uma vez

    # GETTER 
    def __str__(self):
        return f"{self.nome} avaliou o curso {self.curso} com nota {self.avaliacao}"    