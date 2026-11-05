import mysql.connector as mys
x = mys.connect(host='localhost', user='root', passwd='Sreeraj@2007', database='Store')
c = x.cursor()

#Deleting an order:
def order_delete():
    order_id=int(input("Enter order ID to update:"))
    q = "select * from orders where id = %s"
    c.execute(q, (order_id,))
    order_data = c.fetchone()

    if order_data:
        new_quantity = int(input("Enter new quantity: "))
        update= "update orders set quantity ={} where id = {}".format(new_quantity,order_id)
        c.execute(update)
        x.commit()
        print("Order updated successfully!")
    else:
        print("Order not found.")

order_delete()
