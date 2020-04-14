#
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE employees (
            userid integer,
            fass text
            )""")
#vari1 = "hp"
#c.execute("INSERT INTO employees VALUES (:f_name)",{'f_name':vari1})
c.execute("INSERT INTO employees VALUES (:user, :f)",{'user':'1','f':"4;0.1"})
c.execute("INSERT INTO employees VALUES (:user, :f)",{'user':'1','f':"4;0.4"})
c.execute("INSERT INTO employees VALUES (:user, :f)",{'user':'1','f':"4;1.0"})
c.execute("INSERT INTO employees VALUES (:user, :f)",{'user':'1','f':"5;0.1"})
c.execute("INSERT INTO employees VALUES (:user, :f)",{'user':'2','f':"5;0.3"})
conn.commit()

c.execute("SELECT * from employees WHERE fass LIKE '4%'")
print(c.fetchall())
