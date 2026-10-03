from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.models import Animal


# Create your views here.
#class Home(TemplateView):
#    template_name = 'home.html'

class Home(ListView):
    #inicialmente só listagem de animais
    queryset = Animal.objects.filter(status=Animal.Status.DISPONIVEL)
    context_object_name = "animais"
    template_name = 'animais.html'

class GerenciarAnimaisCadastrados(GroupRequiredMixin,ListView):
    group_required = u"Ong"
    model = Animal
    template_name = 'gerenciar-animais-cadastrados.html'

class AnimalCreateView(GroupRequiredMixin,CreateView):
    group_required = u"Ong"
    model = Animal
    fields = ["foto","sexo","idade_aproximada","porte","vacinado","castrado","mais_informacoes","status"]
    template_name = "cadastrar-animal.html"
    success_url = reverse_lazy("gerenciar-animais")

class AnimalUpdateView(GroupRequiredMixin,UpdateView):
    group_required = u"Ong"
    model = Animal
    fields = ["foto", "sexo", "idade_aproximada", "porte", "vacinado", "castrado", "mais_informacoes", "status"]
    template_name = "cadastrar-animal.html"
    success_url = reverse_lazy("gerenciar-animais")

class AnimalDeleteView(GroupRequiredMixin,DeleteView):
    group_required = u"Ong"
    model = Animal
    success_url = reverse_lazy("gerenciar-animais")