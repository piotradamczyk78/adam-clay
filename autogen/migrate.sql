-- =============================================
-- AUTOCOMPLETE MIGRATION SCRIPT FOR MySQL
-- =============================================

-- 1. CREATE DATABASE WITH PROPER ENCODING
CREATE DATABASE IF NOT EXISTS adam_clay_autogen 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. CREATE DEDICATED USER
CREATE USER IF NOT EXISTS 'autogen_user'@'localhost'
IDENTIFIED BY 'AutoGenSecure123!';

-- 3. GRANT PRIVILEGES
GRANT ALL PRIVILEGES ON adam_clay_autogen.* 
TO 'autogen_user'@'localhost';

-- 4. CREATE TABLES (ADAPTED FROM SQLAlchemy MODELS)
USE adam_clay_autogen;

CREATE TABLE IF NOT EXISTS subconscious_agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    temperature FLOAT DEFAULT 0.7,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS agent_conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agent_id INT NOT NULL,
    conversation_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) 
    REFERENCES subconscious_agents(id) 
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. ADD SAMPLE DATA (OPTIONAL)
INSERT IGNORE INTO subconscious_agents 
(name, agent_type, temperature) 
VALUES 
('Analytical', 'ANALYTICAL', 0.3),
('Creative', 'CREATIVE', 0.9);

-- 6. FINAL CONFIGURATION
FLUSH PRIVILEGES;
