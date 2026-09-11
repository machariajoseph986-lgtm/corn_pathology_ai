# PURPOSE: Migrate the existing Plant Health SQLite knowledge base into PostgreSQL.
# EXPECTED OUTPUT: The same records are copied from plant_health.db into PostgreSQL plant_health.

import os
import sqlite3
import psycopg


# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

SQLITE_DATABASE = "knowledge_base/plant_health.db"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "plant_health"
POSTGRES_USER = "postgres"


def get_postgresql_connection():
    """
    Create a connection to the PostgreSQL project database.

    The password is read from the POSTGRES_PASSWORD
    environment variable rather than being stored in code.
    """

    password = os.getenv("POSTGRES_PASSWORD")

    if not password:
        raise RuntimeError(
            "POSTGRES_PASSWORD environment variable is not set."
        )

    return psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=password
    )


def get_sqlite_connection():
    """
    Connect to the existing SQLite knowledge base.
    """

    connection = sqlite3.connect(SQLITE_DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def migrate_table(
    sqlite_connection,
    postgres_connection,
    table_name,
    columns
):
    """
    Copy all records from one SQLite table into
    the corresponding PostgreSQL table.
    """

    column_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    select_query = f"""
        SELECT {column_list}
        FROM {table_name}
    """

    insert_query = f"""
        INSERT INTO {table_name} ({column_list})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    sqlite_rows = sqlite_connection.execute(
        select_query
    ).fetchall()

    with postgres_connection.cursor() as cursor:

        for row in sqlite_rows:

            values = tuple(
                row[column]
                for column in columns
            )

            cursor.execute(
                insert_query,
                values
            )

    print(
        f"{table_name:<20} "
        f"{len(sqlite_rows):>5} records processed"
    )


def main():

    print("SQLITE → POSTGRESQL MIGRATION")
    print("=" * 60)

    sqlite_connection = get_sqlite_connection()
    postgres_connection = get_postgresql_connection()

    try:

        # Parent tables must be migrated before
        # tables containing foreign keys.
        tables = {

            "plants": [
                "plant_id",
                "common_name",
                "genus",
                "family"
            ],

            "species": [
                "species_id",
                "plant_id",
                "scientific_name",
                "common_name"
            ],

            "health_problems": [
                "health_problem_id",
                "plant_id",
                "name",
                "type",
                "description"
            ],

            "pathogens": [
                "pathogen_id",
                "health_problem_id",
                "scientific_name",
                "type",
                "role"
            ],

            "symptoms": [
                "symptom_id",
                "health_problem_id",
                "category",
                "description"
            ],

            "transmission": [
                "transmission_id",
                "health_problem_id",
                "method",
                "description"
            ],

            "conditions": [
                "condition_id",
                "health_problem_id",
                "factor",
                "value",
                "description"
            ],

            "management": [
                "management_id",
                "health_problem_id",
                "category",
                "action"
            ],

            "sources": [
                "source_id",
                "health_problem_id",
                "organization",
                "title",
                "url",
                "accessed_date"
            ]
        }

        for table_name, columns in tables.items():

            migrate_table(
                sqlite_connection,
                postgres_connection,
                table_name,
                columns
            )

        postgres_connection.commit()

        print("=" * 60)
        print("Migration completed successfully.")

    except Exception:

        postgres_connection.rollback()
        raise

    finally:

        sqlite_connection.close()
        postgres_connection.close()


if __name__ == "__main__":
    main()