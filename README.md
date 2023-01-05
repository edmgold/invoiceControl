


# Invoice Control

O objetivo deste projeto é implementar uma solução de controle de boletos mesclando recursos de fila, backend api e webhhook. 

## Objetivo Funcional

Precisamos criar um sistema de cobrança que:

-   Seja capaz de receber uma lista via API, com um CSV de nomes, CPFs, e-mails, valor da divida, vencimento da divida e cod. da divida.

```
name,governmentId,email,debtAmount,debtDueDate,debtId
John [Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-12,8291](<mailto:Doe,11111111111,johndoe@kanastra.com.br>,1000000.00,2022-10-12,8291) 

```

-   Baseado nos inputs, o sistema precisa regularmente gerar os boletos p/ cobrança e disparar e-mails cobrando a lista
-   O sistema também precisa ser capaz de receber uma comunicação JSON do banco (_**webhook**_), avisando que um boleto foi pago e liquidado diretamente em nossa conta bancária, para dar baixa desse boleto no sistema. Exemplo de payload do webhook JSON que iremos receber para cada registro de pagamento:

```json
{
	"debtId": "8291",
	"paidAt": "2022-06-09 10:00:00",
	"paidAmount": 100000.00,
	"paidBy": "John Doe"
}

```

## Recursos

Para a construção da solução, foi utilizado Python com o framework web FastApi. 
Para construir o processamento de boletos e envio de emails, foi utilizado Celery junto com o broker RabitMQ.
O projeto ainda conta com a biblioteca Alembic para as migrations, Ormar (sqlalchemy) como ORM.


## Como testar
Para facilitar os testes foi criado uma estrutura de docker-compose para subir todos os recursos necessários.
Para isto, basta ter o [docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-pt) instalado, baixar o projeto e utilizar o comando `make docker`.
O projeto irá subir localmente na pasta 8000.
Nativamente, o FastApi conta com swagger e redoc que poderão ser acessados através das rotas http://localhost:8000/docs e http://localhost:8000/redoc.


## *Observações*

 - Por motivos de simplicidade, foi utilizado o sqlite como banco de
   dados, mas a estrutura de orm permite trocar tranquilamente para um
   outro sgbd relacional qualquer.
 - Apesar de não ser uma prática recomendável, subi o .env junto com a
   aplicação e chaves de teste afim de facilitar a avaliação do projeto.
 - O projeto encontra-se com 87% de cobertura de testes
