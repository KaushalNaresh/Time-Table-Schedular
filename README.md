# Readme
## Time-Table-Sceduler
A program which automatically prints the Time Table given certain constraints using python Z3 Library.

> Name : Naresh Kumar Kaushal  
 > Department : CSE, Term : Third Year  
> Course Instructor : Dr. Sreejith AV 

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Required Files](#required-files)
3. [How to run](#how-to-run)
4. [Structure](#structure)
5. [Propositions Involved](#propositions-involved)
6. [Addiotional Info And Resources](#additional-info-and-resources)

## Prerequisites  
<div style="text-align: justify"> 

In order to run this Timetable schedular system on your PC you need to install python3 <https://realpython.com/installing-python/> a link to install the same. You also need to install Z3 library developed by Microsoft <https://github.com/Z3Prover/z3/releases> a link for the same. After installing Z3 library do not forget to add that to the PATH variable on your PC. 

</div>

## Required Files
<div style="text-align: justify">

In order to run this schedular make one folder on your desktop name it as you wish and then add the json
and python script file given by us to that same folder.
1. 170030027.json
2. 170030027.py 

</div>

## How to run
<div style="text-align: justify">

Just open the command prompt in the same folder you have created and type *python 170030027.py* It will take few seconds to print the time table on your console but since its hard to interpret what’s going on so it will also generate one csv file *TimeTable.csv* open it with Microsoft Excel to see the final output in a more aesthetic way.

</div>

## Structure
<div style="text-align: justify">

**Universe** – x and y belongs to instances of Room class.   
**Relations involved** 
- day() which maps the day variable of Room object to Mon,Tue,Wed,Thurs,Fri  
- Course() which maps course variable of Room Object to rooms present in json file.  
- Start_Time() which maps the starting time of the course to [8:30-12:30] Or [14:00 – 17:00]  
- End_Time() which maps the starting time of the course to [8:30-12:30] Or [14:00 – 17:00]  
- Faculty() which maps the faculty variable of Room object to one of the faculties present in json file.   
- Batch() which maps the batch variable of Room object to one of the batches in json file.  
- Room() which maps the class variable of Room object to one of the classes present in json file.   

**Constants involved** 
-  ‘Monday’, ‘Tuesday’, ‘Wednesday’, ‘Thursday’, ‘Friday’  
- ‘CL1’, ‘CL2’, ‘CL3’, ‘LT1’, ‘LT2’, ‘LH2’, ‘LH1’  
- ChoiceOfTime which has [Faculty, TimeNotPrefered]  
- ChoiceOfDay which has [Faculty, DayNotPrefered]  
- ChoiceOfRoom which has [Faculty, RoomNotPrefered]  
- RestrictionOnRoom which has [Batch, RoomNotAllowed] 

</div>

## Propositions involved
<div style="text-align: justify">

1. For All x (day(x) == (‘Monday’ Or ‘Tuesday’ Or ‘Wednesday’ Or ‘Thursday’ Or ‘Friday’))
2. For All x For All y (x != y And (course(x) == course(y) -> day(x) != day(y))
3. For All x ((start_Time(x) >= Institute_Start_Time) And (end_Time(x) <= Institute_end_Time) And (start_Time(x) < end_Time(x))
4. For All x (end_Time(x) – start_Time(x) == Duration)
5. For All x For All y ( x!=y And day(x) != day(y) And( Batch(x) == Batch(y) Or Faculty(x) == Faculty(y) Or Room(x) == Room(y)) -> (start_Time(x) >= end_Time(y) Or start_Time(y) >= end_Time(x))
6. For All x ( Room(x) == (‘CL1’ Or ‘CL2’ Or ‘CL3’ Or ‘LT1’ Or ‘LT2’ Or ‘LH2’ Or ‘LH1’))
7. Faculty(x) € ChoiceOfTime.Faculty -> (start_Time(x) And end_Time(x) != ChoiceOfTime.Faculty.Time)
8. Faculty(x) € ChoiceOfDay.Faculty -> (day(x) != ChoiceOfDay.Faculty.Day)
9. Faculty(x) € ChoiceOfRoom.Faculty -> (Room(x) != ChoiceOfRoom.Faculty.Room)
10. Batch(x) € RestrictionOnRoom.Batch -> (Room(x) != RestrictionOnRoom.Batch.Room)  

</div> 
 

|**Variable** |**Explanation**|    
|:----------: | :------------:|  
|**Institute time** | This variable stores the Time for which classes run in IIT Goa. |  
|**Classrooms** | This stores the list of lists which includes [class name, capacity] |  
|**Courses** | This store list of lists which includes [course name, capacity, [duration], faculty, [batches taking this course]]  |  
|**Preference time not prefer** | This includes [Faculty Name, [Time He/She do not like to prefer]] |  
|**Preference day not prefer** | This includes [Faculty Name, [Day He/She do not like to prefer]] |  
|**Preference room not prefer** | This includes [Faculty name, [Room He/She do not like to prefer]] |  
|**Preference of room batch not prefer** | This includes [Batch name, [classes where particular batch can’t have classes]] |  

## Additional Info And Resources    
<div style="text-align: justify">  

To learn more about Z3 library follow the link <https://ericpony.github.io/z3py-tutorial/guideexamples.htm> and HAPPY CODING 😊  
We are providing you the sample of csv file generated by us with little formatting done in Microsoft Excel in pdf format named “TimeTable_1.pdf”.  

**For Further queries drop an email on:**  
<naresh.kaushal.17003@iitgoa.ac.in>  
<bhavam.gupta.17002@iitgoa.ac.in>  
<rajat.kumar.17001@iitgoa.ac.in>
 
</div>
