# Sistema de Agendamento – Laboratório de Anatomia

Este projeto consiste em um sistema web para gerenciamento de salas e agendamentos em um laboratório de anatomia, desenvolvido como atividade acadêmica.

## 🎯 Objetivo

Facilitar o controle de uso das salas do laboratório, permitindo:
- Visualizar disponibilidade
- Criar agendamentos
- Registrar reservas
- Cancelar agendamentos

## 🧱 Arquitetura

O sistema utiliza uma arquitetura em camadas:

- **Frontend:** HTML, CSS e JavaScript puro
- **Backend:** Python com FastAPI
- **Banco de Dados:** MySQL
- **ORM:** SQLAlchemy
- **Validação:** Pydantic

Comunicação realizada via API REST utilizando JSON.

## 🗄️ Modelagem do Banco

Principais tabelas:
- Usuario
- Sala
- Agendamento
- Reserva

Com uso de chaves primárias, chaves estrangeiras e integridade referencial.

## 🚀 Como executar o projeto

### 1️⃣ Banco de Dados

Crie o banco no MySQL:

```sql
CREATE DATABASE laboratorio_anatomia;

Configure o acesso no arquivo database.py.

2️⃣ Backend

Instale as dependências:

pip install fastapi uvicorn sqlalchemy mysql-connector-python


Execute o servidor:

uvicorn main:app --reload


A API ficará disponível em:

http://127.0.0.1:8000


Documentação automática:

http://127.0.0.1:8000/docs

3️⃣ Frontend

Abra o arquivo index.html no navegador.

📌 Funcionalidades

Listagem de salas

Consulta de disponibilidade

Criação de agendamentos

Reserva de salas

Cancelamento de agendamentos

🧪 Tecnologias Utilizadas

Python

FastAPI

MySQL

SQLAlchemy

Pydantic

HTML

JavaScript

📚 Contexto Acadêmico

Projeto desenvolvido com fins acadêmicos, integrando conceitos de:

Banco de dados relacionais

APIs REST

Programação web

Arquitetura de sistemas

✨ Autora

Daniela Oliveira


