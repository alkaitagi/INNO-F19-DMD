import os
import psycopg2
import inserts
import json


def readValue(val):
    if len(val) == 1:
        return val[0]
    else:
        return list(range(val[0], val[1]))


def writeSql(*queries):
    sql = '\n'.join(list(queries))

    with open("sql/population.sql", "w+") as file:
        file.write(sql)

    return sql


def populate():
    with open('json/population.json') as population:
        data = json.load(population)

        json_rooms = readValue(data["rooms"])
        json_beds = readValue(data["beds"])
        json_patients = readValue(data["patients"])
        json_doctors = readValue(data["doctors"])
        json_nurses = readValue(data["nurses"])
        json_analyzes = readValue(data["analyzes"])
        json_inventory_items = readValue(data["inventory_items"])
        json_treatment_plans = readValue(data["treatment_plans"])
        json_logs = readValue(data["logs"])
        json_prescribes = readValue(data["prescribes"])
        json_attends = readValue(data["attends"])
        json_chats = readValue(data["chats"])

    rooms = inserts.insert_rooms(json_rooms, json_beds)
    patients = inserts.insert_patients(json_patients, json_rooms)
    doctors = inserts.insert_employees(json_doctors, "doctor")
    nurses = inserts.insert_employees(json_nurses, "nurse")
    prescribes = inserts.insert_prescribes(json_prescribes, json_doctors,
                                           json_patients)
    analysis_reports = inserts.insert_analysis_results(json_analyzes,
                                                       json_patients)
    attends = inserts.insert_attends(json_attends, json_doctors, json_patients)
    chats = inserts.insert_chats(json_chats, json_doctors, json_patients)
    inventory = inserts.insert_inventory(json_inventory_items)
    uses = inserts.insert_uses(json_treatment_plans, json_inventory_items)
    logs = inserts.insert_logs(json_logs)
    treatment_plans = inserts.insert_treatment_plans(json_treatment_plans,
                                                     json_doctors,
                                                     json_patients)

    con = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    cur = con.cursor()

    cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    with open('sql/tables.sql') as tables:
        cur.execute(tables.read())
    cur.execute(
        writeSql(rooms, patients, doctors, nurses, prescribes,
                 analysis_reports, attends, chats, inventory, treatment_plans,
                 uses, logs))

    print(rooms, patients, doctors, nurses, prescribes,
                 analysis_reports, attends, chats, inventory, treatment_plans,
                 uses, logs)

    con.commit()
    con.close()
    print("Database created and  random data generated")

