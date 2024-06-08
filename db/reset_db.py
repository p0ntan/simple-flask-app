import sqlite3
import csv

def convert_empty_to_null(value):
  return None if value == '' else value

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

files = [
  "user.csv",
  "category.csv",
  "topic.csv",
  "post.csv",
]

for csv_file in files:
  with open("./csv/" + csv_file, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    table = csv_file[:-4]

    placeholders = ', '.join(['?'] * len(headers))
    insert_sql = f"INSERT INTO {table} ({', '.join(headers)}) VALUES ({placeholders});"

    for row in reader:
      row = [convert_empty_to_null(value) for value in row]
      cursor.execute(insert_sql, row)

conn.commit()
conn.close()
