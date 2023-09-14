import sqlite3
import datetime

conn = sqlite3.connect('projects.db')
cursor = conn.cursor()


class Dogovor:
    def __init__(self, name, project=None, id=None):
        self.id = id
        self.name = name
        self.created_date = datetime.datetime.now()
        self.signed_date = None
        self.status = "Черновик"
        self.project = project

    def create(self):
        cursor.execute('''INSERT INTO dogovors (name, created_date, signed_date, status, project_id) 
                                VALUES (?, ?, ?, ?, ?)''', (
            self.name, self.created_date, self.signed_date, self.status,
            None if self.project is None else self.project.id))
        conn.commit()

    def confirm(self):
        self.status = "Активен"
        self.signed_date = datetime.datetime.now()
        cursor.execute("UPDATE dogovors SET signed_date = ?, status = ? WHERE id = ?",
                       (self.signed_date, self.status, self.id))
        conn.commit()

    def finish(self):
        self.status = "Завершен"
        cursor.execute("UPDATE dogovors SET status = ? WHERE id = ?", (self.status, self.id))
        conn.commit()


class Project:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.created_date = datetime.datetime.now()
        self.dogovors = []

    def create(self):
        cursor.execute('''INSERT INTO projects (name, created_date) 
                                VALUES (?, ?)''', (self.name, self.created_date))
        conn.commit()

    def add_dogovor(self, dogovor):
        if dogovor[4] == "Активен":
            cursor.execute("UPDATE dogovors SET project_id = ? WHERE id = ?", (self.id, dogovor[0]))
            conn.commit()

    def finish_dogovor(self, dogovor):
        if dogovor in self.dogovors:
            dogovor.finish()
            cursor.execute("UPDATE dogovors SET status = ? WHERE id = ?", (dogovor.status, dogovor.id))
            conn.commit()


def create_dogovor(name):
    return Dogovor(name).create()


def create_project(name):
    return Project(name).create()


def print_column_names_dogovor():
    cursor.execute("PRAGMA table_info(dogovors)")
    results = cursor.fetchall()
    column_names = [result[1] for result in results]
    print(column_names)


def show_active_dogovors():
    with conn as connection:
        cursor = connection.cursor()
        print_column_names_dogovor()

        cursor.execute("SELECT * FROM dogovors WHERE status=? AND (project_id IS NULL)", ('Активен',))
        results = cursor.fetchall()
        for row in results:
            print(row)


def count_active_dogovor():
    count = cursor.execute("SELECT COUNT(*) FROM dogovors WHERE status=?", ('Активен',))
    count_dogovors = count.fetchone()[0]
    return count_dogovors


def print_column_names_projects(name=None):
    cursor.execute("PRAGMA table_info(projects)")
    results = cursor.fetchall()
    column_names = [result[1] for result in results]
    if name is not None:
        column_names.append(name)
    print(column_names)


def show_projects():
    with conn as connection:
        cursor = connection.cursor()
        print_column_names_projects()

        cursor.execute(
            'SELECT projects.id, projects.name, projects.created_date FROM projects LEFT '
            'JOIN dogovors ON projects.id = dogovors.project_id')
        results = cursor.fetchall()

        for row in results:
            print(row)


def show_projects_no_dogovors():
    with conn as connection:
        cursor = connection.cursor()
        print_column_names_projects()

        cursor.execute(
            "SELECT * FROM projects p WHERE NOT EXISTS (SELECT 1 FROM dogovors d WHERE d.status = 'Активен' AND p.id "
            "= d.project_id)")
        results = cursor.fetchall()
        for row in results:
            print(row)


def projects_with_active_dogovor():
    with conn as connection:
        cursor = connection.cursor()
        print_column_names_projects('dogovor_id')

        cursor.execute(
            "SELECT * FROM projects p WHERE EXISTS (SELECT 1 FROM dogovors d WHERE d.status = 'Активен' AND p.id = "
            "d.project_id)")
        results = cursor.fetchall()
        id_projects = []
        for row in results:
            id_projects.append(row[0])
            print(row)
        return id_projects


def return_active_id_dogovors_for_project(id_proj):
    with conn as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT dogovors.id as dogovor_id FROM dogovors LEFT '
            'JOIN projects ON projects.id = dogovors.project_id WHERE projects.id=? and dogovors.status=?', (id_proj, 'Активен'))
        results = cursor.fetchall()
        if results:
            number = results[0][0]
        return number
