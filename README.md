# Sistema de Agendamento - Laboratorio de Anatomia (LAPA)

Sistema web para gerenciamento de salas, agendamentos e relatorios do Laboratorio de Anatomia.

## Integrantes do grupo

- Daniela Oliveira

## Objetivo

Centralizar o uso das salas do laboratorio com:

- cadastro de usuarios
- cadastro de salas
- criacao e cancelamento de agendamentos
- reserva automatica vinculada ao agendamento
- consulta de disponibilidade
- relatorios baseados em views SQL

## Stack

- Frontend: HTML, CSS e JavaScript (sem framework)
- Backend: FastAPI (Python 3.11)
- Banco: MySQL 8
- Orquestracao: Docker Compose

## Portas da aplicacao

- Frontend: `3000` (Nginx no container, acesso em `http://localhost:3000`)
- Backend API: `8000` (acesso em `http://localhost:8000`)
- Swagger: `http://localhost:8000/docs`
- MySQL: `3307` no host mapeado para `3306` no container

## Arquitetura do projeto

- `frontend_lab_anatomia`: interface web (`index.html` e `relatorios.html`)
- `backend_lab_anatomia`: API REST e regras de negocio
- `sql`: scripts de DDL, DML e trigger

## Como rodar o projeto (Docker)

### Requisitos

- Docker
- Docker-compose

### Passo a passo

```bash
git clone https://github.com/danisjc6/agendamento_LAPA
cd agendamento_LAPA
docker compose up --build
```

### Subir em background

```bash
docker compose up -d --build
```

### Parar os containers

```bash
docker compose down
```

### Rebuild apos alteracoes de codigo

Como as imagens fazem `COPY` do codigo, para refletir alteracoes:

```bash
docker compose up -d --build frontend backend
```

## Funcionalidades implementadas

### Agendamentos

- cria agendamento e reserva em uma unica operacao (`POST /agendamentos/`)
- bloqueia sobreposicao de horarios na mesma sala
- permite cancelamento (`PUT /agendamentos/{id_agendamento}/cancelar`)
- atualiza status para `finalizado` quando horario ja passou (na listagem)
- tela inicial com atualizacao automatica da lista de agendamentos

### Disponibilidade de salas

- endpoint de disponibilidade por sala/data:
  `GET /salas/{id_sala}/disponibilidade?data=YYYY-MM-DD`
- retorno atual: blocos livres de 1h entre 08:00 e 18:00

### Relatorios com views

Na pagina `relatorios.html`, o frontend consome dinamicamente:

- `vw_agendamentos_detalhados`
- `vw_salas_mais_utilizadas`
- `vw_agendamentos_ativos`
- `vw_ocupacao_salas_por_data`
- `vw_salas_livres`

Com exportacao CSV por view selecionada.

## Endpoints principais

### Usuarios (`/usuarios`)

- `POST /usuarios/`
- `GET /usuarios/`
- `GET /usuarios/{matricula}`
- `PUT /usuarios/{matricula}`
- `DELETE /usuarios/{matricula}`

### Salas (`/salas`)

- `GET /salas/`
- `GET /salas/{id_sala}/disponibilidade?data=YYYY-MM-DD`

### Agendamentos (`/agendamentos`)

- `POST /agendamentos/`
- `GET /agendamentos/`
- `PUT /agendamentos/{id_agendamento}/cancelar`

### Reservas (`/reservas`)

- `GET /reservas/`
- `POST /reservas/`

### Relatorios (`/relatorios`)

- `GET /relatorios/views`
- `GET /relatorios/views/{view_nome}`
- `GET /relatorios/views/{view_nome}/csv`

Endpoints legados mantidos:

- `GET /relatorios/agendamentos`
- `GET /relatorios/agendamentos/csv`

## Esquema conceitual do BD (atualizado)

- Modelo conceitual (Lucidchart):
  `https://lucid.app/lucidchart/d1fea927-13ae-4bd2-8b85-e5af8d780775/edit?viewport_loc=-3139%2C-3565%2C2524%2C1340%2C0_0&invitationId=inv_faef2763-0318-4fc4-9ea4-3443acf20d06`
- Diagrama ER no repositorio: `image.png`

Entidades principais:

- Usuario
- Sala
- Agendamento
- Reserva

Relacionamentos:

- um usuario pode ter varios agendamentos
- um agendamento pertence a um usuario
- um agendamento gera uma reserva
- uma sala pode ter varias reservas

## Dicionario de dados

### Tabela `usuarios`

| Campo     | Tipo         | Restricoes | Descricao                |
|-----------|--------------|------------|--------------------------|
| matricula | INT          | PK         | Identificador do usuario |
| nome      | VARCHAR(100) | NOT NULL   | Nome do usuario          |
| email     | VARCHAR(100) | UNIQUE     | Email                    |
| telefone  | VARCHAR(20)  |            | Contato                  |
| curso     | VARCHAR(100) |            | Curso do usuario         |

### Tabela `salas`

| Campo      | Tipo         | Restricoes | Descricao             |
|------------|--------------|------------|-----------------------|
| id_sala    | INT          | PK, AI     | Identificador da sala |
| nome_sala  | VARCHAR(100) | NOT NULL   | Nome da sala          |
| tipo       | VARCHAR(50)  |            | Tipo da sala          |
| capacidade | INT          | CHECK > 0  | Capacidade maxima     |

### Tabela `agendamentos`

| Campo          | Tipo         | Restricoes                    | Descricao                    |
|----------------|--------------|-------------------------------|------------------------------|
| id_agendamento | INT          | PK, AI                        | Identificador do agendamento |
| matricula      | INT          | FK -> usuarios.matricula      | Usuario que agendou          |
| data           | DATE         | NOT NULL                      | Data do agendamento          |
| hora_inicio    | TIME         | NOT NULL                      | Horario de inicio            |
| hora_fim       | TIME         | NOT NULL                      | Horario de fim               |
| finalidade     | VARCHAR(255) |                               | Finalidade                   |
| status         | VARCHAR(20)  | DEFAULT 'ativo'               | ativo/cancelado/finalizado   |

### Tabela `reservas`

| Campo          | Tipo | Restricoes                         | Descricao                         |
|----------------|------|------------------------------------|-----------------------------------|
| id_reserva     | INT  | PK, AI                             | Identificador da reserva          |
| id_agendamento | INT  | FK -> agendamentos.id_agendamento  | Agendamento associado             |
| id_sala        | INT  | FK -> salas.id_sala                | Sala reservada                    |
| (id_ag,id_sala)|      | UNIQUE                             | Impede duplicidade da mesma dupla |

### Views SQL

- `vw_agendamentos_detalhados`
- `vw_salas_mais_utilizadas`
- `vw_agendamentos_ativos`
- `vw_ocupacao_salas_por_data`
- `vw_salas_livres`

Script de criacao: `sql/ddl.sql`

## Documentacao do trigger

- Arquivo: `sql/triggers/trigger_agendamento_passado.sql`
- Nome: `validar_agendamento_passado`
- Tipo: `BEFORE INSERT ON agendamentos`

### Regra de negocio automatizada

O trigger impede que seja criado:

- agendamento com `data` anterior a data atual
- agendamento para hoje com `hora_inicio` anterior ao horario atual

Quando a regra e violada, o banco retorna erro com `SQLSTATE '45000'`.

### Como testar o trigger

1. Suba o projeto com Docker.
2. Acesse o MySQL no container:

```bash
docker compose exec mysql mysql -u root -proot laboratorio_anatomia
```

3. Tente inserir um agendamento em data passada:

```sql
INSERT INTO agendamentos (matricula, data, hora_inicio, hora_fim, finalidade, status)
VALUES (1001, '2020-01-01', '08:00:00', '09:00:00', 'Teste trigger', 'ativo');
```

4. Resultado esperado: erro com mensagem de bloqueio de data passada.

## Como os dados do banco foram povoados

- Estrutura: `sql/ddl.sql` (tabelas e views)
- Dados iniciais: `sql/dml.sql` (usuarios, salas, agendamentos e reservas)
- Trigger: `sql/triggers/trigger_agendamento_passado.sql`

No `docker-compose.yml`, a pasta `./sql` e montada em `/docker-entrypoint-initdb.d`, entao a inicializacao do MySQL executa os scripts automaticamente no primeiro start do volume.

## Correções realizadas nesta versão (vs. versão passada)

- corrigido erro no frontend ao criar agendamento (`a is not defined`)
- removida duplicidade de criacao de reserva no frontend (backend ja cria reserva junto com agendamento)
- corrigido erro de disponibilidade quando tabela de horarios nao existe no DOM
- ajustada interpretacao de disponibilidade no frontend (endpoint retorna blocos livres)
- adicionado refresh automatico de agendamentos na tela principal
- relatorio ordenado por data mais recente para mais antiga
- frontend de relatorios atualizado para consumir as views SQL dinamicamente
- destacar a sala selecionada durante o preenchimento do formulário
- limitar horários de agendamento para o intervalo entre 8:00 e 18:00.

