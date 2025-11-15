# ProjetoEstoquePI
# 📦 Projeto Cadastro de Usuários

Sistema web de cadastro e gerenciamento de usuários, projetos e estoque desenvolvido com Django.

---

## 📋 Requisitos do Projeto

### **Ambiente**
- **Python**: 3.13.2 (ou superior)
- **Framework**: Django 5.1.7
- **Banco de Dados**: SQLite3


---



## 📁 Estrutura do Projeto

```
projeto_cad_usuarios/
├── app_cad_usuario/              # Aplicação principal
│   ├── migrations/               # Migrações do banco de dados
│   ├── templates/                # Templates HTML
│   │   └── usuario/
│   │       ├── pagina_inicial.html
│   │       ├── login.html
│   │       ├── projetos.html
│   │       ├── estoque.html
│   │       ├── historico.html
│   │       ├── alterar_email.html
│   │       ├── alterar_nome.html
│   │       └── alterar_senha.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # Modelos de dados
│   ├── views.py                  # Lógica das views
│   └── tests.py
├── projeto_cad_usuarios/         # Configuração do projeto
│   ├── settings.py               # Configurações principais
│   ├── urls.py                   # URLs do projeto
│   ├── asgi.py
│   └── wsgi.py
├── staticfiles/                  # Arquivos estáticos (CSS, JS, etc.)
├── templates/                    # Templates globais
├── db.sqlite3                    # Banco de dados (criado automaticamente)
├── manage.py                     # Script de gerenciamento do Django
├── requirements.txt              # Dependências do projeto
└── README.md                     # Este arquivo
```

---

## 🔑 Funcionalidades Principais

- ✅ **Autenticação de Usuários** - Login e logout seguro
- ✅ **Gerenciamento de Perfil** - Alterar nome, email e senha
- ✅ **Gerenciamento de Projetos** - Criar, visualizar e concluir projetos
- ✅ **Controle de Estoque** - Adicionar e consultar materiais
- ✅ **Histórico** - Visualizar ações realizadas

---



---



**Desenvolvido com ❤️ usando Django 5.1.7**
