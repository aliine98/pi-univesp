from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def validar_tamanho_foto(foto):
    limite = 5 * 1024 * 1024  # 5MB
    if foto.size > limite:
        raise ValidationError("A imagem deve ter no máximo 5MB.")

# Create your models here.
class Animal(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", _("Disponível para adoção")
        ADOTADO = "ADOTADO", _("Adotado")
    class Sexo(models.TextChoices):
        MACHO = "MACHO", _("Macho")
        FEMEA = "FEMEA", _("Fêmea")
    class Porte(models.TextChoices):
        PEQUENO = "PEQUENO", _("Pequeno")
        MEDIO = "MEDIO", _("Médio")
        GRANDE = "GRANDE", _("Grande")

    foto = models.ImageField("Foto",upload_to='animais', blank=True, null=True,validators=[validar_tamanho_foto])
    mais_informacoes = models.TextField("Mais informações",blank=True, null=True)
    idade_aproximada = models.CharField("Idade Aproximada",max_length=50)
    status = models.CharField("Status",choices=Status, default=Status.DISPONIVEL, max_length=10)
    sexo = models.CharField("Sexo",choices=Sexo, max_length=10)
    porte = models.CharField("Porte",choices=Porte, max_length=10)
    vacinado = models.BooleanField("Vacinado", default=False)
    castrado = models.BooleanField("Castrado", default=False)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    adotado_em = models.DateTimeField("Adotado em", blank=True, null=True)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("animal", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.status == self.Status.ADOTADO and self.adotado_em is None:
            self.adotado_em = timezone.now()
        elif self.status == self.Status.DISPONIVEL:
            self.adotado_em = None
        super().save(*args, **kwargs)