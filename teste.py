import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

users = [
    (1, 'jose', 'asdf'),
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()