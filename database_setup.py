import sqlite3

conn = sqlite3.connect('projects.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS projects 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_date TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS dogovors 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_date TEXT,
                signed_date TEXT,
                status TEXT,
                project_id INT,
                FOREIGN KEY(project_id) REFERENCES projects(id))''')

conn.commit()
