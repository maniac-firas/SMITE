import mysql.connector as mys
x = mys.connect(host='localhost', user='root', passwd='', database='Store')
c = x.cursor()

#Accepting an order:
def order_update():
    order_id = int(input("Enter order ID to update:"))
    q = "select * from orders where id = {}".format(order_id)
    c.execute(q)
    order_data = c.fetchone()

    if order_data:
        new_quantity = int(input("Enter new quantity: "))
        update = "update orders set quantity ={} where id = {}".format(new_quantity,order_id)
        c.execute(update)
        x.commit()
        print("Order updated successfully!")
    else:
        print("Order not found.")

order_update()

while True:
    ch=input("would you like to continue?(y/n):")
    if ch==y:
        order_update()
    else:
        break
