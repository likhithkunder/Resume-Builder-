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


DELIMITER //
CREATE TRIGGER before_education_insert
BEFORE INSERT ON education
FOR EACH ROW
BEGIN
    SET NEW.ed_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_skills_insert
BEFORE INSERT ON skills
FOR EACH ROW
BEGIN
    SET NEW.skill_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_projects_insert
BEFORE INSERT ON projects
FOR EACH ROW
BEGIN
    SET NEW.project_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END //

DELIMITER ;


DELIMITER //
CREATE TRIGGER before_certificates_insert
BEFORE INSERT ON certificates
FOR EACH ROW
BEGIN
    SET NEW.c_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END //

DELIMITER ;


DELIMITER //
CREATE TRIGGER before_experience_insert
BEFORE INSERT ON works_exp
FOR EACH ROW
BEGIN
    SET NEW.exp_id = SUBSTRING(MD5(CONCAT(NOW(), RAND())), 1, 5);
END //

DELIMITER ;
