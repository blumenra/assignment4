

create a dictionary which will map between a taskName and its format of print line in tuple of strings

print 'hellon'
name = 'alon'
room = 100
map = {'taskName': "%s in room %s has been served breakfast at %s"}

time dohoteltask(taskname, parameter) {

    print map['taskName'] % (name, room, str(time()))

    return str(time() # str(time() cannot be assigned into a variable for some reason:(
}