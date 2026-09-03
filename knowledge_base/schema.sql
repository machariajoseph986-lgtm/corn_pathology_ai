-- ============================================================
-- CORN PATHOLOGY AI
-- PLANT HEALTH KNOWLEDGE BASE
-- DATABASE SCHEMA
-- ============================================================

-- Enable foreign-key enforcement in SQLite
PRAGMA foreign_keys = ON;


-- ============================================================
-- 1. PLANTS
-- ============================================================
-- Stores the major crops covered by the knowledge base.

CREATE TABLE IF NOT EXISTS plants (
    plant_id TEXT PRIMARY KEY,
    common_name TEXT NOT NULL UNIQUE,
    genus TEXT,
    family TEXT
);


-- ============================================================
-- 2. SPECIES
-- ============================================================
-- A crop may have one or more scientific species.
-- Example:
-- Coffee -> Coffea arabica
-- Coffee -> Coffea canephora

CREATE TABLE IF NOT EXISTS species (
    species_id TEXT PRIMARY KEY,
    plant_id TEXT NOT NULL,
    scientific_name TEXT NOT NULL,
    common_name TEXT,

    FOREIGN KEY (plant_id)
        REFERENCES plants(plant_id)
        ON DELETE CASCADE,

    UNIQUE (plant_id, scientific_name)
);


-- ============================================================
-- 3. HEALTH PROBLEMS
-- ============================================================
-- Central table for diseases and other plant-health problems.

CREATE TABLE IF NOT EXISTS health_problems (
    health_problem_id TEXT PRIMARY KEY,
    plant_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,

    FOREIGN KEY (plant_id)
        REFERENCES plants(plant_id)
        ON DELETE CASCADE,

    UNIQUE (plant_id, name)
);


-- ============================================================
-- 4. PATHOGENS
-- ============================================================
-- Stores organisms/agents responsible for a health problem.
--
-- A health problem can have multiple pathogens.
-- This is important for diseases such as
-- Maize Lethal Necrosis.

CREATE TABLE IF NOT EXISTS pathogens (
    pathogen_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    scientific_name TEXT NOT NULL,
    type TEXT NOT NULL,
    role TEXT,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 5. SYMPTOMS
-- ============================================================
-- Stores observable symptoms associated with a health problem.

CREATE TABLE IF NOT EXISTS symptoms (
    symptom_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    category TEXT,
    description TEXT NOT NULL,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 6. TRANSMISSION
-- ============================================================
-- Describes how the disease/health problem spreads.

CREATE TABLE IF NOT EXISTS transmission (
    transmission_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    method TEXT NOT NULL,
    description TEXT,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 7. CONDITIONS
-- ============================================================
-- Stores environmental or management conditions that may
-- favor disease development or spread.

CREATE TABLE IF NOT EXISTS conditions (
    condition_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    factor TEXT NOT NULL,
    value TEXT,
    description TEXT,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 8. MANAGEMENT
-- ============================================================
-- Stores prevention, control and management recommendations.

CREATE TABLE IF NOT EXISTS management (
    management_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    category TEXT NOT NULL,
    action TEXT NOT NULL,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 9. SOURCES
-- ============================================================
-- Stores the sources used to support information in the
-- knowledge base.

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    health_problem_id TEXT NOT NULL,
    organization TEXT,
    title TEXT,
    url TEXT NOT NULL,
    accessed_date TEXT,

    FOREIGN KEY (health_problem_id)
        REFERENCES health_problems(health_problem_id)
        ON DELETE CASCADE
);


-- ============================================================
-- INDEXES
-- ============================================================
-- These improve query performance when the chatbot searches
-- the knowledge base.

CREATE INDEX IF NOT EXISTS idx_species_plant
    ON species(plant_id);

CREATE INDEX IF NOT EXISTS idx_health_problems_plant
    ON health_problems(plant_id);

CREATE INDEX IF NOT EXISTS idx_pathogens_health_problem
    ON pathogens(health_problem_id);

CREATE INDEX IF NOT EXISTS idx_symptoms_health_problem
    ON symptoms(health_problem_id);

CREATE INDEX IF NOT EXISTS idx_transmission_health_problem
    ON transmission(health_problem_id);

CREATE INDEX IF NOT EXISTS idx_conditions_health_problem
    ON conditions(health_problem_id);

CREATE INDEX IF NOT EXISTS idx_management_health_problem
    ON management(health_problem_id);

CREATE INDEX IF NOT EXISTS idx_sources_health_problem
    ON sources(health_problem_id);


-- ============================================================
-- SCHEMA COMPLETE
-- ============================================================