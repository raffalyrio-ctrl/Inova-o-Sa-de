from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import PerfilPaciente, PerfilProfissional, Consulta

class CadastroPacienteForm(UserCreationForm):
    telefone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CadastroProfissionalForm(UserCreationForm):
    especialidade = forms.ModelChoiceField(queryset=None)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    registro_profissional = forms.CharField(max_length=50)
    valor_consulta = forms.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Especialidade
        self.fields["especialidade"].queryset = Especialidade.objects.all()


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["data_hora"]
        widgets = {
            "data_hora": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

    def clean_data_hora(self):
        data_hora = self.cleaned_data["data_hora"]
        if data_hora < timezone.now():
            raise forms.ValidationError("Não é possível agendar uma consulta em uma data/horário que já passou.")
        return data_hora


class EditarPerfilProfissionalForm(forms.ModelForm):
    class Meta:
        model = PerfilProfissional
        fields = ["especialidade", "bio", "registro_profissional", "valor_consulta"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class EditarPerfilPacienteForm(forms.ModelForm):
    class Meta:
        model = PerfilPaciente
        fields = ["telefone"]