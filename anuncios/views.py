from django import template
from django.contrib.auth import models, get_user_model
from django.contrib.auth.models import User, Group
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Produto, Servico, Contato
from random import shuffle
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from .forms import ContactForm
from .forms import Produto_Form
from .forms import Contato_Form
from .forms import Servico_Form
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView

# class IndexView(TemplateView):
#    template_name = 'anuncios/index.html'


def index(request):
    return render(request, 'anuncios/index.html')


def usuarios_inativos():
    group = Group.objects.get(name='Inativo')
    usersx = group.user_set.all()

    list = []

    for item in usersx:
        list.append(item.id)

    return list


def produtos(request):

    categorias_todas = list(Categoria.objects.filter(tp_categoria='P'))

    categorias = []
    for itens in categorias_todas:
        if Produto.objects.filter(categoria=itens.id, st_produto='A').exclude(usuario__in=usuarios_inativos()).count() > 0:
            categorias.append(itens)

    return render(request, 'anuncios/produtos.html', {'categorias': categorias})


def servicos(request):
    categorias_todas = list(Categoria.objects.filter(tp_categoria='S'))

    categorias = []
    for itens in categorias_todas:
        if Servico.objects.filter(categoria=itens.id, st_servico='A').exclude(usuario__in=usuarios_inativos()).count() > 0:
            categorias.append(itens)

    return render(request, 'anuncios/servicos.html', {'categorias': categorias})


def listaProdutos(request, id):

    produtos = Produto.objects.filter(categoria=id, st_produto='A').order_by(
        'dt_cadastro').exclude(usuario__in=usuarios_inativos())

    # shuffle(produtos)
    categoria = Categoria.objects.get(id=id)

    paginator = Paginator(produtos, 3)
    page = request.GET.get('page')
    produtos = paginator.get_page(page)

    return render(request, 'anuncios/lista_produtos.html', {'produtos': produtos, 'categoria': categoria})


def listaServicos(request, id):
    servicos = list(Servico.objects.filter(categoria=id, st_servico='A').order_by(
        'dt_cadastro').exclude(usuario__in=usuarios_inativos()))
    # shuffle(servicos)
    categoria = Categoria.objects.get(id=id)

    paginator = Paginator(servicos, 3)
    page = request.GET.get('page')
    servicos = paginator.get_page(page)

    return render(request, 'anuncios/lista_servicos.html', {'servicos': servicos, 'categoria': categoria})


def detalhesProduto(request, id):

    if request.user.is_anonymous:
        is_Morador = False
    else:
        is_Morador = Group.objects.filter(
            user=request.user, name='Morador').exists()

    produto = Produto.objects.get(id=id)

    if is_Morador:
        contatos = Contato.objects.filter(usuario=produto.usuario)
    else:
        contatos = Contato.objects.filter(id=0)

    mensagem = 'Oi, me interesse pelo seu Produto\nGostaria que verificar o valor.\nPodemos conversar'
    return render(request, 'anuncios/detalhes_produto.html', {'produto': produto, 'contatos': contatos, 'mensagem': mensagem})


def detalhesProdutoOriginal(request):
    return render(request, 'anuncios/detalhes_produto_original.html')


def detalhesProdutoCarrossel(request):
    return render(request, 'anuncios/detalhes_produto_carrossel.html')


def detalhesServico(request, id):

    if request.user.is_anonymous:
        is_Morador = False
    else:
        is_Morador = Group.objects.filter(
            user=request.user, name='Morador').exists()

    servico = Servico.objects.get(id=id)

    if is_Morador:
        contatos = Contato.objects.filter(usuario=servico.usuario)
    else:
        contatos = Contato.objects.filter(id=0)

    return render(request, 'anuncios/detalhes_servico.html', {'servico': servico, 'contatos': contatos})


def politicaPrivacidade(request):
    return render(request, 'anuncios/politica_privacidade.html')


def faleConosco(request):
    if request.method == 'GET':

        form = ContactForm()
    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            assunto = form.cleaned_data['assunto']
            seu_email = form.cleaned_data['seu_email']
            mensagem = form.cleaned_data['mensagem']

            try:
                # send_mail ( subject , message )
                assunto = 'Teste (Fale conosco): ' + assunto
                mensagem = 'Nome:' + nome + '\nEmail:' + seu_email + '\nMensagem: ' + mensagem
                send_mail(assunto, mensagem, 'mogiunivesp5@hotmail.com',
                          ['2005436@aluno.univesp.br', '2011457@aluno.univesp.br'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return Sucesso_envio_email(request)
    return render(request, 'anuncios/fale_conosco.html', {'form': form})


def Sucesso_envio_email(request):
    # return HttpResponse('Sucesso! Obrigado pela sua mensagem!')
    return render(request, 'anuncios/envio_email_sucesso.html')


def perguntasRespostas(request):
    return render(request, 'anuncios/perguntas_respostas.html')

# def login(request):
#    return render(request, 'anuncios/login.html')


def politicaCookies(request):
    return render(request, 'anuncios/politica_cookies.html')


def termosUso(request):
    return render(request, 'anuncios/termos_uso.html')


def pesquisa(request):
    search = request.GET.get('search')

    if search:
        p1 = list(Produto.objects.filter(Q(nm_produto__contains=search)))
        p2 = list(Servico.objects.filter(
            Q(tx_titulo_servico__contains=search)))
        lista = p1 + p2
        # shuffle(lista)

    else:
        p1 = list(Produto.objects.all())
        p2 = list(Servico.objects.all())
        lista = p1 + p2

    paginator = Paginator(lista, 3)
    page = request.GET.get('page')
    anuncios = paginator.get_page(page)
    return render(request, 'anuncios/pesquisa.html', {'anuncios': anuncios})


def is_Anunciante(user):
    return user.groups.filter(name='Anunciante').exists() or user.is_superuser


@login_required
@user_passes_test(is_Anunciante)
def Cadastro_produto(request):
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'anuncios/Cadastro_produto.html', {'produtos': produtos})


@login_required
@user_passes_test(is_Anunciante)
def Cadastro_servico(request):
    servicos = Servico.objects.filter(usuario=request.user)
    return render(request, 'anuncios/Cadastro_produto.html', {'servicos': servicos})


@login_required
@user_passes_test(is_Anunciante)
def produto_edit(request, id):
    produto = get_object_or_404(Produto, pk=id)

    if produto.usuario != request.user:
        return redirect('Cadastro_produto')

    form = Produto_Form(instance=produto)

    if (request.method == 'POST'):
        form = Produto_Form(data=request.POST,
                            files=request.FILES, instance=produto)

        if form.is_valid():
            #Produto = form.save(commit=False)
            produto.save()
            return redirect('Cadastro_produto')
        else:
            return render(request, 'produto_edit', {'form': form, 'produto': produto})
    else:
        return render(request, 'anuncios/produto_edit.html', {'form': form, 'produto': produto})


@login_required
@user_passes_test(is_Anunciante)
def produto_delete(request, id):
    produto = get_object_or_404(Produto, pk=id)

    if produto.usuario != request.user:
        return redirect('Cadastro_produto')

    produto.delete()
    #messages.info(request, 'Tarefa deletada com sucesso.')
    return redirect('Cadastro_produto')


@login_required
@user_passes_test(is_Anunciante)
def produto_add(request):
    context = {}
    if request.method == 'POST':

        form = Produto_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            Produto = form.save(commit=False)
            Produto.usuario = request.user
            Produto.save()
            return redirect('Cadastro_produto')
    else:
        form = Produto_Form()
    context['form'] = form
    return render(request, 'anuncios/produto_add.html', context)


@login_required
@user_passes_test(is_Anunciante)
def Cadastro_contato(request):
    contatos = Contato.objects.filter(usuario=request.user)
    return render(request, 'anuncios/Cadastro_contato.html', {'contatos': contatos})


@login_required
@user_passes_test(is_Anunciante)
def contato_add(request):
    context = {}
    if request.method == 'POST':

        form = Contato_Form(data=request.POST)
        if form.is_valid():
            Contato = form.save(commit=False)
            Contato.usuario = request.user
            Contato.condominio = 'Flex Mogi'
            Contato.save()
            return redirect('Cadastro_contato')
    else:
        form = Contato_Form()
    context['form'] = form
    return render(request, 'anuncios/contato_add.html', context)


@login_required
@user_passes_test(is_Anunciante)
def contato_edit(request, id):
    contato = get_object_or_404(Contato, pk=id)

    if contato.usuario != request.user:
        return redirect('Cadastro_produto')

    form = Contato_Form(instance=contato)

    if (request.method == 'POST'):
        form = Contato_Form(data=request.POST, instance=contato)

        if form.is_valid():
            #Produto = form.save(commit=False)
            contato.save()
            return redirect('Cadastro_contato')
        else:
            return render(request, 'contato_edit', {'form': form, 'contato': contato})
    else:
        return render(request, 'anuncios/contato_edit.html', {'form': form, 'contato': contato})


@login_required
@user_passes_test(is_Anunciante)
def contato_delete(request, id):
    contato = get_object_or_404(Contato, pk=id)

    if contato.usuario != request.user:
        return redirect('Cadastro_produto')

    contato.delete()
    #messages.info(request, 'Tarefa deletada com sucesso.')
    return redirect('Cadastro_contato')


@login_required
@user_passes_test(is_Anunciante)
def Cadastro_servico(request):
    servicos = Servico.objects.filter(usuario=request.user)
    return render(request, 'anuncios/Cadastro_servico.html', {'servicos': servicos})


@login_required
@user_passes_test(is_Anunciante)
def servico_add(request):
    context = {}
    if request.method == 'POST':

        form = Servico_Form(data=request.POST, files=request.FILES)
        if form.is_valid():
            Servico = form.save(commit=False)
            Servico.usuario = request.user
            Servico.save()
            return redirect('Cadastro_servico')
    else:
        form = Servico_Form()
    context['form'] = form
    return render(request, 'anuncios/servico_add.html', context)


@login_required
@user_passes_test(is_Anunciante)
def servico_edit(request, id):
    servico = get_object_or_404(Servico, pk=id)

    if servico.usuario != request.user:
        return redirect('Cadastro_produto')

    form = Servico_Form(instance=servico)

    if (request.method == 'POST'):
        form = Servico_Form(data=request.POST,
                            files=request.FILES, instance=servico)

        if form.is_valid():
            #Produto = form.save(commit=False)
            servico.save()
            return redirect('Cadastro_servico')
        else:
            return render(request, 'servico_edit', {'form': form, 'servico': servico})
    else:
        return render(request, 'anuncios/servico_edit.html', {'form': form, 'servico': servico})


@login_required
@user_passes_test(is_Anunciante)
def servico_delete(request, id):
    servico = get_object_or_404(Servico, pk=id)

    if servico.usuario != request.user:
        return redirect('Cadastro_produto')

    servico.delete()
    #messages.info(request, 'Tarefa deletada com sucesso.')
    return redirect('Cadastro_servico')


def anunciante_produtos(request, id):

    todos_usuarios = get_user_model()
    usuario_id = todos_usuarios.objects.get(username=id)

    produtos = Produto.objects.filter(usuario=usuario_id, st_produto='A').order_by(
        'dt_cadastro').exclude(usuario__in=usuarios_inativos())

    paginator = Paginator(produtos, 3)
    page = request.GET.get('page')
    produtos = paginator.get_page(page)

    return render(request, 'anuncios/anunciante_produtos.html', {'produtos': produtos, 'usuario_id': usuario_id})


def anunciante_servicos(request, id):

    todos_usuarios = get_user_model()
    usuario_id = todos_usuarios.objects.get(username=id)

    servicos = Servico.objects.filter(usuario=usuario_id, st_servico='A').exclude(
        usuario__in=usuarios_inativos())

    paginator = Paginator(servicos, 3)
    page = request.GET.get('page')
    servicos = paginator.get_page(page)

    return render(request, 'anuncios/anunciante_servicos.html', {'servicos': servicos, 'usuario_id': usuario_id})
