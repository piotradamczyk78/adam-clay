-- Wykonaj te komendy w MySQL jako root:
-- mysql -u root -p

CREATE DATABASE IF NOT EXISTS adam_clay_autogen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'autogen_godmode'@'localhost' IDENTIFIED BY '1voNPq3vTeLsvlog';
GRANT ALL PRIVILEGES ON adam_clay_autogen.* TO 'autogen_godmode'@'localhost';
FLUSH PRIVILEGES;

-- Sprawdź czy działa:
-- SELECT User, Host FROM mysql.user WHERE User = 'autogen_godmode';
-- SHOW DATABASES LIKE 'adam_clay_autogen';
