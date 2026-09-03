# Inovação Saúde (Django)

Plataforma para paciente buscar profissionais de saúde por especialidade e agendar consultas.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate        # já cria algumas especialidades de exemplo
python manage.py createsuperuser  # opcional, para acessar /admin/

python manage.py runserver
```

Acesse http://127.0.0.1:8000/

## O que existe

- Cadastro de paciente (`/cadastro/paciente/`)
- Cadastro de profissional, com especialidade, bio e valor da consulta (`/cadastro/profissional/`)
- Login / logout, com recuperação de senha por e-mail (`/login/`, `/password-reset/`)
- Busca de profissionais filtrando por especialidade (`/buscar/`)
- Perfil público do profissional com botão de agendar
- Agendamento de consulta, com checagem de horário já ocupado
- "Minhas consultas" — lista diferente para paciente e para profissional, com opção de cancelar

## O que foi corrigido em relação ao repositório original

O projeto já estava estruturado em Django, mas não rodava por causa de alguns bugs. Principais correções:

1. **Templates com nome errado** — as views chamavam `render(request, "cadastro_paciente.html", ...)`, mas os arquivos reais estavam em `templates/consultas/Cadastro paciente.html` (com espaço e maiúscula). Renomeei os arquivos para o padrão do Django (`cadastro_paciente.html`, `buscar.html`, etc.) e corrigi as chamadas em `views.py` para usar `consultas/nome_do_arquivo.html`.
2. **`{% url 'cadastro_cliente' %}`** — em `base.html` e `home.html` apontava para uma URL que não existe; a URL correta é `cadastro_paciente`.
3. **`minhas_consultas`** — o template usa `{% if is_profissional %}` mas a view nunca enviava essa variável no contexto; adicionei.
4. **Login** — `LoginView` apontava para `template_name="login.html"`, que não existe nesse caminho; corrigido para `consultas/login.html`.
5. **Recuperação de senha** — a home linkava para `{% url 'password_reset' %}`, mas essa URL nem existia. Adicionei as 4 rotas padrão do Django (`password_reset`, `password_reset_done`, `password_reset_confirm`, `password_reset_complete`) e criei os templates que faltavam.
6. **`MAILERS` em `settings.py`** — não é uma configuração que o Django reconhece; o nome certo é `EMAIL_BACKEND`. Corrigido (usa o backend de console, que imprime o e-mail no terminal — bom para testar sem precisar de servidor de e-mail real).
7. **JS quebrado em `home.html`** — o botão "Paciente/Profissional" no topo da home chamava `getBoundingPacientRect()` (não existe) em vez de `getBoundingClientRect()`, e o objeto `CONTENT` usava a chave `paciente` enquanto os botões usavam `data-mode="cliente"` — o troca-troca de modo não funcionava. Corrigido.
8. **Cadastro de especialidades** — sem nenhuma especialidade cadastrada, o formulário de profissional ficava vazio. Adicionei uma migration que já cria 10 especialidades comuns.

Testei o fluxo completo (cadastro de paciente, cadastro de profissional, login, busca, agendamento, cancelamento) de ponta a ponta e está funcionando.

## Observações para produção

- `DEBUG = True` e `SECRET_KEY` fixa no código — trocar antes de publicar de verdade.
- `ALLOWED_HOSTS` está vazio — precisa ser preenchido no deploy.
- `EMAIL_BACKEND` está configurado para console (só imprime no terminal); trocar por um provedor real (SMTP, SendGrid, etc.) quando for para produção.
