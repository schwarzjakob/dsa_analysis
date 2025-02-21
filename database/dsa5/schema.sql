-- Create the DSA5 schema
CREATE SCHEMA IF NOT EXISTS dsa5;

-- Table for DSA5 Characters
CREATE TABLE IF NOT EXISTS dsa5.actors (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    mut INT,
    klugheit INT,
    intuition INT, -- renamed from "in" to avoid conflict with reserved words
    charisma INT,
    fingerfertigkeit INT,
    gewandtheit INT,
    konstitution INT,
    köperkraft INT,
    life_points_value INT,
    life_points_max INT,
    astral_energy_value INT,
    astral_energy_max INT,
    initiative NUMERIC,
    species VARCHAR(255),
    culture VARCHAR(255),
    career VARCHAR(255),
    experience_total INT,
    experience_spent INT
);

-- Table for DSA5 Talent Rolls
CREATE TABLE IF NOT EXISTS dsa5.talent_rolls (
    message_id VARCHAR(50) PRIMARY KEY,
    timestamp BIGINT,
    talent_name VARCHAR(255),
    talent_group VARCHAR(255),
    talent_value INT,
    talent_trait_1 VARCHAR(50),
    talent_trait_2 VARCHAR(50),
    talent_trait_3 VARCHAR(50),
    modifier INT,
    actor VARCHAR(50) REFERENCES dsa5.actors (id) ON DELETE CASCADE,
    result INT,
    quality_step INT,
    description TEXT,
    success_level INT,
    roll_type VARCHAR(50)
);
