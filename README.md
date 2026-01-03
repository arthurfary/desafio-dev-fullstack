# Todos
### Aplicativo simples de lista de tarefas (*to-dos*).


# Quickstart

Para rodar, basta clonar o repositório e rodar Docker compose na pasta *root*:

```sh
git clone LINK_REPO
docker compose up --build
```

Após isso, o Docker vai tomar conta de baixar, configurar e inicializar tuno necessário para o projeto.

O backend está documentado em swagger, e informações sobre as rotas pode ser encontrados em [http://localhost:5000](http://localhost:5000/).

> Nota: O backend roda em modo 'dev', é recomendado o uso de um WSGI para deploy em produção, optei por manter em modo dev para reduzir o overhead de desenvolvimento inicial.

# Rodando localmente

Para desenvolvimento, é mais conveninete rodar ambos os servidores localmente, para isso, basta fazer o uso dos seguintes comandos:

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

# E rode o servidor de desenvolvimento com
npm run dev
```
# Endpoints
Os endpoints desse projeto foram feitos seguindo rigorosamente os requisitados na proposta do desafio.
Eles podem ser mais facilmente explorados e compreendidos na documentação automática swagger disponivel em [http://localhost:5000](http://localhost:5000/) (após rodar o serviço do backend).

- GET /tasks → lista todas as tarefas
  - Retorna uma lista com todas as tarefas:
    ```json
    [
      {
          "id": 1,
          "titulo": "Tarefa 1",
          "descricao": "descricao tarefa 1",
          "status": "pendente",
          "dataCriacao": "2026-01-03 03:27:35"
      },
      {
          "id": 2,
          "titulo": "Tarefa 2",
          "descricao": "descricao tarefa 2",
          "status": "pendente",
          "dataCriacao": "2026-01-03 03:27:37"
      },
      ...
    ]
    ```
- POST /tasks → cria nova tarefa
  - Cria uma tarefa "em branco" (dummy) nova. Formato de retorno:
    ```json
    {
      "message": "Task created"
    }
    ```
- PUT /tasks/{id} → atualiza tarefa
  - Atualiza uma tarefa, Formato de retorno:
    ```json
    {
      "message": "Task created"
    }
    ```
- DELETE /tasks/{id} → remove tarefa
  - Deleta uma tarefa, Formato de retorno:
    ```json
    {
      "message": "Task deleted"
    }
    ```
    
# Raciocínio, Decisões
### Tecnologias:
A decisão de utilizar `flask` e `sqlite3` para o backend foi tomada devido a familiaridade que tenho com as ferramentas, utilizei destas em diversos outros projetos e elas se provam completas, rápidas e intuitivas.

Fiz questão de me aprofudnar e configurar o `CORS` (utilziando `flask-cors`) corretamente. Na internet, muitas vezes é recomendado uma solução "tapa buraco", que permite conexão de todos os hosts. Essa interação é extremamente insegura, portantanto criei uma lista de hosts e metodos permitidos pelo CORS.

O `flask_restx` foi novidade para mim. Porém após usá-lo para gerar a documentação Swagger, posso afirmar que continuarei utilizando-o para projetos futuros. Sua tipagem explicita de estruturas (modelos) de resposta incentivam o desenvolvedor a pensar ativamente como sua API vai ser consumida e, posteriormente, documentada.

O banco de dados `sqlite3` foi confgurado para seguir as especificações do desafio. Debati por um tempo em adicionar o `AUTOINCREMENT` no id das tarefas (assim garantindo que não haveriam ids repetidos mesmo após deleção) mas optei por utilizar o sistema de ids padrão do `sqlite3` devido ao escopo pequeno da ferramenta. 

Para o front end, utilizei de um projeto de react *bare bones*, com o [Create Vite App](https://vite.dev/guide/) (Launcher que permite criar varios tipos de projetos em frameworks de js), optei também por Typescript por sua tipagem explicita.
Optei por utilizar alguns componentes para coesão, e CSS puro pela simplicidade e escopo do projeto.

### Documentação e Uso de IA
Para esse projeto, utilizei principalmente documentação para construir as funcionalidades básicas do projeto, também utilizeis fórums como Stack Overflow para esclarecimento. Fiz questão de procurar a fundo as boas práticas da tecnologias que estava utilizando antes de implementá-la (como por exemplo, os cursores do banco de dado sqlite3 e como melhor utilizá-los e quando reutilizá-los). Essa afirmação pode ser validada no histórico de commits do projeto.

Após as funcionalidades principais estabelecidas, utilizei da IA como uma ferramenta para agilizar de tarefas não sensíveis (como criar a base do CSS e formatação visual de código). 

### Docker
Esta foi minha primeira experiencia criando uma infraestrutura com Docker, embora ja tivesse utilzado antes (rodando containers prontos). Acredito que essa ferramenta é essencial, sua habilidade de reduzir/remover o tempo de setup é fenomenal, e a consistência que ela proporciona é extremamente necessária.
Continuarei utilizando-a em projetos futuros.

# Conclusões
Este foi um projeto muito divertido de se trabalhar, ofereceu uma gama interessante de desafios e me proporcionou a oportunidade de utilizar e aprender ferramentas como Docker e Swagger. Agradeço pela oportunidade!

