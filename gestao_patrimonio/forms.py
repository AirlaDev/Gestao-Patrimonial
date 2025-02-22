from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Bem, Categoria, Departamento, Fornecedor, Instituicao, Movimentacao
from django.core.exceptions import ValidationError
from .models import Bem

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
            'fornecedor','instituicao', 'data_aquisicao', 'valor_aquisicao', 
            'rfid_tag', 'status'
        ]

        def clean_rfid_tag(self):
            rfid_tag = self.cleaned_data.get('rfid_tag')
            if rfid_tag:  # Verifica se o campo não está vazio
                # Verifica se a tag já está cadastrada
                if Bem.objects.filter(rfid_tag=rfid_tag).exists():
                    raise ValidationError('Esta RFID Tag já está cadastrada.')
            return rfid_tag
        
        widgets = {
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),  # Campo de data
            'descricao': forms.Textarea(attrs={'rows': 3}),  # Área de texto para descrição
        }
        # Personalize o campo status para usar um menu de opções
        status = forms.ChoiceField(
        choices=Bem.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='Ativo'
    )

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

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = ['nome', 'descricao']