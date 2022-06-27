from django.contrib import admin
from users.models import User
from .models import Categoria, Produto, Condominio, Residencia, Contato, Servico

'''
Classe criada para exibição tabular das informações de contato.
Na área administrativa do Django será apresentada no formulário
Condominío as informações para o cadastro de formas de Contato. Por
exemplo: WhatsApp, Telefone, E-Mail.
'''
#class ContatoInline(admin.TabularInline):
    #model = Contato
    ##extra = 3

#class CondominioAdmin(admin.ModelAdmin):
    #inlines = [ContatoInline]

class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    # exclude = ('dt_cadastro','usuario')
    list_display = ('categoria', 'nm_produto', 'dc_produto',
                    'vl_produto', 'st_produto')
    fields = ['categoria', 'nm_produto', 'dc_produto',
              'vl_produto', 'st_produto','imagem']
    search_fields = ('nm_produto', 'dc_produto', 'categoria')

    #exibir apenas produtos cadastrados pelo usuário logado
    def get_queryset(self, request):
        # Get the logged in user
        usuario_logado = User.objects.filter(username = request.user)
        # Override the get_queryset method for Admin
        qs = super(ProdutoAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            return qs.filter(usuario__in = usuario_logado)
        else:
            return qs

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj = form.save(commit=False)
        obj.usuario = request.user
        if not change:
            obj.usuario = request.user
        return obj

class ServicoAdmin(admin.ModelAdmin):
    model = Servico
    # exclude = ('dt_cadastro','usuario')
    list_display = ('categoria', 'tx_titulo_servico', 'dc_servico',
                    'st_servico')
    fields = ['categoria', 'tx_titulo_servico', 'dc_servico',
              'st_servico','imagem']
    search_fields = ('tx_titulo_servico', 'dc_servico', 'categoria')

    #exibir apenas produtos cadastrados pelo usuário logado
    def get_queryset(self, request):
        # Get the logged in user
        usuario_logado = User.objects.filter(username = request.user)
        # Override the get_queryset method for Admin
        qs = super(ServicoAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            return qs.filter(usuario__in = usuario_logado)
        else:
            return qs

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj = form.save(commit=False)
        obj.usuario = request.user
        if not change:
            obj.usuario = request.user
        return obj






#admin.site.register(Condominio, CondominioAdmin)
#admin.site.register(Categoria)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Servico, ServicoAdmin)
