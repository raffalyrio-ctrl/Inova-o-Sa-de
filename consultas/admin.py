from django.contrib import admin
from .models import Especialidade, PerfilPaciente, PerfilProfissional, Consulta

@admin.register(PerfilProfissional)
class PerfilProfissionalAdmin(admin.ModelAdmin):
    list_display = ("usuario", "especialidade", "valor_consulta")
    search_fields = ("usuario__username", "especialidade__nome")

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "profissional", "data_hora", "status")
    search_fields = ("paciente__username", "profissional__username")
    list_filter = ("status",)

admin.site.register(Especialidade)
admin.site.register(PerfilPaciente)