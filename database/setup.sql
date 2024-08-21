-- Table for characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    alias VARCHAR(255)[]
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
