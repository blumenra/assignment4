import os
import time
import sqlite3

from hotelWorker import hotelWorker


def main():

    if os.path.isfile('cronhoteldb.db'):

        database = sqlite3.connect('cronhoteldb.db')
        hotel_worker = hotelWorker(database)
        cursor = database.cursor()

        cursor.execute("SELECT TaskId "
                       "FROM Tasks")

        task_ids = cursor.fetchall()
        last_task_times = {}
        for task_id in task_ids:
            last_task_times[task_id[0]] = 0

        while os.path.isfile('cronhoteldb.db'):

            cursor.execute("SELECT * "
                           "FROM Tasks JOIN TaskTimes ON Tasks.TaskId = TaskTimes.TaskId "
                           "WHERE TaskTimes.NumTimes != 0")

            tasks = cursor.fetchall()

            cursor.execute("SELECT * "
                           "FROM TaskTimes ")

            task_times = cursor.fetchall()

            if len(tasks) == 0:
                break

            for task in tasks:

                if float(last_task_times[task[0]]) + task_times[task[0]][1] <= time.time():

                    task_time = hotel_worker.dohoteltask(task[1], task[2])
                    last_task_times[task[0]] = task_time
                    cursor.execute("UPDATE TaskTimes "
                                   "SET NumTimes = NumTimes -1 "
                                   "WHERE TaskId = (?)",
                                   (task[0],))

        database.commit()


if __name__ == '__main__':
    main()
