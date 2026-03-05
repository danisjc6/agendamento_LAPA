DROP TRIGGER IF EXISTS validar_agendamento_passado;

DELIMITER $$

CREATE TRIGGER validar_agendamento_passado
BEFORE INSERT ON agendamentos
FOR EACH ROW
BEGIN

    IF NEW.data < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é permitido criar agendamento em data passada.';
    END IF;

    IF NEW.data = CURDATE() AND NEW.hora_inicio < CURTIME() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é permitido criar agendamento em horário passado.';
    END IF;

END$$

DELIMITER ;