
# Sistema de Agendamento – Laboratório de Anatomia (LAPA)

Sistema web para gerenciamento de salas e agendamentos do Laboratório de Anatomia,
desenvolvido como atividade acadêmica.

---

## 🎯 Objetivo

Facilitar o controle de uso das salas do laboratório, permitindo:

- Cadastro de usuários
- Cadastro de salas
- Criação de agendamentos
- Registro de reservas
- Consulta de disponibilidade

---

## 🧱 Arquitetura do Sistema

O projeto segue uma arquitetura em camadas:

- **Frontend:** HTML, CSS e JavaScript puro
- **Backend:** Python (FastAPI)
- **Banco de Dados:** MySQL 8
- **ORM:** SQLAlchemy
- **Containerização:** Docker e Docker Compose

Comunicação via API REST utilizando JSON.

---

## 🗄️ Modelagem do Banco de Dados

### Entidades principais

- **Usuario**
- **Sala**
- **Agendamento**
- **Reserva**

Relacionamentos com chaves primárias e estrangeiras,
garantindo integridade referencial.

📌 O esquema lógico foi obtido a partir da transformação do MERE
para o modelo relacional.

---

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


*(demais tabelas descritas nos scripts SQL)*

---

## 🧪 Normalização

O esquema está normalizado até **no mínimo a Segunda Forma Normal (2FN)**,
eliminando dependências parciais e redundâncias.

---

## 🐳 Como executar o projeto (Docker)

### 1️⃣ Subir o banco de dados
```bash
docker compose up -d