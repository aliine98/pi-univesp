from braces.views import GroupRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.models import Animal


# Create your views here.
#class Home(TemplateView):
#    template_name = 'home.html'

class Home(ListView):
    #inicialmente só listagem de animais
    context_object_name = "animais"
    template_name = 'animais.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['portes'] = Animal.Porte
        context['sexos'] = Animal.Sexo
        return context

    def get_queryset(self):
        animais = Animal.objects.filter(status=Animal.Status.DISPONIVEL)
        porte = self.request.GET.get('porte')
        sexo = self.request.GET.get('sexo')
        vacinado = self.request.GET.get('vacinado')
        castrado = self.request.GET.get('castrado')
        idade = self.request.GET.get('idade')
        if porte:
            animais = animais.filter(porte=porte)
        if sexo:
            animais = animais.filter(sexo=sexo)
        if vacinado:
            animais = animais.filter(vacinado=vacinado)
        if castrado:
            animais = animais.filter(castrado=castrado)
        if idade:
            animais = animais.filter(idade_aproximada__icontains=idade)
        return animais

class GerenciarAnimaisCadastrados(GroupRequiredMixin,ListView):
    group_required = u"Ong"
    model = Animal
    template_name = 'gerenciar-animais-cadastrados.html'

    def get_context_data(self, **kwargs):
        context = super(GerenciarAnimaisCadastrados, self).get_context_data(**kwargs)
        context['portes'] = Animal.Porte
        context['sexos'] = Animal.Sexo
        context['status'] = Animal.Status
        return context

    def get_queryset(self):
        animais = Animal.objects.all()
        porte = self.request.GET.get('porte')
        sexo = self.request.GET.get('sexo')
        vacinado = self.request.GET.get('vacinado')
        castrado = self.request.GET.get('castrado')
        idade = self.request.GET.get('idade')
        codigo = self.request.GET.get('codigo')
        status = self.request.GET.get('status')
        if porte:
            animais = animais.filter(porte=porte)
        if sexo:
            animais = animais.filter(sexo=sexo)
        if vacinado:
            animais = animais.filter(vacinado=vacinado)
        if castrado:
            animais = animais.filter(castrado=castrado)
        if idade:
            animais = animais.filter(idade_aproximada__icontains=idade)
        if status:
            animais = animais.filter(status=status)
        if codigo:
            digitos = "".join(c for c in codigo if c in '0123456789')
            if digitos:
                animais = animais.filter(pk=int(digitos))
            else:
                animais = animais.none()
        return animais

class AnimalCreateView(GroupRequiredMixin,SuccessMessageMixin,CreateView):
    group_required = u"Ong"
    model = Animal
    fields = ["foto","sexo","idade_aproximada","porte","vacinado","castrado","mais_informacoes","status"]
    template_name = "cadastrar-animal.html"
    success_url = reverse_lazy("gerenciar-animais")
    success_message = "Animal cadastrado com sucesso!"

class AnimalUpdateView(GroupRequiredMixin,SuccessMessageMixin,UpdateView):
    group_required = u"Ong"
    model = Animal
    fields = ["foto", "sexo", "idade_aproximada", "porte", "vacinado", "castrado", "mais_informacoes", "status"]
    template_name = "cadastrar-animal.html"
    success_url = reverse_lazy("gerenciar-animais")
    success_message = "Animal atualizado com sucesso!"

class AnimalDeleteView(GroupRequiredMixin,SuccessMessageMixin,DeleteView):
    group_required = u"Ong"
    model = Animal
    success_url = reverse_lazy("gerenciar-animais")
    success_message = "Animal excluído com sucesso!"

class UsuarioUpdateView(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = u"Ong"
    model = User
    fields = ['username']
    template_name = "minha-conta.html"
    success_url = reverse_lazy("minha-conta")
    success_message = "Usuário atualizado com sucesso!"

    def get_object(self, queryset=None):
        return self.request.user

class SenhaUpdateView(GroupRequiredMixin,SuccessMessageMixin,PasswordChangeView):
    group_required = u"Ong"
    template_name = 'mudar-senha.html'
    success_message = "Senha atualizada com sucesso!"
    success_url = reverse_lazy("minha-conta")