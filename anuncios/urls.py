from django.urls import path
from . import views

app_name = 'anuncios'

urlpatterns = [
    path('', views.index, name = 'index'),
    #path('', views.IndexView.as_view(), name='index'),

    path('produtos/', views.produtos, name = 'produtos'),
    path('servicos/', views.servicos, name = 'servicos'),
    path('lista_produtos/<int:id>', views.listaProdutos, name = 'lista_produtos'),
    path('lista_servicos/<int:id>', views.listaServicos, name = 'lista_servicos'),
    path('detalhes_produto/<int:id>', views.detalhesProduto, name = 'detalhes_produto'),
    path('detalhes_produto_original/', views.detalhesProdutoOriginal, name = 'detalhes_produto_original'),
    path('detalhes_produto_carrossel/', views.detalhesProdutoCarrossel, name = 'detalhes_produto_carrossel'),  
    path('detalhes_servico/<int:id>/', views.detalhesServico, name = 'detalhes_servico'),  
    path('politica_privacidade/', views.politicaPrivacidade, name = 'politica_privacidade'),  
    path('Sucesso_envio_email/', views.Sucesso_envio_email, name='Sucesso_envio_email'),
    path('Cadastro_produto/', views.Cadastro_produto, name='Cadastro_produto'),
    path('Cadastro_contato/', views.Cadastro_contato, name='Cadastro_contato'),
    path('Cadastro_servico/', views.Cadastro_servico, name='Cadastro_servico'),

    path('fale_conosco/', views.faleConosco, name = 'fale_conosco'),  
    path('perguntas_respostas/', views.perguntasRespostas, name = 'perguntas_respostas'),  
    #path('login/', views.login, name = 'login'),  


    #path('como_anunciar/', views.comoAnunciar, name = 'como_anunciar'),  
    path('politica_cookies/', views.politicaCookies, name = 'politica_cookies'),  
    path('termos_uso/', views.termosUso, name = 'termos_uso'),  
    path('anunciante_produtos/<str:id>', views.anunciante_produtos, name = 'anunciante_produtos'),  
    path('anunciante_servicos/<str:id>', views.anunciante_servicos, name = 'anunciante_servicos'),  
    path('pesquisa/', views.pesquisa, name = 'pesquisa'),

    path('servico_add/', views.servico_add, name='servico_add'),
    path('servico_edit/<int:id>', views.servico_edit, name='servico_edit'),
    path('servico_delete/<int:id>', views.servico_delete, name='servico_delete'),

    path('contato_add/', views.contato_add, name='contato_add'),
    path('contato_edit/<int:id>/', views.contato_edit, name='contato_edit'),
    path('contato_delete/<int:id>', views.contato_delete, name='contato_delete'),

    path('produto_delete/<int:id>', views.produto_delete, name='produto_delete'),
    path('produto_add/', views.produto_add, name='produto_add'),
    path('produto_edit/<int:id>', views.produto_edit, name='produto_edit'),

]

#aqui defini  o endereço do login que no padrão é registration/login
#urlpatterns += [    path('accounts/', include('django.contrib.auth.urls')),  ]
