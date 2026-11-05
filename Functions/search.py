import mysql.connector as mys
import csv
mydb = mys.connect(host='localhost', user='root', passwd = 'Firas@1704', database='Store')
myc = mydb.cursor()

q1 = "select * from stock"
myc.execute(q1)
data = myc.fetchall()

# Self-built Functions
def fileplay(temp, x=''):
    fobj = open('store.txt', 'w')
    for item in ['Sno', 'Type', 'Company', 'MRP', 'Status']:
        if item == x:
            s='>'+str(item)+'<'+'\t\t\t'
            fobj.write(s)
        else:
            s=str(item)+'\t\t\t'
            fobj.write(s)
    for row in temp:
        fobj.write('\n')
        for item in row:
            s=str(item)+'\t\t\t'
            fobj.write(s)
    
def display(temp, x=''):
    print("\n\n")
    for item in ['Sno', 'Type', 'Company', 'MRP', 'Status']:
        if item == x:
            print('>'+item+'<', end='\t\t')
        else:
            print(item, end='\t\t')
    for row in temp:
        print('\n')
        for item in row:
                print(item, end='\t\t')
    fileplay(temp, x)

def searchfilter(filter):
    qp = "Select * from stock order by " + filter
    myc.execute(qp)
    display(myc.fetchall(), filter)



display(data)
ans = 'Y'

while ans == 'Y' or ans == 'y':
    print("\n\n")
    print('1. Search by Name')
    print('2. Search by Filter')
    print('0. Exit')

    opt = int(input("Enter option to use:"))

    if opt == 1:
        pass
    
    elif opt == 2:
        print("\n\n")
        print('Choose filter')
        print('1. Type')
        print('2. Company')
        print('3. MRP')
        print('4. Status')

        fil = int(input("Enter filter:"))

        if fil == 1:    searchfilter('type')
        elif fil == 2:  searchfilter('company')
        elif fil == 3:  searchfilter('MRP')
        elif fil == 4:  searchfilter('Status')

    elif opt == 0:
        print("\n")
        print("Function terminated.")
        break

    else:
        print("\n")
        print("Incorrect option. Please try again.")

    print("\n")
    ans = input("Do you want to continue(Y/N):")

        

        
