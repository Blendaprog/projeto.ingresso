# 🎟️ TicketShow

**Plataforma web de eventos e gerenciamento de ingressos.**

O TicketShow é um projeto desenvolvido em Python com Flask, com o objetivo de oferecer uma plataforma para visualizar eventos, gerenciar ingressos e administrar informações.

## ✨ Funcionalidades

- Cadastro e login de usuários.
- Autenticação com senhas protegidas por hash.
- Painel administrativo.
- Cadastro e gerenciamento de eventos.
- Gerenciamento de lotes de ingressos.
- Visualização e gerenciamento de ingressos.
- Persistência de dados com SQLite.
- Interface personalizada para navegação.

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## 🚀 Como executar localmente

**1. Clone o repositório:**

```bash
git clone https://github.com/Blendaprog/projeto.ingresso.git
```

**2. Entre na pasta:**

```bash
cd projeto.ingresso
```

**3. Crie um ambiente virtual:**

```bash
python -m venv .venv
```

**4. Ative o ambiente no Windows:**

```powershell
.venv\Scripts\activate
```

**5. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**6. Configure as variáveis de ambiente**, utilizando o arquivo `.env.example` como referência.

**7. Execute a aplicação:**

```bash
python app.py
```

Acesse pelo navegador:

`http://127.0.0.1:5000`

## 📁 Estrutura do projeto

| Arquivo/Pasta | Descrição |
|---|---|
| `app.py` | Aplicação e rotas Flask |
| `banco.py` | Operações com o banco SQLite |
| `modelos.py` | Modelos do sistema |
| `templates/` | Páginas HTML |
| `static/` | Arquivos CSS e recursos estáticos |
| `requirements.txt` | Dependências do projeto |

## 🔒 Segurança

- Senhas armazenadas utilizando hash.
- Banco de dados local SQLite.
- Arquivos de configuração e dados privados protegidos pelo `.gitignore`.

## 👩‍💻 Desenvolvedora

**Blendaprog**

Projeto desenvolvido para fins educacionais.

---

⭐ Obrigada por conhecer o TicketShow!