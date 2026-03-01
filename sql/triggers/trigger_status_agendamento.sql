DELIMITER //

CREATE TRIGGER before_insert_agendamento
BEFORE INSERT ON agendamento
FOR EACH ROW
BEGIN
    IF TIMESTAMP(NEW.data, NEW.hora) < NOW() THEN
        SET NEW.status = 'finalizado';
    ELSE
        SET NEW.status = 'ativo';
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_update_agendamento
BEFORE UPDATE ON agendamento
FOR EACH ROW
BEGIN
    IF TIMESTAMP(NEW.data, NEW.hora) < NOW() THEN
        SET NEW.status = 'finalizado';
    END IF;
END;
//

DELIMITER ;