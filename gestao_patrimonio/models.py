from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')
    informacoes_personalizadas = models.TextField(blank=True, null=True)  # Exemplo de campo personalizado
    # Adicione outros campos necessários para a dashboard

    def __str__(self):
        return f"Dashboard de {self.usuario.username}"

class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    contato = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Instituicao(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Bem(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Em Manutenção', 'Em Manutenção'),
        
    ]
    nome = models.CharField(max_length=140)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.SET_NULL, null=True)  # Nova relação com Instituicao
    data_aquisicao = models.DateField()
    valor_aquisicao = models.DecimalField(max_digits=10, decimal_places=2)
    rfid_tag = models.CharField(max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Ativo')  # Ativo, Em Manutenção, Descartado

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    bem = models.ForeignKey(Bem, on_delete=models.CASCADE)
    departamento_origem = models.ForeignKey(Departamento, related_name='movimentacoes_origem', on_delete=models.SET_NULL, null=True)
    departamento_destino = models.ForeignKey(Departamento, related_name='movimentacoes_destino', on_delete=models.SET_NULL, null=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Movimentação de {self.bem.nome} em {self.data_movimentacao}"