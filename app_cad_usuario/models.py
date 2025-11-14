from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Usuario(models.Model):
    nome = models.CharField(max_length=100)  
    login = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Estoque(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    material = models.CharField(max_length=100)  
    cor = models.CharField(max_length=50) 
    quantidade_metros = models.FloatField(default=0)  

    def __str__(self):
        return f"{self.material} ({self.cor})"

class Projeto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    nome = models.CharField(max_length=100)
    material = models.ForeignKey('Estoque', on_delete=models.CASCADE)  
    cor = models.CharField(max_length=50)
    quantidade = models.IntegerField(default=1)  
    metros_por_unidade = models.FloatField(default=0)  

    def __str__(self):
        return self.nome

class Historico(models.Model):
    ACAO_CHOICES = [
        ('adicionado', 'Adicionado'),
        ('editado', 'Editado'),
        ('excluido', 'Excluído'),
        ('concluido', 'Concluído'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    tabela = models.CharField(max_length=100)  
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)  
    descricao = models.TextField()  
    data_hora = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.tabela} - {self.acao} - {self.data_hora}"

