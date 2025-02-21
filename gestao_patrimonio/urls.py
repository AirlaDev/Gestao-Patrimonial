from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    

    
    path('bens/', views.bem_list, name='bem_list'),
    path('bens/create/', views.bem_create, name='bem_create'),
    path('bens/update/<int:pk>/', views.bem_update, name='bem_update'),
    path('bens/delete/<int:pk>/', views.bem_delete, name='bem_delete'),
    path('bens/ler_tag_rfid/', views.ler_tag_rfid, name='ler_tag_rfid'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/create/', views.categoria_create, name='categoria_create'),
    path('categorias/update/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('categorias/delete/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    path('departamentos/', views.departamento_list, name='departamento_list'),
    path('departamentos/create/', views.departamento_create, name='departamento_create'),
    path('departamentos/update/<int:pk>/', views.departamento_update, name='departamento_update'),
    path('departamentos/delete/<int:pk>/', views.departamento_delete, name='departamento_delete'),
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/create/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/update/<int:pk>/', views.fornecedor_update, name='fornecedor_update'),
    path('fornecedores/delete/<int:pk>/', views.fornecedor_delete, name='fornecedor_delete'),
    path('movimentacoes/', views.movimentacao_list, name='movimentacao_list'),
    path('movimentacoes/create/', views.movimentacao_create, name='movimentacao_create'),
    path('movimentacoes/update/<int:pk>/', views.movimentacao_update, name='movimentacao_update'),
    path('movimentacoes/delete/<int:pk>/', views.movimentacao_delete, name='movimentacao_delete'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
