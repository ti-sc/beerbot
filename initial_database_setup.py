# This has to be executed only when you set up the beer-bot for the very first time.
# later it should be stored in a file called something like initial_db_setup.py

import sqlite3
conn = sqlite3.connect('../beerbot_database.db')
#creates a cursor
c = conn.cursor()

# create the table journal, where every transaction i stored
c.execute("""CREATE TABLE journal (
            user_id integer,
            date text,
            time text,
            amount real,
            keg_string text
            )""")
conn.commit()

# create the table keg_overview. Here all kegs are stored
c.execute("""CREATE TABLE keg_overview(
            keg_id integer,
            brand text,
            volume integer,
            price real,
            best_before string,
            deposit_payer string,
            beer_payer string,
            purchase_date string,
            status integer,
            remaining real
            )""")
conn.commit()

# create table user. This table includes all users who ever used your beer-bot.
c.execute("""CREATE TABLE users(
            user_id integer,
            first_name text,
            last_name text,
            database_access integer,
            tap_payer integer
            )""")
conn.commit()
# tap payer is integer if you want to use the user-id of the roommates (who pay) to link with guests.