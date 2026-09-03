import sqlite3
import json
from pathlib import Path


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "plant_health.db"


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():
    """
    Create and return a connection to the plant health database.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign-key enforcement for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    # Return rows that can be accessed by column name.
    connection.row_factory = sqlite3.Row

    return connection


# ---------------------------------------------------------
# DISEASE PROFILE
# ---------------------------------------------------------

def get_disease_profile(health_problem_id):
    """
    Retrieve the complete profile of a disease.

    Parameters
    ----------
    health_problem_id : str
        The unique ID of the disease.

    Returns
    -------
    dict or None
        Complete disease profile, or None if the disease
        does not exist.
    """

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type,
        hp.description,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'scientific_name', pa.scientific_name,
                        'type', pa.type,
                        'role', pa.role
                    )
                )
                FROM pathogens pa
                WHERE pa.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS pathogens,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'category', s.category,
                        'description', s.description
                    )
                )
                FROM symptoms s
                WHERE s.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS symptoms,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'method', t.method,
                        'description', t.description
                    )
                )
                FROM transmission t
                WHERE t.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS transmission,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'factor', c.factor,
                        'value', c.value,
                        'description', c.description
                    )
                )
                FROM conditions c
                WHERE c.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS conditions,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'category', m.category,
                        'action', m.action
                    )
                )
                FROM management m
                WHERE m.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS management,

        COALESCE(
            (
                SELECT json_group_array(
                    json_object(
                        'organization', so.organization,
                        'title', so.title,
                        'url', so.url
                    )
                )
                FROM sources so
                WHERE so.health_problem_id = hp.health_problem_id
            ),
            '[]'
        ) AS sources

    FROM health_problems hp

    JOIN plants p
        ON hp.plant_id = p.plant_id

    WHERE hp.health_problem_id = ?
    """

    with get_connection() as connection:

        row = connection.execute(
            query,
            (health_problem_id,)
        ).fetchone()

    if row is None:
        return None

    profile = dict(row)

    # Convert JSON strings into Python objects.
    json_fields = [
        "pathogens",
        "symptoms",
        "transmission",
        "conditions",
        "management",
        "sources"
    ]

    for field in json_fields:
        profile[field] = json.loads(profile[field])

    return profile

# ---------------------------------------------------------
# GET ALL DISEASES
# ---------------------------------------------------------

def get_all_diseases():
    """
    Retrieve all diseases currently stored in the knowledge base.

    Returns
    -------
    list of dict
        Disease ID, disease name, crop, and disease type.
    """

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type
    FROM health_problems hp
    JOIN plants p
        ON hp.plant_id = p.plant_id
    ORDER BY p.common_name, hp.name;
    """

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]


# ---------------------------------------------------------
# FIND DISEASE
# ---------------------------------------------------------

def find_disease(search_term):
    """
    Search for diseases using disease name, crop name,
    or known disease abbreviations.
    """

    search_term = search_term.strip().lower()

    # Known disease aliases.
    aliases = {
        "mln": "maize lethal necrosis",
    }

    search_term = aliases.get(search_term, search_term)

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type
    FROM health_problems hp
    JOIN plants p
        ON hp.plant_id = p.plant_id
    WHERE
        LOWER(hp.name) LIKE ?
        OR LOWER(p.common_name) LIKE ?
    ORDER BY hp.name;
    """

    pattern = f"%{search_term}%"

    with get_connection() as connection:
        rows = connection.execute(
            query,
            (pattern, pattern)
        ).fetchall()

    return [dict(row) for row in rows]


# ---------------------------------------------------------
# SIMPLE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("PLANT HEALTH KNOWLEDGE BASE TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # TEST 1: ALL DISEASES
    # -----------------------------------------------------

    print("\nAVAILABLE DISEASES")
    print("-" * 60)

    diseases = get_all_diseases()

    for disease in diseases:
        print(
            f"{disease['crop']:10} | "
            f"{disease['disease']:25} | "
            f"{disease['type']}"
        )

    # -----------------------------------------------------
    # TEST 2: SEARCH
    # -----------------------------------------------------

    print("\nSEARCH TEST: maize")
    print("-" * 60)

    matches = find_disease("maize")

    for match in matches:
        print(
            f"ID: {match['health_problem_id']} | "
            f"Disease: {match['disease']} | "
            f"Crop: {match['crop']}"
        )

    # -----------------------------------------------------
    # TEST 3: COMPLETE PROFILE
    # -----------------------------------------------------

    print("\nCOMPLETE PROFILE TEST")
    print("-" * 60)

    disease_id = "HP_MAIZE_MLN"

    profile = get_disease_profile(disease_id)

    if profile is None:

        print("Disease not found.")

    else:

        print(f"Disease      : {profile['disease']}")
        print(f"Crop         : {profile['crop']}")
        print(f"Type         : {profile['type']}")
        print(f"Pathogens    : {len(profile['pathogens'])}")
        print(f"Symptoms     : {len(profile['symptoms'])}")
        print(f"Transmission : {len(profile['transmission'])}")
        print(f"Conditions   : {len(profile['conditions'])}")
        print(f"Management   : {len(profile['management'])}")
        print(f"Sources      : {len(profile['sources'])}")

    print("\n" + "=" * 60)
    print("DATABASE LAYER TEST COMPLETE")
    print("=" * 60)