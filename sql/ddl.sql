CREATE DATABASE IF NOT EXISTS laboratorio_anatomia;
USE laboratorio_anatomia;

CREATE TABLE usuarios (
    matricula INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    curso VARCHAR(100)
);

CREATE TABLE salas (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nome_sala VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    capacidade INT CHECK (capacidade > 0)
);

CREATE TABLE agendamentos (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    matricula INT NOT NULL,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    finalidade VARCHAR(255),
    status VARCHAR(20) DEFAULT 'ativo',
    CONSTRAINT fk_usuario
      FOREIGN KEY (matricula) REFERENCES usuarios(matricula)

);

CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_agendamento INT NOT NULL,
    id_sala INT NOT NULL,
    CONSTRAINT fk_agendamento
      FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento),
    CONSTRAINT fk_sala
      FOREIGN KEY (id_sala) REFERENCES salas(id_sala),
    CONSTRAINT uk_reserva UNIQUE (id_agendamento, id_sala)
);

CREATE VIEW vw_agendamentos_detalhados AS
SELECT
    a.id_agendamento,
    u.nome AS nome_usuario,
    u.email,
    s.nome_sala,
    s.tipo,
    s.capacidade,
    a.data,
    a.hora_inicio,
    a.hora_fim,
    a.finalidade,
    a.status
FROM agendamentos a
JOIN usuarios u 
    ON a.matricula = u.matricula
JOIN reservas r 
    ON a.id_agendamento = r.id_agendamento
JOIN salas s 
    ON r.id_sala = s.id_sala;


CREATE VIEW vw_salas_mais_utilizadas AS
SELECT
    s.nome_sala,
    COUNT(r.id_reserva) AS total_reservas
FROM salas s
LEFT JOIN reservas r ON s.id_sala = r.id_sala
GROUP BY s.nome_sala;


CREATE VIEW vw_agendamentos_ativos AS
SELECT *
FROM vw_agendamentos_detalhados
WHERE status = 'ativo';


CREATE OR REPLACE VIEW vw_ocupacao_salas_por_data AS
SELECT
    s.nome_sala AS sala,
    a.data,
    COUNT(r.id_reserva) AS total_agendamentos
FROM salas s
JOIN reservas r ON s.id_sala = r.id_sala
JOIN agendamentos a ON r.id_agendamento = a.id_agendamento
GROUP BY s.nome_sala, a.data;


CREATE OR REPLACE VIEW vw_salas_livres AS
SELECT
    s.id_sala,
    s.nome_sala,
    s.tipo,
    s.capacidade
FROM salas s
WHERE s.id_sala NOT IN (
    SELECT r.id_sala
    FROM reservas r
    JOIN agendamentos a ON r.id_agendamento = a.id_agendamento
    WHERE a.data = CURRENT_DATE()
);




