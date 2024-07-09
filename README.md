### Bank Manager System RestAPI
**Abordagem:** 

Utilizado o Django Rest Framework para a criação de um sistema de logística de pedidos.

Criado os objetos em banco relacional **(PostgreSQL/SQLite)**:

**Account** 
- id
- balance

**Transaction** 
- account_id
- type
- value
- tax

Taxas:

**Taxa de débito:** 3% sobre a operação

**Taxa de crédito:** 5% sobre a operação

**Taxa do Pix:** Sem custo

Criado o app manager e o viewsets com os endpoints:

O endpoint "/conta" deve criar e fornecer informações sobre o número da conta e o saldo. 

- **POST /v1/conta/** que recebe um valor inicial e retorna o número da conta
    **Exemplo:**
    ```
    {
        "conta_id": 123
        "valor": 10
    }
    ```
    Retorna:
    ```
    {
        "conta_id": 123
        "saldo": 10
    }
    ```  

- **GET /v1/conta/?id=123 ou /v1/conta/?conta_id=123** retorna o saldo da conta
    **Exemplo:**
    ```
    {
        "conta_id": 123
        "saldo”: 10
    }
    ```
    **Filtros:**

      id: Identificador da conta (Int)

      conta_id: Identificador do conta (Int)


O endpoint "/transacao" será responsável por realizar diversas operações financeiras.

- **POST /v1/transacao/** cria uma transação conforme o tipo de pagamento, gera taxa e retorna o saldo da conta
    **Exemplo:**
    ```
    {
        "forma_pagamento": "P", 
        "conta_id": 123, 
        "valor":10
    }
    ```
    Retorna:
    ```
    {
        "conta_id": 123
        "saldo”: 0
    }
    ```  


**Por que desta abordagem?**

**Por que usei o Django Rest?** Utilizei está abordaggem pelo meu conhecimento em Django Rest

e por já ter um projeto base para a criação de sistemas com autenticação, base de viewset e testes.

**Por que usei o banco relacional?** Por ser um banco de dados que facilita a busca de dados e reduz a duplicidade, 

além de que é facilmente integrado ao Django e possui suporte para consultar com filtros e ordenação.

**Por que usei o Docker?** Utilizei o Docker para facilitar a execução do projeto em qualquer ambiente,


**Adicionais**

Utilizado RabbitMQ para a criação de filas de mensagens para a realização de transações assíncronas.
Utilizado Celery para a criação de tarefas assíncronas para a realização de transações.
Utilizado Redis para a criação de cache de mensagens para a realização de transações assíncronas.


### Run in:
```
http://localhost:8000/docs/
```


### Docker PostgreSQL:
```
You need to create .env like example_env file

sudo docker-compose -f docker-compose-postgresql.yml up
```


### Docker SQLite3:
```
sudo docker-compose -f docker-compose-sqlite.yml up
```


### Configurations .env: 
```
Copy .env.example to .env
Set your environment variables on .env file
Use variables with the same names as you use when creating the database
```


### Environment: 
Python Version 3.8.10
```
python3 -m venv venv 
OR
virtualenv --python=python3 venv

source venv/bin/activate

cd django/
```


### Database - POSTGRES (Linux): 
```
sudo -i -u postgres
psql
CREATE USER user_default WITH PASSWORD 'password_default';
ALTER USER user_default CREATEDB;
CREATE DATABASE vl_database;
ALTER DATABASE vl_database OWNER TO user_default;
CREATE EXTENSION pg_trgm;
```


### Requirements: 
```
pip install -r requirements.txt
```


### Migration: 
```
python manage.py migrate
```


### Collect Staticfiles: 
```
python manage.py collectstatic   
```


### Run: 
```
python manage.py runserver
```


### Documentation: 
```
/docs
/docs/redoc
```


### Create User and Access Token in API: 
```
Use endpoint /auth/signup/ 
Before use /auth/jwt/create/ 

Now you have your access_token and refresh_token
```


### Use Authenticate Token: 
```
Bearer {access_token}
```


### Create Super User / Login: 
```
python manage.py createsuperuser 

To login use email and password

Already have a super user in database: admin@admin.com / admin
```


### Unit Tests: 
```
python manage.py test --failfast manager
```


### Unit Tests Report HTML: 
```
coverage run --source='./manager' manage.py test
coverage report

coverage html
HTML report: django/htmlcov/index.html
```


### New translations:
```
python manage.py makemessages --locale pt_BR

Change to pt-br on settings:
LANGUAGE_CODE= 'pt-BT'

Obs: If necessary translate to portuguese.
```


### Debug and traceback:
```
Need to set DEBUG=True in .env file

Need to set ENVIRONMENT_MODE=dev in .env file
```

## Copyright and license

Code released under the [freeBSD License](https://github.com/Henriquejdc/BankManager/blob/master/LICENSE.md).
