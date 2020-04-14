# database management

# mit diesem skript kann die Bierbot-Datenbank verwaltet werden.
# use this script to manage the beerbot database

# import sqllite:
import sqlite3

print("Wenn die gesamte Bierbot-Datenbank neu angelegt werden soll, 'create_db' eingeben. \n")

while True:
    command = input("Befehl eingeben:\n")

    if command == "create_db":
        print("Datenbank wird neu angelegt, falls noch nicht vorhanden")
        # create database (if not existing)
        conn = sqlite3.connect(':memory:')

        # create variable for the cursor:
        c = conn.cursor()
    elif: command =="end":
        print("Datenbankverwaltung beendet.")
        break
    else:
        print("Ende, da Befehl nicht erkannt")
        break
