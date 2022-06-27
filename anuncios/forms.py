from django.apps import AppConfig
from django import forms
from .models import Categoria, Produto, Servico, Contato
from users.models import User




STATUS_CHOICES = (
        ('Login e Cadastro de usuario', 'Login e Cadastro de usuario'),
        ('Cadastro de produtos/serviço', 'Cadastro de produtos/serviço'),
        ('Criticas e Sugestões', 'Criticas e Sugestões'),
        ('Outros', 'Outros'),
        ('','')
)

class ContactForm(forms.Form):
    nome = forms.CharField(required=True)
    seu_email = forms.EmailField(required=True)
    assunto = forms.ChoiceField(choices = STATUS_CHOICES, label='Assunto', initial='',widget=forms.Select(), required=True)
    mensagem = forms.CharField(widget=forms.Textarea, required=True)




class Produto_Form(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nm_produto', 'categoria','dc_produto','vl_produto','imagem','st_produto')



class Contato_Form(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('tp_contato','tx_contato')



class Servico_Form(forms.ModelForm):
    class Meta:
        model = Servico
        #fields = ('tx_titulo_servico','categoria','doc_servico','st_servico','imagem')
        fields = ('tx_titulo_servico','categoria','dc_servico', 'imagem','st_servico')
