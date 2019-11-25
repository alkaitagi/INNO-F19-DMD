import os
import psycopg2
import inserts

conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

cur = conn.cursor()
cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")

with open('tables.sql') as tables:
    cur.execute(tables.read())

rooms = inserts.insert_room(1, 5)
patients = inserts.insert_patient(101, 135, 1, 5)
doctors = inserts.insert_employee(1, 5, "doctor")
nurses = inserts.insert_employee(5, 10, "nurse")
prescribe = inserts.insert_prescribe(3, 1, 5, 101, 135)
analysis_report = inserts.insert_analysis_result(5, 101, 135)
attends = inserts.insert_attends(10000, 1, 5, 101, 135)
chat = inserts.insert_chat(3, 1, 5, 101, 135)
inventory = inserts.insert_inventory(3)
treatment_plan = inserts.insert_treatment_plan(3, 1, 5, 101, 135)
uses = inserts.insert_uses(0, 3, 0, 3)
logs = inserts.insert_log(3)

print(treatment_plan)

cur.execute(rooms)
cur.execute(patients)
cur.execute(doctors)
cur.execute(nurses)
cur.execute(prescribe)
cur.execute(analysis_report)
cur.execute(attends)
cur.execute(chat)
cur.execute(inventory)
cur.execute(treatment_plan)
cur.execute(uses)
cur.execute(logs)

print(rooms,
      patients,
      doctors,
      nurses,
      prescribe,
      analysis_report,
      attends,
      chat,
      inventory,
      treatment_plan,
      uses,
      logs,
      sep="\n")

conn.commit()
conn.close()
