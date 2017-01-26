import os
import sys
from time import time

import sqlite3


def create_tables(data_base):

    cursor = data_base.cursor()

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

    data_base = sqlite3.connect('cronhoteldb.db')

    create_tables(data_base)

    cursor = data_base.cursor()
    task_id = 0

    with open(config_file_name) as configFile:
        for line in configFile:
            line_list = line.strip('\n').split(',')
            if line_list[0] == 'room':
                cursor.execute("INSERT INTO Rooms VALUES(?)",
                               (line_list[0],))

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

    data_base.commit()

    pass


def main():

    # configFile = sys.argv[1]
    config_file = raw_input('Please enter the config file name: ')

    database_existed = os.path.isfile('cronhoteldb.db')

    if not database_existed:
        initialize_db(config_file)



    # create a DB file called cronhoteldb.db
    # create all tables from input file
    # insert records into tables according to input file

if __name__ == '__main__':
    main()
