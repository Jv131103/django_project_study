# Instalação do SQL

Para este projeto usaremos **MySQL**, mas você pode optar por **MariaDB** ou **PostgreSQL** se preferir. Abaixo há **duas rotas**:

- **Opção A — Instalação manual** do MySQL na sua máquina.
- **Opção B — Usar o projeto Docker** já pronto (**DatabasesDocker**) para subir o banco com persistência e `.env` padronizado.

> Dica: se você quer ir direto ao ponto, **recomendamos a Opção B (Docker)** pela praticidade e reprodutibilidade.

---

## Opção A — Instalação manual (MySQL)

### Windows
1. Baixe o **MySQL Community Server** no site oficial.
2. Instale com o **MySQL Installer** (escolha Server + Workbench se quiser GUI).
3. Guarde a **senha do `root`** definida no instalador.

### macOS
- Com Homebrew:
  ```bash
  brew install mysql
  brew services start mysql
  ```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl enable --now mysql
```

### Linux (RHEL/Fedora)
```bash
sudo dnf install @mysql
sudo systemctl enable --now mysqld
```

### Verificar instalação
```bash
mysql --version
mysql -u root -p -h 127.0.0.1 -P 3306
```

### Criar banco e usuário do projeto
Entre no cliente (`mysql -u root -p`) e rode:
```sql
CREATE DATABASE appdb;
CREATE USER 'app'@'%' IDENTIFIED BY 'app123';
GRANT ALL PRIVILEGES ON appdb.* TO 'app'@'%';
FLUSH PRIVILEGES;
```

> **Conexão padrão do projeto** (ajuste conforme seu ambiente):  
> Host: `127.0.0.1` • Porta: `3306` • DB: `appdb` • User: `app` • Pass: `app123`

> **Cliente SQL** (opcional): veja [INSTALLDBEAVER.md](./INSTALLDBEAVER.md) para instalar e configurar o **DBeaver**.

---

## Opção B — Usar Docker (recomendado)

Você pode subir o MySQL usando o projeto **DatabasesDocker**, que já vem com **Docker Compose + profiles** e **persistência** de dados.  
Abra em outra aba para mais detalhes e instruções completas:  
**DatabasesDocker (GitHub)**: <https://github.com/Jv131103/DatabasesDocker>

### Passo a passo rápido
1. **Clonar o repositório** (em uma pasta fora do seu projeto atual, por exemplo `~/dev/DatabasesDocker`):
   ```bash
   git clone https://github.com/Jv131103/DatabasesDocker.git
   cd DatabasesDocker/db-stack
   ```
2. **Configurar variáveis**: copie o exemplo e ajuste portas/credenciais se quiser.
   ```bash
   cp .env-example .env
   # edite o arquivo .env com seu editor favorito
   ```
3. **Subir apenas o MySQL** (usando profile `mysql`):
   ```bash
   docker compose --profile mysql up -d
   ```
4. **Acompanhar logs** (útil até passar no healthcheck):
   ```bash
   docker compose logs -f
   ```
5. **Testar conexão** (cliente dentro do container ou DBeaver):
   - Dentro do container:
     ```bash
     docker exec -it mysql84 mysql -u root -p
     ```
   - No **DBeaver** (ou similar):  
     Host: `127.0.0.1` • Port: `3307` • DB: `appdb` • User: `app` • Pass: `app123`

> As portas e credenciais são definidas no `.env` do **DatabasesDocker**. Os valores padrão (exemplo) são:
>
> - **MYSQL_PORT**=`3307`  
> - **MYSQL_DATABASE**=`appdb`  
> - **MYSQL_USER**=`app`  
> - **MYSQL_PASSWORD**=`app123`  
> - **MYSQL_ROOT_PASSWORD**=`admin123`

### Parar/Remover
```bash
# Parar somente o serviço MySQL
docker compose --profile mysql down

# Remover volumes (apaga os dados!)
docker compose --profile mysql down -v
```

### Trocar de banco (MariaDB/PostgreSQL)
O mesmo repositório permite subir **MariaDB** ou **PostgreSQL** apenas mudando o `--profile`:
```bash
# MariaDB
docker compose --profile mariadb up -d

# PostgreSQL
docker compose --profile postgres up -d
```

---

## Conectar o seu projeto a esse banco

No seu projeto (aplicação), configure a string de conexão conforme os valores do `.env` do banco. Exemplos:

### MySQL (padrão do DatabasesDocker)
- **Host**: `127.0.0.1`  
- **Porta**: `3307`  
- **Database**: `appdb`  
- **Usuário**: `app`  
- **Senha**: `app123`

### Exemplo de URL (Django / SQLAlchemy)
```text
# Django (django-environ)
DATABASE_URL=mysql://app:app123@127.0.0.1:3307/appdb

# SQLAlchemy
mysql+pymysql://app:app123@127.0.0.1:3307/appdb
```

> Para **DBeaver** (cliente SQL), consulte [INSTALLDBEAVER.md](./INSTALLDBEAVER.md).

---

## Dicas e Solução de Problemas (FAQ)

- **Erro de autenticação (MySQL/MariaDB)**  
  Entre no container e recrie o usuário:
  ```sql
  CREATE USER 'app'@'%' IDENTIFIED BY 'app123';
  GRANT ALL PRIVILEGES ON appdb.* TO 'app'@'%';
  FLUSH PRIVILEGES;
  ```

- **Não consigo conectar em `localhost`**  
  Prefira `127.0.0.1` (evita problemas de resolução/IPv6).

- **O serviço está subindo, mas a conexão falha**  
  Veja os logs até o healthcheck ficar OK:
  ```bash
  docker compose logs -f
  ```

- **Quero mudar portas/credenciais**  
  Edite o arquivo `.env` do **DatabasesDocker** e reinicie o serviço.

- **Quero usar PostgreSQL**  
  Altere o profile para `postgres` e ajuste a string de conexão (porta padrão do exemplo: `5433`).

---

## Segurança (produção)

- **Altere as senhas padrão** e limite privilégios do usuário da aplicação.  
- **Segregue ambientes** (dev/homolog/produção) e variáveis por `.env`.  
- Configure **backup/restore** do volume de dados.  
- Em produção, prefira conexões seguras (TLS) e **firewall**/restrições de acesso.

---

Pronto! Agora você pode instalar o SQL **manualmente** ou **subir via Docker** com o projeto auxiliar **DatabasesDocker**. Para detalhes completos do stack Docker (múltiplos bancos, persistência e perfis), consulte:  
<https://github.com/Jv131103/DatabasesDocker>
