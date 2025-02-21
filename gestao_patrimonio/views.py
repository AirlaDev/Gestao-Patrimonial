import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Bem, Categoria, Departamento, Fornecedor, Movimentacao
from .forms import BemForm, CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm, UserRegisterForm
from django.db.models import Count, Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
import serial # Importe a biblioteca pyserial
# Dashboard
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Bem, Categoria, Movimentacao
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Sum
from .models import Bem, Categoria, Movimentacao
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BemForm
from .models import Bem
from django.contrib import messages
from django.db.models import Count, Q


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    # Captura o termo de pesquisa
    search_query = request.GET.get('search', '')

    # Filtra os ativos com base no termo de pesquisa (nome ou rfid_tag)
    if search_query:
        ativos = Bem.objects.filter(Q(nome__icontains=search_query) | Q(rfid_tag__icontains=search_query))
    else:
        ativos = Bem.objects.all()

    # Dados para exibição geral
    total_ativos = ativos.count()
    valor_total_patrimonio = sum([bem.valor_aquisicao for bem in ativos])
    ativos_em_manutencao = ativos.filter(status='em_manutencao').count()

    # Dados para o gráfico de Ativos por Categoria
    categorias = Categoria.objects.annotate(num_ativos=Count('bem'))
    labels_categorias = [categoria.nome for categoria in categorias]
    data_categorias = [categoria.num_ativos for categoria in categorias]

    # Dados para o gráfico de Ativos por Departamento
    departamentos = Departamento.objects.annotate(num_ativos=Count('bem'))
    labels_departamentos = [departamento.nome for departamento in departamentos]
    data_departamentos = [departamento.num_ativos for departamento in departamentos]

    context = {
        'total_ativos': total_ativos,
        'valor_total_patrimonio': valor_total_patrimonio,
        'ativos_em_manutencao': ativos_em_manutencao,
        'labels_categorias': labels_categorias,
        'data_categorias': data_categorias,
        'labels_departamentos': labels_departamentos,
        'data_departamentos': data_departamentos,
        'ativos': ativos,  # Passa os ativos filtrados para o template
        'search_query': search_query,  # Passa o termo de pesquisa para o template
    }

    return render(request, 'dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de login após logout

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Passa o request para authenticate
            
            if user is not None:
                login(request, user)  # Faz o login automático após o registro
                messages.success(request, f'Usuário {username} cadastrado com sucesso!')  # Mensagem de sucesso
                return redirect('dashboard')  # Redireciona para o dashboard após o cadastro
            else:
                messages.error(request, 'Erro ao autenticar o usuário após o cadastro.')  # Mensagem de erro
        else:
            messages.error(request, 'Erro ao cadastrar o usuário. Verifique os dados.')  # Mensagem de erro
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# CRUD para Bens
@login_required
def bem_list(request):
    bens = Bem.objects.all()
    return render(request, 'bens/bem_list.html', {'bens': bens})

@login_required
def bem_create(request):
    if request.method == 'POST':
        form = BemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bem_list')
    else:
        form = BemForm()
    return render(request, 'bens/bem_form.html', {'form': form})

@login_required
def bem_update(request, pk):
    bem = get_object_or_404(Bem, pk=pk)
    if request.method == 'POST':
        form = BemForm(request.POST, instance=bem)
        if form.is_valid():
            form.save()
            return redirect('bem_list')
    else:
        form = BemForm(instance=bem)
    return render(request, 'bens/bem_form.html', {'form': form})

@login_required
def bem_delete(request, pk):
    bem = get_object_or_404(Bem, pk=pk)
    if request.method == 'POST':
        bem.delete()
        return redirect('bem_list')
    return render(request, 'bens/bem_confirm_delete.html', {'bem': bem})

# CRUD para Categorias
@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/categoria_form.html', {'form': form})

@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categoria_form.html', {'form': form})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'categorias/categoria_confirm_delete.html', {'categoria': categoria})

# CRUD para Departamentos
@login_required
def departamento_list(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentos/departamento_list.html', {'departamentos': departamentos})

@login_required
def departamento_create(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departamento_list')
    else:
        form = DepartamentoForm()
    return render(request, 'departamentos/departamento_form.html', {'form': form})

@login_required
def departamento_update(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('departamento_list')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentos/departamento_form.html', {'form': form})

@login_required
def departamento_delete(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        departamento.delete()
        return redirect('departamento_list')
    return render(request, 'departamentos/departamento_confirm_delete.html', {'departamento': departamento})

# CRUD para Fornecedores
@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedores/fornecedor_list.html', {'fornecedores': fornecedores})

@login_required
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores/fornecedor_form.html', {'form': form})

@login_required
def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'fornecedores/fornecedor_form.html', {'form': form})

@login_required
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('fornecedor_list')
    return render(request, 'fornecedores/fornecedor_confirm_delete.html', {'fornecedor': fornecedor})

# CRUD para Movimentações
@login_required
def movimentacao_list(request):
    movimentacoes = Movimentacao.objects.all()
    return render(request, 'movimentacoes/movimentacao_list.html', {'movimentacoes': movimentacoes})

@login_required
def movimentacao_create(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimentacao_list')
    else:
        form = MovimentacaoForm()
    return render(request, 'movimentacoes/movimentacao_form.html', {'form': form})

@login_required
def movimentacao_update(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk)
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()
            return redirect('movimentacao_list')
    else:
        form = MovimentacaoForm(instance=movimentacao)
    return render(request, 'movimentacoes/movimentacao_form.html', {'form': form})

@login_required
def movimentacao_delete(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk)
    if request.method == 'POST':
        movimentacao.delete()
        return redirect('movimentacao_list')
    return render(request, 'movimentacoes/movimentacao_confirm_delete.html', {'movimentacao': movimentacao})

# Configurações da porta serial (ajuste conforme necessário)
PORT = 'COM3'  # Substitua pela porta serial correta
BAUDRATE = 9600

# View para cadastrar/atualizar bens
def bem_create_update(request, pk=None):
    if pk:
        bem = get_object_or_404(Bem, pk=pk)
    else:
        bem = None

    if request.method == 'POST':
        form = BemForm(request.POST, instance=bem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bem salvo com sucesso!')
            return redirect('bem_list')
        else:
            messages.error(request, 'Erro ao salvar o bem. Verifique os dados.')
    else:
        form = BemForm(instance=bem)

    return render(request, 'bens/bem_form.html', {'form': form})

# View para ler a tag rfid
def ler_tag_rfid(request):
    tag_id = None
    error_message = None

    try:
        ser = serial.Serial(PORT, BAUDRATE)
        tag_id = ser.readline().decode('utf-8').strip()
        ser.close()
    except serial.SerialException as e:
        error_message = f'Erro ao ler a tag rfid: {e}'

    return render(request, 'bens/ler_tag_rfid.html', {'tag_id': tag_id, 'error_message': error_message})