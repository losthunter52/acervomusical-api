from django.urls import path
from .views import user, autor, edicao, formacao, genero, partitura, uploads

urlpatterns = [
    path('login/', user.login, name='login'),
    path('users/', user.list_users, name='list_users'),
    path('users/add/', user.add_user, name='add_user'),
    path('users/edit/<str:username>/', user.edit_user, name='edit_user'),
    path('users/delete/<str:username>/', user.delete_user, name='delete_user'),
    path('users/clone/', user.clone_user, name='clone_user'),

    # -- autor --
    path('autores/', autor.list_autores, name='list_autores'),
    path('autores/add/', autor.add_autor, name='add_autor'),
    path('autores/edit/<int:id>/', autor.edit_autor, name='edit_autor'),
    path('autores/delete/<int:id>/', autor.delete_autor, name='delete_autor'),
    
    # -- edicao --
    path('edicoes/', edicao.list_edicoes, name='list_edicoes'),
    path('edicoes/add/', edicao.add_edicao, name='add_edicao'),
    path('edicoes/edit/<int:id>/', edicao.edit_edicao, name='edit_edicao'),
    path('edicoes/delete/<int:id>/', edicao.delete_edicao, name='delete_edicao'),
    
    # -- formacao --
    path('formacoes/', formacao.list_formacoes, name='list_formacoes'),
    path('formacoes/add/', formacao.add_formacao, name='add_formacao'),
    path('formacoes/edit/<int:id>/', formacao.edit_formacao, name='edit_formacao'),
    path('formacoes/delete/<int:id>/', formacao.delete_formacao, name='delete_formacao'),
    
    # -- genero --
    path('generos/', genero.list_generos, name='list_generos'),
    path('generos/add/', genero.add_genero, name='add_genero'),
    path('generos/edit/<int:id>/', genero.edit_genero, name='edit_genero'),
    path('generos/delete/<int:id>/', genero.delete_genero, name='delete_genero'),

    # -- partituras --
    path('partituras/', partitura.list_partituras, name='list_partituras'),
    path('partituras/<int:id>/', partitura.get_partitura, name='get_partitura'),
    path('partituras/add/', partitura.add_partitura, name='add_partitura'),
    path('partituras/edit/<int:id>/', partitura.edit_partitura, name='edit_partitura'),
    path('partituras/delete/<int:id>/', partitura.delete_partitura, name='delete_partitura'),

    # -- uploads --
    path('uploads/imagem/', uploads.upload_imagem, name='upload_imagem'),
    path('uploads/imagem/delete/<int:id>/', uploads.delete_imagem, name='delete_imagem'),
]
