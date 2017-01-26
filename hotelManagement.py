import os
import sys
import sqlite3


def create_tables(database):

    cursor = database.cursor()

    cursor.execute("CREATE TABLE TaskTimes("
                   "TaskId integer PRIMARY KEY NOT NULL,"
                   "DoEvery integer NOT NULL,"
                   "NumTimes integer NOT NULL)")

    cursor.execute("CREATE TABLE Tasks("
                   "TaskId integer NOT NULL REFERENCES TaskTimes(TaskId),"
                   "TaskName text NOT NULL,"
                   "Parameter integer)")

    cursor.execute("CREATE TABLE Rooms("
                   "RoomNumber integer PRIMARY KEY NOT NULL)")

    cursor.execute("CREATE TABLE Residents("
                   "RoomNumber integer NOT NULL REFERENCES Rooms(RoomNumber),"
                   "FirstName text NOT NULL,"
                   "LastName text NOT NULL)")

    pass


def initialize_db(config_file_name):

    database = sqlite3.connect('cronhoteldb.db')

    create_tables(database)

    cursor = database.cursor()
    task_id = 0

    with open(config_file_name) as configFile:
        for line in configFile:
            line_list = line.strip('\n').split(',')
            if line_list[0] == 'room':
                cursor.execute("INSERT INTO Rooms VALUES(?)",
                               (line_list[1],))

                if len(line_list) == 4:
                    cursor.execute("INSERT INTO Residents VALUES(?,?,?)",
                                   (line_list[1], line_list[2], line_list[3],))

            else:
                if line_list[0] == 'clean':
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)",
                                   (task_id, line_list[0], 0,))
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)",
                                   (task_id, line_list[1], line_list[2],))
                    task_id += 1
                else:
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)",
                                   (task_id, line_list[0], line_list[2],))
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)",
                                   (task_id, line_list[1], line_list[3],))
                    task_id += 1

    database.commit()

    pass


def main():

    config_file = sys.argv[1]

    database_existed = os.path.isfile('cronhoteldb.db')

    if not database_existed:
        initialize_db(config_file)

if __name__ == '__main__':
    main()

