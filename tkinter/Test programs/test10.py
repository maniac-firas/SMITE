import mysql.connector as mys

#Program Starters
mydb = mys.connect(host='localhost', user='root', passwd = 'Firas@1704', database='Store')
myc = mydb.cursor()

query = "SELECT SKU FROM Stock WHERE SKU LIKE %s"
myc.execute(query, ('SKU003' + '%',))
print(myc.fetchall()[0][0])