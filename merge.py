import csv
from datetime import datetime

INPUT_FILE_NAME = "data/new_data.csv"
OUTPUT_FILE_NAME = "data/Jordan.csv"
with open(INPUT_FILE_NAME, "r") as csvfile:
    with open(OUTPUT_FILE_NAME, "w") as outfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = reader.next()
        header.remove(header[-1])
        print header # ['BENCH', 'SQUAT', 'DEADLIFT', 'BODYWEIGHT']
        outfile.write(','.join(header) + "\n")
        for row in reader:
            row[0] = row[0][:6] + '20' + row[0][6:]
            row.remove(row[-1])
            # print row
            outfile.write(','.join(row) + "\n")

INPUT_FILE_NAME1 = "data/Jordan.csv"
INPUT_FILE_NAME2 = "data/Steve.csv"
INPUT_FILE_NAME3 = "data/Isaak.csv"

OUTPUT_FILE_NAME1 = "data/bench.csv"
OUTPUT_FILE_NAME2 = "data/squat.csv"
OUTPUT_FILE_NAME3 = "data/deadlift.csv"


with open(INPUT_FILE_NAME1, "r") as csvfile1:
    with open(INPUT_FILE_NAME2, "r") as csvfile2:
        with open(INPUT_FILE_NAME3, "r") as csvfile3:
            reader1 = csv.reader(csvfile1, delimiter=',')
            reader1.next()
            bench = {}
            squat = {}
            deadlift = {}
            for row in reader1:
                row[0] = datetime.strptime(row[0], '%m-%d-%Y')
                bench[row[0]] = [row[1], 'x', 'x']
                squat[row[0]] = [row[2], 'x', 'x']
                deadlift[row[0]] = [row[3], 'x', 'x']

            reader2 = csv.reader(csvfile2, delimiter=',')
            reader2.next()
            for row in reader2:
                row[0] = datetime.strptime(row[0], '%m-%d-%Y')
                if row[0] in bench:
                    bench[row[0]][1] = row[1]
                    squat[row[0]][1] = row[2]
                    deadlift[row[0]][1] = row[3]
                else:
                    bench[row[0]] = ['x', row[1], 'x']
                    squat[row[0]] = ['x', row[2], 'x']
                    deadlift[row[0]] = ['x', row[3], 'x']
            
            reader3 = csv.reader(csvfile3, delimiter=',')
            reader3.next()
            for row in reader3:
                row[0] = datetime.strptime(row[0], '%m-%d-%Y')
                if row[0] in bench:
                    bench[row[0]][2] = row[2]
                    squat[row[0]][2] = row[1]
                    deadlift[row[0]][2] = row[3]
                else:
                    bench[row[0]] = ['x', 'x', row[2]]
                    squat[row[0]] = ['x', 'x', row[1]]
                    deadlift[row[0]] = ['x', 'x', row[3]]

            bench = bench.items()
            bench_sorted = sorted(bench)
            squat = squat.items()
            squat_sorted = sorted(squat)
            deadlift = deadlift.items()
            deadlift_sorted = sorted(deadlift)
            # print squat_sorted
            with open(OUTPUT_FILE_NAME1, 'w') as outfile1:
                outfile1.write(",".join(["date", "Jordan", "Steve", "Isaak"]) + "\n")
                for each in bench_sorted:
                    date_string = each[0].strftime("%m-%d-%Y")
                    #print date_string
                    outfile1.write(date_string + "," + ','.join(each[1]) + "\n")
            with open(OUTPUT_FILE_NAME2, 'w') as outfile2:
                outfile2.write(",".join(["date", "Jordan", "Steve", "Isaak"]) + "\n")
                for each in squat_sorted:
                    date_string = each[0].strftime("%m-%d-%Y")
                    #print date_string
                    outfile2.write(date_string + "," + ','.join(each[1]) + "\n")
            with open(OUTPUT_FILE_NAME3, 'w') as outfile3:
                outfile3.write(",".join(["date", "Jordan", "Steve", "Isaak"]) + "\n")
                for each in deadlift_sorted:
                    date_string = each[0].strftime("%m-%d-%Y")
                    #print date_string
                    outfile3.write(date_string + "," + ','.join(each[1]) + "\n")

        