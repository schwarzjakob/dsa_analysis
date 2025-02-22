-- Create the DSA5 schema
CREATE SCHEMA IF NOT EXISTS dsa5;

-- Traits Table
CREATE TABLE IF NOT EXISTS dsa5.traits (
    id serial PRIMARY KEY,
    trait_abbreviation VARCHAR(50),
    trait_name VARCHAR(255)
);

INSERT INTO
    dsa5.traits (trait_abbreviation, trait_name)
VALUES
    ('mu', 'Mut'),
    ('kl', 'Klugheit'),
    ('in', 'Intuition'),
    ('ch', 'Charisma'),
    ('ff', 'Fingerfertigkeit'),
    ('ge', 'Gewandtheit'),
    ('ko', 'Konstitution'),
    ('kk', 'Körperkraft');

-- Characters
CREATE TABLE IF NOT EXISTS dsa5.characters (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url TEXT,
    type VARCHAR(50),
    mut INT,
    klugheit INT,
    intuition INT,
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

-- Trait Rolls
CREATE TABLE IF NOT EXISTS dsa5.trait_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    trait_id INT REFERENCES dsa5.traits (id),
    trait_value INT,
    modifier INT,
    roll_result INT,
    success_level INT
);

-- Talent Rolls
CREATE TABLE IF NOT EXISTS dsa5.talent_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    talent_name VARCHAR(255),
    talent_group VARCHAR(255),
    talent_value INT,
    talent_trait_1_id INT REFERENCES dsa5.traits (id),
    talent_trait_2_id INT REFERENCES dsa5.traits (id),
    talent_trait_3_id INT REFERENCES dsa5.traits (id),
    modifier INT,
    result INT,
    quality_step INT,
    success_level INT,
    description TEXT
);

-- Spell Rolls
CREATE TABLE IF NOT EXISTS dsa5.spell_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    spell_name VARCHAR(255),
    spell_value INT,
    spell_trait_1_id INT REFERENCES dsa5.traits (id),
    spell_trait_2_id INT REFERENCES dsa5.traits (id),
    spell_trait_3_id INT REFERENCES dsa5.traits (id),
    modifier INT,
    result INT,
    quality_step INT,
    success_level INT,
    description TEXT
);

-- Attack Rolls
CREATE TABLE IF NOT EXISTS dsa5.attack_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    attack_name VARCHAR(255),
    attack_type VARCHAR(255),
    attack_value INT,
    modifier INT,
    roll_result INT,
    damage INT,
    description TEXT
);

-- Parry Rolls
CREATE TABLE IF NOT EXISTS dsa5.parry_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    parry_name VARCHAR(255),
    parry_type VARCHAR(255),
    parry_value INT,
    modifier INT,
    roll_result INT,
    description TEXT
);

-- Dodge Rolls
CREATE TABLE IF NOT EXISTS dsa5.dodge_rolls (
    event_id VARCHAR(50) PRIMARY KEY,
    character_id VARCHAR(50) REFERENCES dsa5.characters (id) ON DELETE CASCADE,
    timestamp BIGINT,
    dodge_value INT,
    modifier INT,
    roll_result INT,
    description TEXT
);