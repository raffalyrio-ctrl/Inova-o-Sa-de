from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/paciente/", views.cadastro_paciente, name="cadastro_paciente"),
    path("cadastro/profissional/", views.cadastro_profissional, name="cadastro_profissional"),
    path("login/", auth_views.LoginView.as_view(template_name="consultas/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("buscar/", views.buscar_profissionais, name="buscar_profissionais"),
    path("profissional/<int:profissional_id>/", views.perfil_profissional, name="perfil_profissional"),
    path("profissional/<int:profissional_id>/agendar/", views.agendar_consulta, name="agendar_consulta"),
    path("minhas-consultas/", views.minhas_consultas, name="minhas_consultas"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("consulta/<int:consulta_id>/cancelar/", views.cancelar_consulta, name="cancelar_consulta"),
]