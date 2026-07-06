import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

DB_NAME = "database/resumes.db"


# ---------------------------------------
# Database Connection
# ---------------------------------------
def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------------------------------
# Create Candidates Table
# ---------------------------------------
def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT UNIQUE,

        phone TEXT,

        skills TEXT,

        resume_path TEXT,

        resume_text TEXT

    )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------
# Save Candidate
# ---------------------------------------
def save_candidate(

    name,
    email,
    phone,
    skills,
    resume_path,
    resume_text

):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO candidates(

            name,
            email,
            phone,
            skills,
            resume_path,
            resume_text

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            name,
            email,
            phone,
            skills,
            resume_path,
            resume_text

        )

        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        # Duplicate Email
        return False

    finally:

        conn.close()


# ---------------------------------------
# Get All Candidates
# ---------------------------------------
def get_all_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            id,
            name,
            email,
            phone,
            skills,
            resume_path,
            resume_text

        FROM candidates

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ---------------------------------------
# Get Candidate By ID
# ---------------------------------------
def get_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM candidates WHERE id=?",

        (candidate_id,)

    )

    row = cursor.fetchone()

    conn.close()

    return row


# ---------------------------------------
# Delete Candidate
# ---------------------------------------
def delete_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    # Get Resume Path First
    cursor.execute(

        "SELECT resume_path FROM candidates WHERE id=?",

        (candidate_id,)

    )

    row = cursor.fetchone()

    if row:

        resume_path = row[0]

        # Delete Resume File
        if os.path.exists(resume_path):
            os.remove(resume_path)

    # Delete Database Record
    cursor.execute(

        "DELETE FROM candidates WHERE id=?",

        (candidate_id,)

    )

    conn.commit()

    conn.close()


# ---------------------------------------
# Total Candidates
# ---------------------------------------
def get_candidate_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM candidates"

    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ---------------------------------------
# Search Candidates
# ---------------------------------------
def search_candidates(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM candidates

        WHERE

            name LIKE ?

            OR email LIKE ?

            OR skills LIKE ?

    """,

    (

        f"%{keyword}%",

        f"%{keyword}%",

        f"%{keyword}%"

    )

    )

    rows = cursor.fetchall()

    conn.close()

    return rows