from django.db import migrations

ESPECIALIDADES = [
    "Clínico Geral",
    "Cardiologia",
    "Dermatologia",
    "Ginecologia",
    "Pediatria",
    "Psicologia",
    "Nutrição",
    "Fisioterapia",
    "Ortopedia",
    "Psiquiatria",
]


def seed_especialidades(apps, schema_editor):
    Especialidade = apps.get_model("consultas", "Especialidade")
    for nome in ESPECIALIDADES:
        Especialidade.objects.get_or_create(nome=nome)


def remove_especialidades(apps, schema_editor):
    Especialidade = apps.get_model("consultas", "Especialidade")
    Especialidade.objects.filter(nome__in=ESPECIALIDADES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("consultas", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_especialidades, remove_especialidades),
    ]
