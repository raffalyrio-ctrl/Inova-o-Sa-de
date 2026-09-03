from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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