-- Table for characters
CREATE TABLE IF NOT EXISTS characters (
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
CREATE TABLE IF NOT EXISTS traits_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    trait_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT
);

-- Table for talent rolls
CREATE TABLE IF NOT EXISTS talents_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    talent_id INT REFERENCES talents(talent_id) ON DELETE CASCADE,
    trait_one_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    trait_two_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    trait_three_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT,
    trait_value1 INT,
    trait_value2 INT,
    trait_value3 INT
);

-- Table for spell rolls
CREATE TABLE IF NOT EXISTS spells_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
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
CREATE TABLE IF NOT EXISTS attacks_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    attack_id INT REFERENCES attacks(attack_id) ON DELETE CASCADE,
    modifier INT,
    success BOOLEAN,
    tap_zfp INT,
    taw_zfw INT
);

-- Table for initiative rolls
CREATE TABLE IF NOT EXISTS initiative_rolls (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    current_ini INT,
    rolled_ini INT,
    modifier INT
);

-- Table for tracking total damage
CREATE TABLE IF NOT EXISTS total_damage (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    total_damage INT
);

-- Table for character traits
CREATE TABLE IF NOT EXISTS character_traits (
    trait_id SERIAL PRIMARY KEY,
    trait_name VARCHAR(255) UNIQUE NOT NULL,
    trait_abbreviation CHAR(2) UNIQUE NOT NULL
);

-- Table for talent_categories
CREATE TABLE IF NOT EXISTS talent_categories (
    talent_category_id SERIAL PRIMARY KEY,
    talent_category_name VARCHAR(255) UNIQUE NOT NULL
);

-- Table for talents
CREATE TABLE IF NOT EXISTS talents (
    talent_id SERIAL PRIMARY KEY,
    talent_name VARCHAR(255) UNIQUE NOT NULL,
    talent_category_id INT REFERENCES talent_categories(talent_category_id) ON DELETE CASCADE,
    talent_trait_one_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    talent_trait_two_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    talent_trait_three_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE
);

-- Table for spells
CREATE TABLE IF NOT EXISTS spells (
    spell_id SERIAL PRIMARY KEY,
    spell_name VARCHAR(255) UNIQUE NOT NULL,
    spell_trait_one_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    spell_trait_two_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    spell_trait_three_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE
);

-- Table for attack_categories
CREATE TABLE IF NOT EXISTS attack_categories (
    attack_category_id SERIAL PRIMARY KEY,
    attack_category_name VARCHAR(255) UNIQUE NOT NULL
);

-- Table for attacks
CREATE TABLE IF NOT EXISTS attacks (
    attack_id SERIAL PRIMARY KEY,
    attack_name VARCHAR(255) UNIQUE NOT NULL,
    attack_category_id INT REFERENCES attack_categories(attack_category_id) ON DELETE CASCADE,
    attack_trait_one_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    attack_trait_two_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE,
    attack_trait_three_id INT REFERENCES character_traits(trait_id) ON DELETE CASCADE
);

