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
