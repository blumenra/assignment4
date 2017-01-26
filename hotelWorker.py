import time


class hotelWorker(object):

    def __init__(self, database):
        self.database = database
        self.print_formats = {'breakfast': "%s in room %s has been served breakfast at %s",
                         'wakeup': "%s in room %s received a wakeup call at %s",
                         'clean': "Rooms %s were cleaned at %s"}

    def concatenate_rooms(self, rooms):

        acc_list = ""
        for room in rooms:
            acc_list += str(room[0]) + ', '

        acc_list = acc_list.strip(' ')
        acc_list = acc_list.strip(',')

        return acc_list

    def dohoteltask(self, task_name, parameter):

        cursor = self.database.cursor()

        # clean task
        if parameter == 0:
            cursor.execute("SELECT Rooms.RoomNumber "
                           "FROM Rooms "
                           "LEFT JOIN Residents ON Rooms.RoomNumber = Residents.RoomNumber "
                           "WHERE Residents.RoomNumber IS NULL")

            rooms = cursor.fetchall()
            stringed_rooms = self.concatenate_rooms(rooms)

            print self.print_formats[task_name] % (stringed_rooms, str(time.time()))

        # breakfast, wakeup tasks
        else:
            cursor.execute("SELECT * "
                           "FROM Residents "
                           "WHERE RoomNumber = (?)",
                           (parameter,))

            room = parameter
            record = cursor.fetchone()
            first_name = record[1]
            last_name = record[2]
            name = first_name + ' ' + last_name

            print self.print_formats[task_name] % (name, room, str(time.time()))

        return str(time.time())
