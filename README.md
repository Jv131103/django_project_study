# django_project_study
Django project study

## 📑 Guias de Instalação
- [Instalação do Node.js](./INSTALL_NODE.md)
- [Instalação do Python](./INSTALL_PYTHON.md)
- [Instalação do SQL](./INSTALL_SQL.md)

## 📑 Guias de Documentação
- [Sistema Empresarial ERP](./doc/sistema_empresarial.txt)
- [IDE VS EDITOR DE CÓDIGO FONTE](./doc/ide_vs_editor.txt)
- [EXTRAS DE DOCUMENTACAO](./doc/django/)

# Guia para o Django

> Setup rápido com ambiente virtual + instalação via `requirements.txt`.

## 📑 Índice
- [Pré-requisitos](#pré-requisitos)
- [Criar ambiente virtual (venv)](#criar-ambiente-virtual-venv)
- [Instalar dependências](#instalar-dependências)
- [Variáveis de ambiente (.env)](#variáveis-de-ambiente-env)
- [Migrações e usuário admin](#migrações-e-usuário-admin)
- [Rodar o servidor](#rodar-o-servidor)
- [Conectar ao banco (Docker)](#conectar-ao-banco-docker)
- [Gerar/atualizar requirements.txt](#geraratualizar-requirementstxt)
- [Dicas e solução de problemas](#dicas-e-solução-de-problemas)

---

## ✅ Pré-requisitos
- Python **3.10+**
- `pip` atualizado: `python -m pip install --upgrade pip`
- (Opcional) Docker + Docker Compose para usar bancos locais

---

## Criar ambiente virtual (venv)

> Aqui usei **venv** nativo do Python. (Se preferir, pode usar `virtualenv`, `poetry` ou `pdm`.)

```bash
# Dentro da pasta do projeto
python -m venv .venv

# Ativar o venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

Confirme que está ativo (o prompt geralmente mostra `(.venv)`).

---

## Instalar dependências

> Com o venv ativo:

```bash
pip install -r requirements.txt
```

Se não existir `requirements.txt`, veja a seção **[Gerar/atualizar requirements.txt](#geraratualizar-requirementstxt)**.

---

## Variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (ou use o método que preferir) e configure o mínimo necessário:

```ini
# DEBUG/SECRET
DEBUG=1
SECRET_KEY=troque-esta-chave

# Exemplo com SQLite (padrão do Django)
DATABASE_URL=sqlite:///db.sqlite3

# Exemplos para bancos em Docker (ajuste conforme seu setup):
# MariaDB
# DATABASE_URL=mysql://app:app123@127.0.0.1:3308/appdb
# MySQL
# DATABASE_URL=mysql://app:app123@127.0.0.1:3307/appdb
# PostgreSQL
# DATABASE_URL=postgres://app:admin123@127.0.0.1:5433/appdb
```

> Dica: para usar `DATABASE_URL`, instale `dj-database-url` e, no `settings.py`, faça o parse.

```python
# settings.py (exemplo)
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "chave-insegura-dev")
DEBUG = os.getenv("DEBUG", "0") == "1"

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
        conn_max_age=600,
    )
}
```

---

## Migrações e usuário admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Rodar o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

---

## Conectar ao banco (Docker)

Se você subiu os bancos com Docker usando profiles e `.env`:

- **MariaDB** → Host: `127.0.0.1` • Porta: `3308` • DB: `appdb` • User: `app` • Senha: `app123`  
  `DATABASE_URL=mysql://app:app123@127.0.0.1:3308/appdb`

- **MySQL 8.4** → Host: `127.0.0.1` • Porta: `3307` • DB: `appdb` • User: `app` • Senha: `app123`  
  `DATABASE_URL=mysql://app:app123@127.0.0.1:3307/appdb`

- **PostgreSQL 16** → Host: `127.0.0.1` • Porta: `5433` • DB: `appdb` • User: `app` • Senha: `admin123`  
  `DATABASE_URL=postgres://app:admin123@127.0.0.1:5433/appdb`

> Instale os drivers conforme o banco escolhido:
> - MySQL/MariaDB: `pip install mysqlclient` *(recomendado)* ou `pip install pymysql`  
>   (Se usar PyMySQL, adicione em `__init__.py`: `import pymysql; pymysql.install_as_MySQLdb()`.)
> - PostgreSQL: `pip install psycopg[binary]` (ou `psycopg2-binary`)

---

## Gerar/atualizar `requirements.txt`

```bash
# Congelar libs do ambiente virtual:
pip freeze > requirements.txt
```

> Dica: mantenha versões fixas para builds reprodutíveis.

---

## Dicas e solução de problemas

- **Ativação do venv**: se `command not found`, verifique se ativou o `.venv` correto.
- **Erro de driver de banco**:
  - MySQL/MariaDB: instale `mysqlclient` (pode exigir `libmysqlclient-dev`)  
    ```bash
    # Debian/Ubuntu
    sudo apt-get update && sudo apt-get install -y default-libmysqlclient-dev build-essential
    pip install mysqlclient
    ```
  - PostgreSQL:  
    ```bash
    sudo apt-get update && sudo apt-get install -y libpq-dev build-essential
    pip install "psycopg[binary]"
    ```

- **Múltiplos bancos em Docker**: garanta portas distintas (já estão no seu compose).
- **Arquivos que vale ignorar** (`.gitignore`):
  ```
  .venv/
  __pycache__/
  *.pyc
  *.sqlite3
  .env
  ```

---

✅ Pronto! Com isso você tem:
1) Ambiente virtual isolado
2) Dependências instaladas  
3) Banco local (SQLite ou Docker)  
4) Projeto rodando em `runserver`
