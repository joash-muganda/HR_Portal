-- This file starts the database
CREATE DATABASE IF NOT EXISTS hr_db;
CREATE USER IF NOT EXISTS 'hr_system'@'%' IDENTIFIED BY 'team_late';
CREATE USER IF NOT EXISTS 'hr_system'@'localhost' IDENTIFIED BY 'team_late';
FLUSH PRIVILEGES;
GRANT ALL ON hr_db.* to 'hr_system'@'localhost';
GRANT ALL ON hr_db.* to 'hr_system'@'%';
FLUSH PRIVILEGES;
