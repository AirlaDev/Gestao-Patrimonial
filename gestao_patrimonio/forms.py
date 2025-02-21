from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Bem, Categoria, Departamento, Fornecedor, Movimentacao

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = [
            'nome', 'descricao', 'categoria', 'departamento', 
            'fornecedor', 'data_aquisicao', 'valor_aquisicao', 
            'rfid_tag', 'status'
        ]
        widgets = {
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),  # Campo de data
            'descricao': forms.Textarea(attrs={'rows': 3}),  # Área de texto para descrição
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = '__all__'