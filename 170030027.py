## Time Table Schedular
## Team => Naresh Kumar Kaushal, Bhavam Gupta, Rajat Kumar Dalai

import json
from z3 import *
import math

def timeToMint(time):                 ## Function to conver given time in hour:minute format to total number of minutes
    hour = math.floor(time)
    mint = int((time - hour)*100)
    return int(hour*60+mint)

def function(classes):               ## A helper function to set the cell width in .csv files
    coursename = classes[0]
    for course in courses:
        if course[0] == coursename:
            if course[2][0] == 180:
                return 100
            if course[2][0] == 60:
                return 30
            if course[2][0] == 90:
                return 50

#Read JSON data into the datastore variable
with open('170030027.json') as f:
    datastore = json.load(f)
instTimes = datastore["Institute time"]
classrooms = datastore["Classrooms"]
courses = datastore["Courses"]
prefTimeDoesntPref = datastore["Preference time not prefer"]
prefDayDoesntPref = datastore["Preference day not prefer"]
prefRoomDoesntPref = datastore["Preference room not prefer"]
prefOfRoomBatchDoesntPref = datastore["Preference of room batch not prefer"]

coursename = [] ## List storing the Name of the course
duration = []   ## List storing the Duration of the course 
Tempclasses = []    ## List storing the name of the classes

for course in courses:
    coursename.append(course[0])
    duration.append(course[2])

for classname in classrooms:
    Tempclasses.append(classname[0])

for i in range(len(instTimes)):
    for j in range(len(instTimes[i])):              ## Loop to convert Institute times to minutes using 'timeToMint()' function
        instTimes[i][j] = timeToMint(instTimes[i][j])

classAndCapacity = {}                               ## dictionary which maps the class to its capacity 
for i in range(len(classrooms)):
    if classrooms[i][1] not in classAndCapacity:
        classAndCapacity[classrooms[i][1]] = [classrooms[i][0]]
    else:
        classAndCapacity[classrooms[i][1]] += [classrooms[i][0]]


days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

## ******************We will create a class of Room which has a constructor which initialise the following parametres:************************
## Course => Course running in this object of room class
## Day => For which day this object of room class is created
## Room => What is the name of the object of this room class i.e LH1,LT1,LT2 etc.
## Count => Count is the value which goes from 1 to number of lectures possible for given course.  
## StartTime => It is a Z3 variable named as coursename_count_start_Time eg. CS228_1_start_Time.
## EndTime => It is a Z3 variable named as coursename_count_end_Time eg. CS228_1_end_Time.
## Batch => The name of the batch studying in this object of room class.
## Capacity => The capacity of this object of room class.
## Faculty => The name of the faculty teaching in this object of room class.

class Room:
    def __init__(self,course,count,batch,capacity,faculty):
        self.course = course
        self.day = String('{}_{}_day'.format(course,count))
        self.room = String('{}_{}_room'.format(course,count))
        self.startTime = Real('{}_{}_start_Time'.format(course,count))
        self.EndTime = Real('{}_{}_end_Time'.format(course,count))
        self.Batch = batch
        self.Capacity = capacity
        self.Faculty = faculty

## Creating the objects of Room class   
var = [[Room(coursename[j],i,courses[j][4],courses[j][1],courses[j][3]) for i in range(len(duration[j]))] for j in range(len(duration))]

## Constraint which fixed the domain of day variable to Sunday,Monday------------Saturday.
val_for_days = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = [var[i][j].day == String(Day) for Day in days]
        val_for_days.append(Or(*exp))

## Constraint which specifies that a particular course can't have more than 1 class a particular day.
constr_1 = []
for i in range(len(duration)):
    exp1 = Distinct([var[i][j].day for j in range(len(duration[i]))])
    constr_1.append(exp1)
constraint = [And(*constr_1)]

## Constraint which specifies that Time during which the course runs must be whithin the institute specified timings.
val_for_st_and_end_times = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = [And(Or(And(var[i][j].EndTime <= instTimes[1][1],var[i][j].startTime >= instTimes[1][0]),
                  And(var[i][j].startTime >= instTimes[0][0], var[i][j].EndTime <= instTimes[0][1])),var[i][j].startTime < var[i][j].EndTime)]
        val_for_st_and_end_times.append(*exp)

## Constraint which states that (EndTime-StartTime == Duration) for the particular course.
constr_2 = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = (var[i][j].EndTime - var[i][j].startTime) == duration[i][j]
        constr_2.append(exp)

## Just storing the objects of the room class in  asinle list rather than 2 dimensional list.
list_of_var = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        list_of_var.append(var[i][j])

## Constraint which specifies that if the 2 courses are different and running on same day and (Having the same batch OR
##                                                                                             Having the same faculty teaching OR
##                                                                                             Running in the same room) Then
## they must run at differnt timings.
constr_for_clashes = []
for i in range(len(list_of_var)):
    for j in range(len(list_of_var)):
        exp1 = False
        if i != j:
            for m in range(len(list_of_var[i].Batch)):
                for n in range(len(list_of_var[j].Batch)):
                    if list_of_var[i].Batch[m] == list_of_var[j].Batch[n]:
                        exp1 = True
                        break
                if exp1 == True:
                    break

        exp = If(Or(And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, exp1),
                    And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, list_of_var[i].Faculty == list_of_var[j].Faculty),
                    And(list_of_var[i] != list_of_var[j], list_of_var[i].day == list_of_var[j].day, list_of_var[i].room == list_of_var[j].room)),
                 Or(list_of_var[i].startTime >= list_of_var[j].EndTime, list_of_var[j].startTime >= list_of_var[i].EndTime),
                 True)
        constr_for_clashes.append(exp)


## Constraint which specifies that name of the room object will be the one given in the list specified in the JSON file. 
val_for_room = []
for i in range(len(duration)):
    for j in range(len(duration[i])):
        exp = Or(*[var[i][j].room == String(rooom) for rooom in classAndCapacity[courses[i][1]]])
        val_for_room.append(exp)


## Constraint which impose certain timing constraints because of the choice of faculty.
constrCozOfChoiceOfTimeOfProf = []
for i in range(len(list_of_var)):
    for j in range(len(prefTimeDoesntPref)):
        exp = If(list_of_var[i].Faculty == prefTimeDoesntPref[j][0],
                 And(Or(list_of_var[i].startTime < timeToMint(prefTimeDoesntPref[j][1][0]),list_of_var[i].startTime > timeToMint(prefTimeDoesntPref[j][1][1])),
                     Or(list_of_var[i].EndTime < timeToMint(prefTimeDoesntPref[j][1][0]),list_of_var[i].EndTime > timeToMint(prefTimeDoesntPref[j][1][1]))),
                 True)
        constrCozOfChoiceOfTimeOfProf.append(exp)

## Constraint which impose certain constraints regarding preference of day by particular professor.
constrCozOfChoiceOfDayOfProf = []
for i in range(len(list_of_var)):
    for j in range(len(prefDayDoesntPref)):
        exp = If(list_of_var[i].Faculty == prefDayDoesntPref[j][0],
                 And(*[list_of_var[i].day != String(day) for day in prefDayDoesntPref[j][1]]),
                 True)
        constrCozOfChoiceOfDayOfProf.append(exp)

## Constraint which impose certain constraints regarding prefernce of room by particular professor.
constrCozOfChoiceOfRoomOfProf = []
for i in range(len(list_of_var)):
    for j in range(len(prefRoomDoesntPref)):
        exp = If(list_of_var[i].Faculty == prefRoomDoesntPref[j][0],
                 And(*[list_of_var[i].room != String(room) for room in prefRoomDoesntPref[j][1]]),
                 True)
        constrCozOfChoiceOfRoomOfProf.append(exp)

## Constraing which restricts certain batches to have classes in particular rooms.
constrCozOfChoiceOfRoomOfBatch = []
for i in range(len(list_of_var)):
    exp1 = False
    idx = 0
    for m in range(len(list_of_var[i].Batch)):
        for n in range(len(prefOfRoomBatchDoesntPref)):
            if list_of_var[i].Batch[m] == prefOfRoomBatchDoesntPref[n][0]:
                idx = n
                exp1 = True
                break
        if exp1 == True:
            break
    exp = If(exp1,
            And(*[list_of_var[i].room != String(room) for room in prefOfRoomBatchDoesntPref[idx][1]]),
            True)
    constrCozOfChoiceOfRoomOfBatch.append(exp)

## Finally feeding all the constraints to the solver.
S = Solver()
S.add(val_for_days)
S.add(constraint)
S.add(val_for_st_and_end_times)
S.add(constr_2)
S.add(val_for_room)
S.add(constr_for_clashes)
S.add(constrCozOfChoiceOfTimeOfProf)
S.add(constrCozOfChoiceOfDayOfProf)
S.add(constrCozOfChoiceOfRoomOfProf)
S.add(constrCozOfChoiceOfRoomOfBatch)

S.check()
m = S.model()

printingTT = {}
mappingOfRoom = {}  ## Dictionary which maps the room variable to names of the room available in JSON file
mappingOfDay = {}   ## Dictionary which maps the day variable to days available.


## This loop just fills the 'mappingOfRoom' dictionary
for i in range(len(list_of_var)):
    temp = m.evaluate(list_of_var[i].room)
    for roomcap in classrooms:
        if temp == m.evaluate(String(roomcap[0])):
            mappingOfRoom[temp] = roomcap[0]

## This loop just fills the 'mappingOfDay' dictionary
for i in range(len(list_of_var)):
    temp = m.evaluate(list_of_var[i].day)
    for day in days:
        if temp == m.evaluate(String(day)):
            mappingOfDay[temp] = day

## This loop just fills the 'printingTT' dictionary
for i in range(len(list_of_var)):
    if mappingOfDay[m.evaluate(list_of_var[i].day)] not in printingTT:
        printingTT[mappingOfDay[m.evaluate(list_of_var[i].day)]] = [[list_of_var[i].course,simplify(m.evaluate(list_of_var[i].startTime)/60),simplify(m.evaluate(list_of_var[i].EndTime)/60),mappingOfRoom[m.evaluate(list_of_var[i].room)],list_of_var[i].Faculty,list_of_var[i].Batch]]
        print()
    else:
        printingTT[mappingOfDay[m.evaluate(list_of_var[i].day)]] += [[list_of_var[i].course,simplify(m.evaluate(list_of_var[i].startTime)/60),simplify(m.evaluate(list_of_var[i].EndTime)/60),mappingOfRoom[m.evaluate(list_of_var[i].room)],list_of_var[i].Faculty,list_of_var[i].Batch]]

print(printingTT)

## Now this part is just to print the time table in csv format.
columns = ["Day","class","8.30-9:00","9:00-9:30","9:30-10:00","10:00-10:30","10:30-11:00","11:00-11:30","11:30-12:00","12:00-12:30","14:00-14:30","14:30-15:00","15:00-15:30","15:30-16:00","16:00-16:30","16:30-17:00"]
mapTime = {'8.5':'8.30-9:00','9':'9:00-9:30','9.5':'9:30-10:00','10':"10:00-10:30",'10.5':'10:30-11:00','11':"11:00-11:30",'11.5':'11:30-12:00','12':"12:00-12:30",'14':'14:00-14:30','14.5':"14:30-15:00",'15':'15:00-15:30','15.5':"15:30-16:00",'16':'16:00-16:30','16.5':"16:30-17:00"}
import csv
with open('TimeTable.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=columns)
    writer.writeheader()
    for day in days:
        listOfDictionaries = []
        count = 0

        for classn in Tempclasses:
            if classn == 'LAB5' or classn == 'LAB2' or classn == 'LAB6' or classn == 'LAB7' or classn == 'LAB8' or classn == 'LAB9' or classn == 'LAB10' :
                if count == 0:
                    temp = {'Day':day,'class':'LAB'}
                    listOfDictionaries.append(temp)
                    count += 1
            else:
                temp = {'Day':day,'class':classn}
                listOfDictionaries.append(temp)
        #CL1,CL2,CL3,LH1,LH2,LT1,LT2,T1,T2,T3,LAB = {'Day':day,'class':'CL1'},{'Day':day,'class':'CL2'},{'Day':day,'class':'CL3'},{'Day':day,'class':'LH1'},{'Day':day,'class':'LH2'},{'Day':day,'class':'LT1'},{'Day':day,'class':'LT2'},{'Day':day,'class':'T1'},{'Day':day,'class':'T2'},{'Day':day,'class':'T3'},{'Day':day,'class':'LAB'}
        for classes in printingTT[day]:
            # for classe,cap in classrooms:
            time = mapTime[classes[1].as_decimal(1)]
            merge = function(classes)
            cellvalue = classes[0]+classes[4]
            # value = '{0: < merge}'.format(cellvalue)
            for diction in listOfDictionaries:
                if classes[3] == 'LAB5' or classes[3] == 'LAB2' or classes[3] == 'LAB6' or classes[3] == 'LAB7' or classes[3] == 'LAB8' or classes[3] == 'LAB9' or classes[3] == 'LAB10' :
                    if diction['class'] == 'LAB':
                        if time not in diction:
                            diction[time] = [[classes[0],classes[4]]]
                        else:
                            diction[time] += [[classes[0],classes[4]]]
                        break

                elif classes[3] == diction['class']: 
                    if merge == 30:
                        diction[time] = '{0: <30}'.format(cellvalue)
                    elif merge == 50:
                        diction[time] = '{0: <50}'.format(cellvalue)
                    break
        writer.writerows(listOfDictionaries)