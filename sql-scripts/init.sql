-- This file starts the database
CREATE DATABASE hr_db;
CREATE USER 'hr_user'@'localhost' IDENTIFIED BY 'team_late';
FLUSH PRIVILEGES;
GRANT ALL ON hr_db.* to hr_user;
GRANT ALL ON hr_db.* to hr_user@localhost;
