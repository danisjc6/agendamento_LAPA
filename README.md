Sistema de Agendamento – Laboratório de Anatomia

Sistema web para gerenciamento de salas e agendamentos em um laboratório de anatomia, desenvolvido como atividade acadêmica na disciplina de Banco de Dados.

🎯 Objetivo

Facilitar o controle de uso das salas do laboratório, permitindo:

Visualizar salas disponíveis

Criar e gerenciar agendamentos

Registrar reservas

Cancelar agendamentos

🧱 Arquitetura do Sistema

O sistema segue uma arquitetura em camadas:

Frontend: HTML, CSS e JavaScript puro

Backend: Python com FastAPI

Banco de Dados: MySQL

ORM: SQLAlchemy

```sql

CREATE DATABASE laboratorio_anatomia;

A comunicação é realizada via API REST, utilizando JSON.

🗂️ Modelagem do Banco de Dados
📌 Esquema Conceitual (MERE)

O modelo conceitual contempla as seguintes entidades principais:

Usuário

Sala

Agendamento

Reserva

Relacionamentos:

Um usuário pode realizar vários agendamentos

Um agendamento pode estar associado a uma sala por meio de uma reserva

(Diagrama conceitual pode ser inserido aqui como imagem ou link)

📌 Esquema Lógico (Modelo Relacional)

Tabelas resultantes da transformação do MERE:

usuarios

salas

agendamentos

reservas

Com uso de:

Chaves primárias

Chaves estrangeiras

Integridade referencial

📖 Dicionário de Dados (Resumo)
Tabela: Usuario
| Campo     | Tipo         | Restrições | Descrição                |
| --------- | ------------ | ---------- | ------------------------ |
| matricula | INT          | PK         | Identificador do usuário |
| nome      | VARCHAR(100) | NOT NULL   | Nome do usuário          |
| email     | VARCHAR(100) |            | Email                    |
| telefone  | VARCHAR(20)  |            | Contato                  |
| curso     | VARCHAR(100) |            | Curso do usuário         |

Tabela: Sala
| Campo      | Tipo         | Restrições | Descrição             |
| ---------- | ------------ | ---------- | --------------------- |
| id_sala    | INT          | PK         | Identificador da sala |
| nome_sala  | VARCHAR(100) | NOT NULL   | Nome da sala          |
| tipo       | VARCHAR(50)  |            | Tipo da sala          |
| capacidade | INT          |            | Capacidade máxima     |

Tabela: Agendamento
| Campo      | Tipo         | Restrições | Descrição                   |
| ---------- | ------------ | ---------- | ----------------------------|
| id         | INT          | PK         | Identificador do agendamento|
| matricula  | INT          | NOT NULL   | matricula do usuário        |
| data       | date         |            | Data do agendamento         |
| hora_inicio| time         |            | horário do início do agendam|
| hora_fim   | time         |            | horário do fim do agendam.  |
| finalidade | varchar(100) |            | Aula, palestra, evento, etc |
| status     | varchar(100) |            | ativo, cancelado            |

Tabela: Reserva
| Campo         | Tipo        | Restrições | Descrição                   |
| ------------- | ------------| ---------- | ----------------------------|
| id_agendamento| INT         | PK         | Identificador do agendamento|
| nome_sala     | varchar(100)| NOT NULL   | Nome da sala                |


🧪 Normalização

O banco de dados encontra-se normalizado até a Segunda Forma Normal (2FN), garantindo:

Eliminação de dependências parciais

Não redundância de dados

Integridade relacional

🐳 Execução com Docker
Pré-requisitos

Docker

Docker Compose

Subir o sistema
docker compose up -d


Serviços criados:

MySQL

Backend FastAPI

🗄️ Criação e Carga do Banco de Dados

O banco é criado e povoado automaticamente via Docker, utilizando scripts SQL localizados na pasta:

/database
├── ddl.sql
└── dml.sql


schema.sql: criação das tabelas (DDL)

dados_iniciais.sql: inserção de dados de teste (DML)

🌐 Acesso ao Sistema

API: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

Frontend: abrir frontend_lab_anatomia/index.html

🧪 Tecnologias Utilizadas

Python

FastAPI

MySQL

SQLAlchemy

Pydantic

Docker

HTML, CSS e JavaScript

📚 Contexto Acadêmico

Projeto desenvolvido com fins acadêmicos, integrando conceitos de:

Modelagem conceitual e lógica de dados

Normalização

Bancos de dados relacionais

APIs REST

Programa

Containerização com Docker

✨ Autora

Daniela Oliveira



