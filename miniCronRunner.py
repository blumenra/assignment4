

def main():

create a worker
create a dictionary which will map between a taskId and time

while(dataBase.exists) {
    do next task:

        read unfinished tasks from db;
        make a worker to do it by using dohoteltask(taskname, parameter)
        save the returned time from the function and use it for the next time for this task
        update the numTimes field of the taskTimes table

}

if __name__ == '__main__':
    main()
