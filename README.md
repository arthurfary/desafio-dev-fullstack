# Todos
## Aplicativo simples de lista de tarefas (*to-dos*).

---

# Quickstart

Para rodar, basta clonar o repositório e rodar Docker compose na pasta *root*:

```sh
git clone LINK_REPO
docker compose up --build
```

Após isso, o Docker vai tomar conta de baixar, configurar e inicializar tuno necessário para o projeto.

> Nota: O backend roda em modo 'dev', é recomendado o uso de um WSGI para deploy em produção, optei por manter em modo dev para reduzir o overhead de desenvolvimento inicial.

# Rodando localmente

Para desenvolvimento, é mais convenineto rodar ambos os servidores localmente, para isso, basta fazer o uso dos seguintes comandos:

## Backend
> Dentro do diretório `backend/`

```sh
# Crie um ambiente virtual e execute-o
python -m venv .venv
. .venv/bin/activate

# Instale as dependencias
pip install -r requirements.txt

# Inicie o servidor de dev com o flask
flask --app api run --debug

# Ou simplesmente
python api.py

# Por fim, rode os testes usando
pytest test_api.py
```

## Frontend
> Dentro do diretório `frontend/`

```sh
# Instale dependências
npm install

# E rode o servidor de desenvolvimnento com
npm run dev
```



Python back + React front to-do app!
