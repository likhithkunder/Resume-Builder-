DELIMITER //
CREATE PROCEDURE validate_id(IN table_name VARCHAR(255), IN table_name_id_column VARCHAR(255), IN id VARCHAR(255), OUT is_valid BOOLEAN)
BEGIN
    DECLARE count_result INT;

    SET @query = CONCAT('SELECT COUNT(*) INTO @count_result FROM ', table_name, ' WHERE ', table_name_id_column, ' = "', id, '"');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET is_valid = (@count_result > 0);
END //
DELIMITER ;



DELIMITER //
CREATE TRIGGER before_user_insert
BEFORE INSERT ON user
FOR EACH ROW
BEGIN
    SET NEW.user_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END;
//
DELIMITER ;
