import csv

with open("trips.csv") as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        print(line[:len(line)-1])