import csv

data = [1, 2, 3]

with open('C:/Users/Firas/OneDrive/Desktop/F5 Club Project/Database creators/Test.csv', 'w', newline='') as f:
    fw = csv.writer(f)
    fw.writerow(data)
    print('Completed')