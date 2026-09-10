from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilPaciente, PerfilProfissional, Especialidade, Consulta
from .forms import (
    CadastroPacienteForm,
    CadastroProfissionalForm,
    AgendamentoForm,
    EditarPerfilProfissionalForm,
    EditarPerfilPacienteForm,
)


def home(request):
    return render(request, "consultas/home.html")


def cadastro_paciente(request):
    if request.method == "POST":
        form = CadastroPacienteForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            PerfilPaciente.objects.create(
                usuario=usuario,
                telefone=form.cleaned_data["telefone"]
            )
            login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("home")
    else:
        form = CadastroPacienteForm()
    return render(request, "consultas/cadastro_paciente.html", {"form": form})


def cadastro_profissional(request):
    if request.method == "POST":
        form = CadastroProfissionalForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            PerfilProfissional.objects.create(
                usuario=usuario,
                especialidade=form.cleaned_data["especialidade"],
                bio=form.cleaned_data["bio"],
                registro_profissional=form.cleaned_data["registro_profissional"],
                valor_consulta=form.cleaned_data["valor_consulta"]
            )
            login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("home")
    else:
        form = CadastroProfissionalForm()
    return render(request, "consultas/cadastro_profissional.html", {"form": form})


def buscar_profissionais(request):
    especialidade_id = request.GET.get("especialidade")
    profissionais = PerfilProfissional.objects.all()

    if especialidade_id:
        profissionais = profissionais.filter(especialidade_id=especialidade_id)

    especialidades = Especialidade.objects.all()
    return render(request, "consultas/buscar.html", {
        "profissionais": profissionais,
        "especialidades": especialidades
    })


def perfil_profissional(request, profissional_id):
    profissional = get_object_or_404(PerfilProfissional, id=profissional_id)
    return render(request, "consultas/perfil_profissional.html", {"profissional": profissional})


@login_required
def agendar_consulta(request, profissional_id):
    profissional_perfil = get_object_or_404(PerfilProfissional, id=profissional_id)
    profissional_user = profissional_perfil.usuario

    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            data_hora_escolhida = form.cleaned_data["data_hora"]

            # A validação mais importante: checar conflito de horário
            conflito = Consulta.objects.filter(
                profissional=profissional_user,
                data_hora=data_hora_escolhida,
                status="confirmada"
            ).exists()

            if conflito:
                messages.error(request, "Esse horário já está ocupado. Escolha outro.")
            else:
                Consulta.objects.create(
                    paciente=request.user,
                    profissional=profissional_user,
                    data_hora=data_hora_escolhida
                )
                messages.success(request, "Consulta agendada com sucesso!")
                return redirect("minhas_consultas")
    else:
        form = AgendamentoForm()

    return render(request, "consultas/agendar.html", {"form": form, "profissional": profissional_perfil})


@login_required
def minhas_consultas(request):
    is_profissional = hasattr(request.user, "perfilprofissional")
    if is_profissional:
        consultas = Consulta.objects.filter(profissional=request.user)
    else:
        consultas = Consulta.objects.filter(paciente=request.user)

    return render(request, "consultas/minhas_consultas.html", {
        "consultas": consultas,
        "is_profissional": is_profissional,
    })


@login_required
def editar_perfil(request):
    """
    Operação de UPDATE do CRUD: permite que o usuário logado edite
    o próprio perfil (profissional ou paciente), dependendo do tipo de conta.
    """
    if hasattr(request.user, "perfilprofissional"):
        perfil = request.user.perfilprofissional
        FormClasse = EditarPerfilProfissionalForm
    else:
        perfil, _ = PerfilPaciente.objects.get_or_create(usuario=request.user)
        FormClasse = EditarPerfilPacienteForm

    if request.method == "POST":
        form = FormClasse(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("editar_perfil")
    else:
        form = FormClasse(instance=perfil)

    return render(request, "consultas/editar_perfil.html", {"form": form})


@login_required
def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    # Segurança: só o próprio paciente ou profissional envolvido pode cancelar
    if request.user == consulta.paciente or request.user == consulta.profissional:
        consulta.status = "cancelada"
        consulta.save()
        messages.success(request, "Consulta cancelada.")

    return redirect("minhas_consultas")