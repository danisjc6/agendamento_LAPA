DELIMITER $$

CREATE TRIGGER validar_agendamento_passado
BEFORE INSERT ON agendamentos
FOR EACH ROW
BEGIN
    IF TIMESTAMP(NEW.data, NEW.hora_inicio) < NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é permitido criar agendamento no passado.';
    END IF;
END$$

DELIMITER ;