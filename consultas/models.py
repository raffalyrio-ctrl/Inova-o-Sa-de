from django.db import models
from django.contrib.auth.models import User

class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class PerfilPaciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.usuario.username


class PerfilProfissional(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    registro_profissional = models.CharField(max_length=50, blank=True)
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.usuario.username


class Consulta(models.Model):
    STATUS_CHOICES = [
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("concluida", "Concluída"),
    ]

    paciente = models.ForeignKey(User, related_name="consultas_paciente", on_delete=models.CASCADE)
    profissional = models.ForeignKey(User, related_name="consultas_profissional", on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmada")
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente} com {self.profissional} em {self.data_hora}"