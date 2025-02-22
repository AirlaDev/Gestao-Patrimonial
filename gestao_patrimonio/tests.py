from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bem, Categoria, Departamento, Fornecedor, Instituicao, Movimentacao
from .forms import BemForm, CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm, InstituicaoForm

class TestModels(TestCase):
    def setUp(self):
        # Criação de objetos para testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.categoria = Categoria.objects.create(nome='Categoria Teste')
        self.departamento = Departamento.objects.create(nome='Departamento Teste')
        self.fornecedor = Fornecedor.objects.create(nome='Fornecedor Teste')
        self.instituicao = Instituicao.objects.create(nome='Instituição Teste')
        self.bem = Bem.objects.create(
            nome='Bem Teste',
            descricao='Descrição Teste',
            categoria=self.categoria,
            departamento=self.departamento,
            fornecedor=self.fornecedor,
            instituicao=self.instituicao,
            data_aquisicao='2023-01-01',
            valor_aquisicao=1000.00,
            status='Ativo'
        )
        self.movimentacao = Movimentacao.objects.create(
            bem=self.bem,
            departamento_origem=self.departamento,
            departamento_destino=self.departamento,
            observacoes='Movimentação Teste'
        )

    # Testes para o modelo Categoria
    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), 'Categoria Teste')

    # Testes para o modelo Departamento
    def test_departamento_str(self):
        self.assertEqual(str(self.departamento), 'Departamento Teste')

    # Testes para o modelo Fornecedor
    def test_fornecedor_str(self):
        self.assertEqual(str(self.fornecedor), 'Fornecedor Teste')

    # Testes para o modelo Instituicao
    def test_instituicao_str(self):
        self.assertEqual(str(self.instituicao), 'Instituição Teste')

    # Testes para o modelo Bem
    def test_bem_str(self):
        self.assertEqual(str(self.bem), 'Bem Teste')

    # Testes para o modelo Movimentacao
    def test_movimentacao_str(self):
        self.assertEqual(str(self.movimentacao), f"Movimentação de {self.bem.nome} em {self.movimentacao.data_movimentacao}")


class TestViews(TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Criação de objetos para testes
        self.categoria = Categoria.objects.create(nome='Categoria Teste')
        self.departamento = Departamento.objects.create(nome='Departamento Teste')
        self.fornecedor = Fornecedor.objects.create(nome='Fornecedor Teste')
        self.instituicao = Instituicao.objects.create(nome='Instituição Teste')
        self.bem = Bem.objects.create(
            nome='Bem Teste',
            descricao='Descrição Teste',
            categoria=self.categoria,
            departamento=self.departamento,
            fornecedor=self.fornecedor,
            instituicao=self.instituicao,
            data_aquisicao='2023-01-01',
            valor_aquisicao=1000.00,
            status='Ativo'
        )

    # Testes para a view dashboard
    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    # Testes para a view de criação de Bem
    def test_bem_create_view(self):
        response = self.client.get(reverse('bem_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bens/bem_form.html')

    # Testes para a view de atualização de Bem
    def test_bem_update_view(self):
        response = self.client.get(reverse('bem_update', args=[self.bem.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bens/bem_form.html')

    # Testes para a view de exclusão de Bem
    def test_bem_delete_view(self):
        response = self.client.get(reverse('bem_delete', args=[self.bem.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bens/bem_confirm_delete.html')

    # Testes para a view de listagem de Categorias
    def test_categoria_list_view(self):
        response = self.client.get(reverse('categoria_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/categoria_list.html')

    # Testes para a view de criação de Categoria
    def test_categoria_create_view(self):
        response = self.client.get(reverse('categoria_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/categoria_form.html')

    # Testes para a view de listagem de Departamentos
    def test_departamento_list_view(self):
        response = self.client.get(reverse('departamento_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'departamentos/departamento_list.html')

    # Testes para a view de criação de Departamento
    def test_departamento_create_view(self):
        response = self.client.get(reverse('departamento_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'departamentos/departamento_form.html')

    # Testes para a view de listagem de Fornecedores
    def test_fornecedor_list_view(self):
        response = self.client.get(reverse('fornecedor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fornecedores/fornecedor_list.html')

    # Testes para a view de criação de Fornecedor
    def test_fornecedor_create_view(self):
        response = self.client.get(reverse('fornecedor_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fornecedores/fornecedor_form.html')

    # Testes para a view de listagem de Instituições
    def test_instituicao_list_view(self):
        response = self.client.get(reverse('instituicao_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituicoes/instituicao_list.html')

    # Testes para a view de criação de Instituição
    def test_instituicao_create_view(self):
        response = self.client.get(reverse('instituicao_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituicoes/instituicao_form.html')

    # Testes para a view de listagem de Movimentações
    def test_movimentacao_list_view(self):
        response = self.client.get(reverse('movimentacao_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movimentacoes/movimentacao_list.html')

    # Testes para a view de criação de Movimentação
    def test_movimentacao_create_view(self):
        response = self.client.get(reverse('movimentacao_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movimentacoes/movimentacao_form.html')


class TestForms(TestCase):
    def setUp(self):
        # Criação de objetos para testes
        self.categoria = Categoria.objects.create(nome='Categoria Teste')
        self.departamento = Departamento.objects.create(nome='Departamento Teste')
        self.fornecedor = Fornecedor.objects.create(nome='Fornecedor Teste')
        self.instituicao = Instituicao.objects.create(nome='Instituição Teste')

    # Testes para o formulário de Bem
    def test_bem_form_valid(self):
        form_data = {
            'nome': 'Novo Bem',
            'descricao': 'Nova Descrição',
            'categoria': self.categoria.id,
            'departamento': self.departamento.id,
            'fornecedor': self.fornecedor.id,
            'instituicao': self.instituicao.id,
            'data_aquisicao': '2023-01-01',
            'valor_aquisicao': 2000.00,
            'status': 'Ativo'
        }
        form = BemForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testes para o formulário de Categoria
    def test_categoria_form_valid(self):
        form_data = {'nome': 'Nova Categoria'}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testes para o formulário de Departamento
    def test_departamento_form_valid(self):
        form_data = {'nome': 'Novo Departamento'}
        form = DepartamentoForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testes para o formulário de Fornecedor
    def test_fornecedor_form_valid(self):
        form_data = {'nome': 'Novo Fornecedor'}
        form = FornecedorForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testes para o formulário de Instituição
    def test_instituicao_form_valid(self):
        form_data = {'nome': 'Nova Instituição'}
        form = InstituicaoForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testes para o formulário de Movimentação
    def test_movimentacao_form_valid(self):
        bem = Bem.objects.create(
            nome='Bem Teste',
            descricao='Descrição Teste',
            categoria=self.categoria,
            departamento=self.departamento,
            fornecedor=self.fornecedor,
            instituicao=self.instituicao,
            data_aquisicao='2023-01-01',
            valor_aquisicao=1000.00,
            status='Ativo'
        )
        form_data = {
            'bem': bem.id,
            'departamento_origem': self.departamento.id,
            'departamento_destino': self.departamento.id,
            'observacoes': 'Nova Movimentação'
        }
        form = MovimentacaoForm(data=form_data)
        self.assertTrue(form.is_valid())