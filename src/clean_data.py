import sqlite3

def main(): 
    conn = sqlite3.connect("data/maternal_health_risk.db")
    remove_invalid_heart_rate_entries(conn)
    add_pulse_pressure_column(conn)
    add_has_hypertension_column(conn)
    add_age_bracket_column(conn)
    verify_database(conn)
    close_connection(conn)


def remove_invalid_heart_rate_entries(conn):
    #delete irregular BPM data entries
    cursor = conn.execute("DELETE FROM maternal_health_risk WHERE HeartRate < 30")
    conn.commit()  #permanently save the changes to the database


def add_pulse_pressure_column(conn):
    #add pulse pressure column - engineered feature
    try:
        cursor = conn.execute("ALTER TABLE maternal_health_risk ADD COLUMN PulsePressure REAL")

    except sqlite3.OperationalError:
        print(f"Error adding PulsePressure column.")

    cursor = conn.execute("UPDATE maternal_health_risk SET PulsePressure = SystolicBP - DiastolicBP")
    conn.commit() 

def add_has_hypertension_column(conn):
    #add has_hypertension column - engineered feature
    try:
        cursor = conn.execute("ALTER TABLE maternal_health_risk ADD COLUMN HasHypertension INTEGER")

    except sqlite3.OperationalError:
        print(f"Error adding HasHypertension column.")

    cursor = conn.execute("" \
    "UPDATE maternal_health_risk " \
    "SET HasHypertension = CASE " \
    "WHEN SystolicBP >= 140 OR DiastolicBP >=90 " \
    "THEN 1 ELSE 0 " \
    "END")

    conn.commit()

def add_age_bracket_column(conn):
    #add age_bracket column - engineered feature
    try:
        cursor = conn.execute("ALTER TABLE maternal_health_risk ADD COLUMN AgeBracket TEXT")

    except sqlite3.OperationalError:
        print("Error adding AgeBracket column")

    cursor = conn.execute("" \
    "UPDATE maternal_health_risk " \
    "SET AgeBracket = CASE " \
    "WHEN Age < 20 THEN 'teen' " \
    "WHEN Age < 35 THEN 'reproductive_age' " \
    "ELSE 'advanced_maternal_age' " \
    "END")

    conn.commit()

def verify_database(conn):
    cursor = conn.execute("SELECT COUNT(*) FROM maternal_health_risk")
    for row in cursor:
        print(row)
    print()

    cursor = conn.execute("PRAGMA table_info(maternal_health_risk)")
    for row in cursor:
        print(row)
    print()

    cursor = conn.execute("SELECT COUNT(*) FROM maternal_health_risk WHERE PulsePressure IS NULL")
    for row in cursor:
        print(row)
    print()

    cursor = conn.execute("SELECT COUNT(*) FROM maternal_health_risk where HasHypertension = 1")
    for row in cursor:
        print(row)
    print()

    cursor = conn.execute("SELECT AgeBracket, COUNT(*) FROM maternal_health_risk GROUP BY AgeBracket")
    for row in cursor:
        print(row)
    print()

def close_connection(conn):
    conn.close()

if __name__ == "__main__":
    main()