

# Principais tecnologias usadas
- **Infra**: docker, docker-compose, pip
- **DB**: postgres
- **Backend**: Django, Django Rest Framework
- **Test**: coverage, pytest
- **Lint**: Black, Flake8
- **Lib**: CreditCard



# Instalação

O Projeto possui docker e docker-compose, para ser instalado deve seguir o compose que se encontra na raiz do projeto
Nele se encontra uma configuração do projeto em Django e um Banco de Dados em Postgres

### OBS: So esta com .env no repositório para facilitar a instala.

```bash
    docker-compose up --build
```
# Autenticação e autorização

Para fazer as requisições é necessário passa o token de um usuário valido. Para isso, um usuário é criado ao automaticamente para teste.

Para pegar o token acesse o endpoint abaixo com os dados do usuário.

```bash
    usuario = pedro
    senha = 123456
```

|Verb  |URI Pattern
:----:|-------------------------|
| POST  | /api-token-auth/


Realize um Post para o endpoint /api-token-auth/ para pegar o token do usuario.

```bash
curl --location 'http://localhost:8000/api-token-auth/' \
--header 'Content-Type: application/json' \
--data '{
"username": "pedro",
"password": "123456"
}'
```

# Criar cartão de credito

Para criar o cartão você deve passar os dados do cartão e o token do usuário.


|Verb  |URI Pattern
:----:|-------------------------|
| POST  | /api/v1/credit_card/


```bash
curl --location 'http://localhost:8000/api/v1/credit_card/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token d522c66d29689a63e348a74defc469fa622f35f8' \
--data '{
    "exp_date": "10/2222",
    "holder": "Fulano",
    "number": "5555666677778884",
    "cvv": 123
}'
```

# Pegar os dados do cartão.
## Retornar todos os cartões do usuário
Para pegar todos os cartões basta acessar o endpoint abaixo com o token do usuário.

|Verb  |URI Pattern
:----:|-------------------------|
| GET  | /api/v1/credit_card/


```bash
curl --location 'http://localhost:8000/api/v1/credit_card/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token d522c66d29689a63e348a74defc469fa622f35f8'
```

## Retornar um cartão especifico do usuário



|Verb  |URI Pattern
:----:|-------------------------|
| GET  | /api/v1/credit_card/id/

```bash
curl --location 'http://localhost:8000/api/v1/credit_card/1/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token d522c66d29689a63e348a74defc469fa622f35f8'
```

## Executar os Testes

Para executar os testes com docker-compose

```bash
  docker-compose run django pytest source
```


## Relacionado


[Página do Desafio](https://github.com/MaisTodos/backend-python-creditcard)
