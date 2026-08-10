import sqlite3

conn = sqlite3.connect("data/maternal_health_risk.db")

#select the first 5 rows from the maternal_health_risk table
cursor = conn.execute("SELECT * FROM maternal_health_risk LIMIT 5") 

for row in cursor:    #iterate through the cursor and print each row
    print(row)

print("")
#find irregular BPM data entries based on previous notebook detailing these
cursor = conn.execute("SELECT * FROM maternal_health_risk WHERE HeartRate < 30")

for row in cursor:
    print(row)

#delete irregular BPM data entries
cursor = conn.execute("DELETE FROM maternal_health_risk WHERE HeartRate < 30")
conn.commit()  #permanently save the changes to the database

#confirm irregular rows are deleted
cursor = conn.execute("SELECT * FROM maternal_health_risk WHERE HeartRate < 30")
for row in cursor:
    print(row)

conn.close()