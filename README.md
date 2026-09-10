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

## Configuração para produção (Deploy)

`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` e a configuração de e-mail agora são lidos de
variáveis de ambiente, com valores padrão que funcionam sem configuração nenhuma para
rodar localmente. Para publicar (ex: PythonAnywhere):

1. Copie `.env.example` para `.env` e preencha os valores (veja os comentários dentro
   do arquivo). O `.env` nunca é enviado ao GitHub (já está no `.gitignore`).
2. No mínimo, defina:
   ```
   DJANGO_SECRET_KEY=uma-chave-nova-so-sua
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=seuprojetoo.pythonanywhere.com
   ```
3. (Opcional) Preencha `EMAIL_HOST`, `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` se
   quiserem que a recuperação de senha envie e-mail de verdade. Sem isso, o sistema
   continua funcionando normalmente, só que o "e-mail" aparece no log do servidor em
   vez de ser enviado.
4. No painel do PythonAnywhere, essas mesmas variáveis também podem ser definidas
   direto na aba "Web" → "Environment variables", como alternativa ao arquivo `.env`.

Gerar uma `SECRET_KEY` nova:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Outras observações

- `TIME_ZONE` foi ajustado para `America/Sao_Paulo` (estava em `UTC`), já que as
  consultas são agendadas por pacientes e profissionais no Brasil. Isso afeta como
  os horários são exibidos e como a validação de "não agendar no passado" é calculada.
