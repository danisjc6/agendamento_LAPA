INSERT INTO usuarios VALUES
(1001, 'Ana Silva', 'ana@ufape.edu.br', '9999-1111', 'Medicina Veterinária'),
(1002, 'João Lima', 'joao@ufape.edu.br', '9999-2222', 'Zootecnia');

INSERT INTO salas (id_sala, nome_sala, tipo, capacidade) VALUES
(1, 'Sala de Aula', 'laboratório', 40),
(2, 'Sala de Preparo de Peças', 'laboratório', 40),
(3, 'Auditório LAPA', 'auditório', 60),
(4, 'Sala de reuniões', 'auditório', 20);

INSERT INTO agendamentos (id_agendamento, matricula, data, hora_inicio, hora_fim, finalidade, status)
VALUES
(1, 1001, '2026-03-10', '08:00', '10:00', 'Aula prática', 'ativo'),
(2, 1001, '2026-03-12', '14:00', '16:00', 'Reunião de grupo', 'cancelado'),
(3, 1002, '2026-03-11', '09:00', '11:00', 'Estudo de caso', 'ativo');

INSERT INTO reservas (id_reserva, id_agendamento, id_sala) VALUES 
(1, 1, 1),
(2, 2, 4),
(3, 3, 2);  