-- Table for characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    alias VARCHAR(255)[],
    Mut INT,               -- MU
    Klugheit INT,          -- KL
    Intuition INT,         -- IN
    Charisma INT,          -- CH
    Fingerfertigkeit INT,  -- FF
    Gewandtheit INT,       -- GE
    Konstitution INT,      -- KO
    Körperkraft INT        -- KK
);


-- Table for trait rolls
CREATE TABLE traits_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    category VARCHAR(255),
    talent VARCHAR(255),
    trait VARCHAR(255),
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT
);

-- Table for talent rolls
CREATE TABLE talents_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    category VARCHAR(255),
    talent VARCHAR(255),
    trait1 VARCHAR(255),
    trait2 VARCHAR(255),
    trait3 VARCHAR(255),
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT,
    trait_value1 INT,
    trait_value2 INT,
    trait_value3 INT
);

-- Table for spell rolls
CREATE TABLE spells_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    category VARCHAR(255),
    spell VARCHAR(255),
    trait1 VARCHAR(255),
    trait2 VARCHAR(255),
    trait3 VARCHAR(255),
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT,
    trait_value1 INT,
    trait_value2 INT,
    trait_value3 INT
);

-- Table for attack rolls
CREATE TABLE attacks_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    category VARCHAR(255),
    attack VARCHAR(255),
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT
);

-- Table for initiative rolls
CREATE TABLE initiative_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    current_ini INT,
    rolled_ini INT,
    modifier INT
);

-- Table for tracking total damage
CREATE TABLE total_damage (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id),
    total_damage INT
);

-- Insert some characters
INSERT INTO characters (name, alias, Mut, Klugheit, Intuition, Charisma, Fingerfertigkeit, Gewandtheit, Konstitution, Körperkraft) VALUES 
('Akira Masamune', '{}', 15, 14, 17, 13, 13, 14, 15, 18),
('Hanzo Shimada', '{}', 12, 14, 15, 11, 12, 16, 12, 12),
('Elanor Walham', '{"Niko K."}', 11, 12, 15, 13, 12, 16, 13, 12),
('Bargaan Treuwall', '{"Yannik F."}', 15, 14, 16, 11, 16, 13, 16, 18),
('Walpurga Hausmännin', '{"Luisa B.", "Walpurga Hausmännin (Walla Burija Sabu Hasmanin)"}', 14, 10, 15, 15, 11, 11, 13, 10),
('Kurtek', '{}', 14, 10, 15, 13, 8, 14, 13, 15),
('Torgan Rehernagrot', '{}', 14, 13, 13, 13, 12, 15, 11, 10),
('Playboy51', '{}', 12, 13, 16, 14, 12, 16, 13, 12);
