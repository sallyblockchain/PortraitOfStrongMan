import sys
import os

f = open(sys.argv[1], 'r')

DATE = 0
NAME = 1
WEIGHT = 2
REP = 3
BODYWEIGHT=4

TIME_BETWEEN_SETS = 180
TIME_BETWEEN_REPS = 8
TIME_SET_MIN = 60

lifts = {}
weightProgression = {}
yearVolume = {}

for line in f:
    results = line.split(',')
    name = results[NAME].strip()
    date = results[DATE]
    yearSplit = date.split('-')
    if len(yearSplit) != 3:
        print "Skipping ", date
        continue
    year = yearSplit[2]
    if name not in lifts:
        lifts[name] = {} 
        lifts[name]['days'] = {}
    if date not in lifts[name]['days']:
        lifts[name]['days'][date] = {}
        lifts[name]['days'][date]['maxWeight'] = 0
        lifts[name]['days'][date]['totalWeight'] = 0
        lifts[name]['days'][date]['totalReps'] = 0
    if date not in weightProgression:
        weightProgression[date] = {}
        weightProgression[date]['totalWeight'] = 0
        weightProgression[date]['totalReps'] = 0
        weightProgression[date]['totalSets'] = 0
        weightProgression[date]['gymtime'] = 0
        if len(results) == 5:
            weightProgression[date]['bodyweight'] = results[BODYWEIGHT].strip()
        else:
            weightProgression[date]['bodyweight'] = 'x'
    if year not in yearVolume:            
        yearVolume[year] = {}
        print "Adding Year: ", year
    if name not in yearVolume[year]:
        yearVolume[year][name] = 0

    bodyweight = 'x'
    rep = 0
    weight = 0

    if len(results) == 5:
        if not results[WEIGHT].isdigit():
            #print "ERROR, not digit ", results[WEIGHT]
            continue
        bodyweight = results[BODYWEIGHT].strip()
        rep = int(results[REP])
        weight = int(results[WEIGHT])
    elif len(results) == 3 or len(results) == 4:
        repSplit = results[-1].strip().split('x')
        if len(repSplit) != 2:
            #print "Not in correct format: ", results
            continue
        repSplit[0] = repSplit[0].strip()
        repSplit[1] = repSplit[1].strip()
        if not (repSplit[0].isdigit() and repSplit[1].isdigit()):
            #print "Not a digit: ", results
            continue 
        rep = int(repSplit[1])
        weight = int(repSplit[0])
        #flip weight and rep
        if weight < rep:
            tmp = rep
            rep = weight
            weight = tmp
    else:
        #print "skipping this: ", results
        continue

    #see if this weight was the max weight
    if (weight > lifts[name]['days'][date]['maxWeight'] ):
        lifts[name]['days'][date]['maxWeight'] = weight
    #find how much weight was lifted 
    lifts[name]['days'][date]['totalWeight'] += ( rep*weight )
    #increment number of reps
    lifts[name]['days'][date]['totalReps'] += rep

    weightProgression[date]['totalWeight'] += ( rep*weight )
    weightProgression[date]['totalReps'] += rep
    weightProgression[date]['totalSets'] += 1

    yearVolume[year][name] += (rep*weight)

#remove exercises if not lifted on more than 20 days
delList = []
for name in lifts:
    if len(lifts[name]['days']) < 5:
        delList.append(name)

for name in delList:
    lifts.pop(name, None)


name1 = ""
name2 = ""
name3 = ""
num1 = 0
num2 = 0
num3 = 0

for name in lifts:
    if len(lifts[name]['days']) > num1:
        name3 = name2
        num3 = num2
        name2 = name1
        num2 = num1
        name1 = name
        num1 = len(lifts[name]['days'])
    elif len(lifts[name]['days']) > num2:
        name3 = name2
        num3 = num2
        name2 = name
        num2 = len(lifts[name]['days'])
    elif len(lifts[name]['days']) > num3:
        name3 = name
        num3 = len(lifts[name]['days'])

def printTop():
    print "Three most popular exercises: "
    print name1, " numDays: ", num1
    print name2, " numDays: ", num2
    print name3, " numDays: ", num3

topDay1 = []
topDay2 = []
topDay3 = []
sortedDates = []

for day in lifts[name1]['days']:
    topDay1.append(day)

for day in lifts[name2]['days']:
    topDay2.append(day)

for day in lifts[name3]['days']:
    topDay3.append(day)

for day in weightProgression:
    sortedDates.append(day)

#return 0 if same, -1 if date1 is earlier than date2, 1 if date1 is later than date2
def compareDate(date1, date2):
    date1Split = date1.split('-')
    date2Split = date2.split('-')
    #print "LENGHTS: ", len(date1Split), " : ", len(date2Split)
    if len(date1Split) != 3:
        return -1
    if len(date2Split) != 3:
        return 1
    year1 = int(date1Split[2])
    year2 = int(date2Split[2])
    month1 = int(date1Split[0])
    month2 = int(date2Split[0])
    day1 = int(date1Split[1])
    day2 = int(date2Split[1])

    if date1 == date2:
        return 0
    if (year1 < year2):
        return -1
    if (year1 > year2):
        return 1
    #years must be the same if we got here
    if (month1 < month2):
        return -1
    if (month1 > month2):
        return 1
    #months same if we got here
    if (day1 < day2):
        return -1
    if (day1 > day2):
        return 1
    return 0

def sortByDate(listToSort):
    sortedDates = []
    lastDate = "0-0-0"
    listLen = len(listToSort)
    i = 0
    while (i < listLen):
        currentSmallest = "" 
        for aDate in listToSort:
            if currentSmallest == "":
                currentSmallest = aDate
                continue
            if compareDate(currentSmallest, lastDate) <= 0:
                currentSmallest = aDate
                continue
            if compareDate(aDate, currentSmallest) == -1 and compareDate(aDate, lastDate) > 0:
                currentSmallest = aDate
        lastDate = currentSmallest
        sortedDates.append(currentSmallest)
        i += 1
    return sortedDates

topDay1 = sortByDate(topDay1)
topDay2 = sortByDate(topDay2)
topDay3 = sortByDate(topDay3)
sortedDates = sortByDate(sortedDates)
sortedDates.pop() #need to pop last day

def printInfo(name, sortedArray):
    print "Printing Info for: ", name
    for aDay in sortedArray:
        print "\t", aDay, " max: ", lifts[name]['days'][aDay]['maxWeight'], " total: ", lifts[name]['days'][aDay]['totalWeight']

def printTop3():
    print "Format: DATE | LIFT1 | LIFT1_MAXWEIGHT | LIFT1_TOTALWEIGHT | LIFT2 | ... | BODYWEIGHT | TOTALWEIGHT | TOTALSETS | TOTALREPS | GYMTIME (Minutes), | WEIGHT PER MIN"
    for aDate in sortedDates:
        maxWeight1 = 'x'
        total1 = 'x'
        if aDate in lifts[name1]['days']:
            maxWeight1 = lifts[name1]['days'][aDate]['maxWeight']
            total1 = lifts[name1]['days'][aDate]['totalWeight']
        maxWeight2 = 'x'
        total2 = 'x'
        if aDate in lifts[name2]['days']:
            maxWeight2 = lifts[name2]['days'][aDate]['maxWeight']
            total2 = lifts[name2]['days'][aDate]['totalWeight']
        maxWeight3 = 'x'
        total3 = 'x'
        if aDate in lifts[name3]['days']:
            maxWeight3 = lifts[name3]['days'][aDate]['maxWeight']
            total3 = lifts[name3]['days'][aDate]['totalWeight']
        totalTime = ((weightProgression[aDate]['totalSets']*TIME_BETWEEN_SETS) + (weightProgression[aDate]['totalReps']*TIME_BETWEEN_REPS) + (weightProgression[aDate]['totalSets']*TIME_SET_MIN))/60
        weightPerMin = 0
        if totalTime != 0:
            weightPerMin = weightProgression[aDate]['totalWeight']/totalTime
        print aDate, ",", name1, ",", maxWeight1, ",", total1, ",", name2, ",", maxWeight2, ",", total2, ",", name3, ",", maxWeight3, ",", total3, ",", weightProgression[aDate]['bodyweight'], ",", weightProgression[aDate]['totalWeight'], ",", weightProgression[aDate]['totalSets'], ",", weightProgression[aDate]['totalReps'], ",", totalTime, ",", weightPerMin

def printTopSimple():
    print "DATE ", name1, " ", name2, " ", name3 
    for aDate in sortedDates:
        maxWeight1 = 'x'
        total1 = 'x'
        if aDate in lifts[name1]['days']:
            maxWeight1 = lifts[name1]['days'][aDate]['maxWeight']
            total1 = lifts[name1]['days'][aDate]['totalWeight']
        maxWeight2 = 'x'
        total2 = 'x'
        if aDate in lifts[name2]['days']:
            maxWeight2 = lifts[name2]['days'][aDate]['maxWeight']
            total2 = lifts[name2]['days'][aDate]['totalWeight']
        maxWeight3 = 'x'
        total3 = 'x'
        if aDate in lifts[name3]['days']:
            maxWeight3 = lifts[name3]['days'][aDate]['maxWeight']
            total3 = lifts[name3]['days'][aDate]['totalWeight']
        totalTime = ((weightProgression[aDate]['totalSets']*TIME_BETWEEN_SETS) + (weightProgression[aDate]['totalReps']*TIME_BETWEEN_REPS) + (weightProgression[aDate]['totalSets']*TIME_SET_MIN))/60
        weightPerMin = 0
        if totalTime != 0:
            weightPerMin = weightProgression[aDate]['totalWeight']/totalTime
        print aDate, " ", maxWeight1, " ", maxWeight2, " ", maxWeight3


def printWeightInfo(input):
    if input not in lifts:
        print "The lift: " + input + " is not in our records"
        return
    print "Format: DATE | LIFT | LIFT_MAXWEIGHT | LIFT_TOTALWEIGHT"
    for aDate in sortedDates:
        maxWeight = 'x'
        total = 'x'
        if aDate in lifts[input]['days']:
            maxWeight = lifts[input]['days'][aDate]['maxWeight']
            total = lifts[input]['days'][aDate]['totalWeight']
        print aDate, " ", input, " ", maxWeight, " ", total

input = ""
while "quit" not in input and "exit" not in input:
    print "type 'quit' to exit, 'top' to print most popular lifts"
    print "'top1', 'top2', or 'top3' to print more specific information about the top 1, 2, and 3 lifts"
    print "'add' to see the additional lifts (less popular)"
    print "'weight' to see the bodyweight progression"
    print "'all' for aggregated data"
    input = raw_input()
    if "top1" in input:
        printInfo(name1, topDay1)
    elif "top2" in input: 
        printInfo(name2, topDay2)
    elif "top3" in input: 
        printInfo(name3, topDay3)
    elif "add" in input:
        for aName in lifts:
            print aName, len(lifts[aName]['days'])
    elif "top" in input:
        printTop()
    elif "weight" in input:
        for aDate in sortedDates:
            print aDate, " ", weightProgression[aDate]['bodyweight']    
    elif "all" in input:
        printTop3()
    elif "simple" in input:
        printTopSimple()
    elif "extra" in input:
        f = open("extra.txt", 'w')
        for year in yearVolume:
            print "Year: ", year
            for lift in yearVolume[year]:
                if yearVolume[year][lift] < 5000:
                    continue
                print "\t Lift: ", lift, " weight: ", yearVolume[year][lift]
                f.write(year + "," + lift + "," + str(yearVolume[year][lift]) + "\n" )
        f.close()
    elif "quit" not in input and "exit" not in input:
        printWeightInfo(input)
