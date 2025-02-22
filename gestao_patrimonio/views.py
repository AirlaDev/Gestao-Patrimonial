import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Bem, Categoria, Departamento, Fornecedor, Instituicao, Movimentacao
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
from .forms import BemForm, CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm, InstituicaoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

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


def dashboard(request):
    # Captura o termo de pesquisa e o filtro de instituição
    search_query = request.GET.get('search', '')
    instituicao_filtro = request.GET.get('instituicao', '')

    # Filtra os ativos com base no termo de pesquisa (nome ou rfid_tag) e instituição
    ativos = Bem.objects.all()
    if search_query:
        ativos = ativos.filter(Q(nome__icontains=search_query) | Q(rfid_tag__icontains=search_query))
    if instituicao_filtro:
        ativos = ativos.filter(instituicao_id=instituicao_filtro)

    # Dados para exibição geral
    total_ativos = ativos.count()
    valor_total_patrimonio = sum([bem.valor_aquisicao for bem in ativos])
    ativos_em_manutencao = ativos.filter(status='Em Manutenção').count()

    # Dados para os gráficos
    categorias = Categoria.objects.annotate(num_ativos=Count('bem'))
    labels_categorias = [categoria.nome for categoria in categorias]
    data_categorias = [categoria.num_ativos for categoria in categorias]

    departamentos = Departamento.objects.annotate(num_ativos=Count('bem'))
    labels_departamentos = [departamento.nome for departamento in departamentos]
    data_departamentos = [departamento.num_ativos for departamento in departamentos]

    instituicoes = Instituicao.objects.annotate(num_ativos=Count('bem'))
    labels_instituicoes = [instituicao.nome for instituicao in instituicoes]
    data_instituicoes = [instituicao.num_ativos for instituicao in instituicoes]

    # Dados para o gráfico de status por instituição
    status_por_instituicao = []
    for instituicao in instituicoes:
        ativos_instituicao = ativos.filter(instituicao=instituicao)
        ativos_ativos = ativos_instituicao.filter(status='Ativo').count()
        ativos_manutencao = ativos_instituicao.filter(status='Em Manutenção').count()
        status_por_instituicao.append({
            'instituicao': instituicao.nome,
            'ativos': ativos_ativos,
            'manutencao': ativos_manutencao
        })

    # Extrair labels e dados para o gráfico de status por instituição
    status_labels = [item['instituicao'] for item in status_por_instituicao]
    status_ativos = [item['ativos'] for item in status_por_instituicao]
    status_manutencao = [item['manutencao'] for item in status_por_instituicao]

    context = {
        'total_ativos': total_ativos,
        'valor_total_patrimonio': valor_total_patrimonio,
        'ativos_em_manutencao': ativos_em_manutencao,
        'labels_categorias': labels_categorias,
        'data_categorias': data_categorias,
        'labels_departamentos': labels_departamentos,
        'data_departamentos': data_departamentos,
        'labels_instituicoes': labels_instituicoes,
        'data_instituicoes': data_instituicoes,
        'instituicoes': instituicoes,
        'instituicao_filtro': int(instituicao_filtro) if instituicao_filtro else '',
        'ativos': ativos,
        'search_query': search_query,
        'status_por_instituicao': status_por_instituicao,
        'status_labels': status_labels,
        'status_ativos': status_ativos,
        'status_manutencao': status_manutencao,
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
            login(request, user)  # Faz o login diretamente após o registro
            messages.success(request, f'Usuário {user.username} cadastrado com sucesso!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
            messages.success(request, 'Bem cadastrado com sucesso!')
            return redirect('bem_list')
        else:
            # Exibe erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
        # Tenta abrir a porta serial e ler a tag RFID
        ser = serial.Serial(PORT, BAUDRATE)
        tag_id = ser.readline().decode('utf-8').strip()  # Lê a tag e remove espaços em branco
        ser.close()  # Fecha a porta serial
    except serial.SerialException as e:
        # Se houver um erro, captura a mensagem
        error_message = f'Erro ao ler a tag RFID: {e}'

    # Redireciona para a página de pesquisa com o valor da tag
    if tag_id:
        return redirect(f"{reverse('dashboard')}?search={tag_id}")
    else:
        messages.error(request, error_message or 'Erro ao ler a tag RFID.')
        return redirect('dashboard')
    
# CRUD para Instituições
@login_required
def instituicao_list(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'instituicoes/instituicao_list.html', {'instituicoes': instituicoes})

@login_required
def instituicao_create(request):
    if request.method == 'POST':
        form = InstituicaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instituicao_list')
    else:
        form = InstituicaoForm()
    return render(request, 'instituicoes/instituicao_form.html', {'form': form})

@login_required
def instituicao_update(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk)
    if request.method == 'POST':
        form = InstituicaoForm(request.POST, instance=instituicao)
        if form.is_valid():
            form.save()
            return redirect('instituicao_list')
    else:
        form = InstituicaoForm(instance=instituicao)
    return render(request, 'instituicoes/instituicao_form.html', {'form': form})

@login_required
def instituicao_delete(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk)
    if request.method == 'POST':
        instituicao.delete()
        return redirect('instituicao_list')
    return render(request, 'instituicoes/instituicao_confirm_delete.html', {'instituicao': instituicao})

@csrf_exempt
def ler_tag_rfid_view(request):
    if request.method == 'POST':
        try:
            tag_id, tag_text = ler_tag_rfid()
            if tag_id and tag_text:
                return JsonResponse({
                    'status': 'success',
                    'tag_id': tag_id,
                    'tag_text': tag_text
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Erro ao ler a tag RFID. Tente novamente.'
                }, status=500)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido'
    }, status=405)