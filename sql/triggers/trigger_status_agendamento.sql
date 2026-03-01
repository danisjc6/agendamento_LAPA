DELIMITER $$

CREATE TRIGGER before_insert_agendamento
BEFORE INSERT ON agendamentos
FOR EACH ROW
BEGIN
    -- Se a data+hora do agendamento já passou, status = 'finalizado', senão 'ativo'
    IF TIMESTAMP(NEW.data, NEW.hora_inicio) < NOW() THEN
        SET NEW.status = 'finalizado';
    ELSE
        SET NEW.status = 'ativo';
    END IF;
END$$

CREATE TRIGGER before_update_agendamento
BEFORE UPDATE ON agendamentos
FOR EACH ROW
BEGIN
    -- Sempre verifica se o agendamento já passou, e ajusta status
    IF TIMESTAMP(NEW.data, NEW.hora_inicio) < NOW() THEN
        SET NEW.status = 'finalizado';
    ELSE
        SET NEW.status = 'ativo';
    END IF;
END$$

DELIMITER ;

SHOW GRANTS FOR CURRENT_USER();