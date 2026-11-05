import mysql.connector as mys


#Program Starters
mydb = mys.connect(host='localhost', user='root', passwd = 'Firas@1704', database='Store')
myc = mydb.cursor()

#Type codes
q='select SKU, Type from stock'
myc.execute(q)
temp = myc.fetchall()

data = []
for info in temp:
    st = info[0][7:9]
    data.append([st, info[1].upper()])
res = []
for val in data:
    if val not in res:
        res.append(val)

print(res)

with open('Type Codes.txt', 'w') as f:
    for row in res:
        f.write(row[0]+' - '+row[1]+'\n')