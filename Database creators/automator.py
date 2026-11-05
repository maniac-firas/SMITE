import mysql.connector as mys
import csv
mydb = mys.connect(host='localhost', user='root', passwd = 'Firas@1704', database='Store')
myc = mydb.cursor()

recs = ''
main = tuple()
with open('Stock.csv', 'r') as f:
    fw = csv.reader(f)
    for row in fw:
            recs = recs + str(tuple(row)) + ', '
recs=recs[0:len(recs)-2]

q1 = "Insert into Stock (SKU, product_name, Type, Company, Floor, Rack, MRP, Quantity, DOM, Duration, Delivery, Status) values "+recs
print(q1)
myc.execute(q1)
mydb.commit()
print('Finished')



            
            
