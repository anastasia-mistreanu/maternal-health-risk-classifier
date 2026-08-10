import sqlite3

def main(): 
    conn = sqlite3.connect("data/maternal_health_risk.db")
    remove_invalid_heart_rate_entries(conn)
    add_pulse_pressure_column(conn)
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

def close_connection(conn):
    conn.close()

if __name__ == "__main__":
    main()