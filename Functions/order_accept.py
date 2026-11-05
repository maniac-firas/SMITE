#Accept an order

import mysql.connector as mys
mydb = mys.connect(host='localhost', user='root', passwd='', database='Store')
c = mydb.cursor()

#creating the table with tbale name 'orders'
c.execute('''create table if not exists orders (
    id int primary key,
    customer_name varchar(100),
    item_id int,
    quantity int)''')

def order_accept():
    Id=int(input('enter customer id:'))
    customer_name = input("Enter customer name: ")
    item_id = int(input("Enter item ID: "))
    quantity = int(input("Enter quantity: "))

    q = "insert into orders values ("+str(Id)+','+str(customer_name)+','+str(item_id)+','+str(quantity)+')'
    c.execute(q)
    x.commit()
    print("Order placed successfully!")

num=int(input("How many orders would you like to place?"))
i=0
while i<=num:
    order_accept()
    i+=1
