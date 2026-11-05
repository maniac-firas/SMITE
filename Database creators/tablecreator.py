import csv
def establish_table(mydb, myc):
    myc.execute('create database Store if not exists')
    myc.execute('use database Store')
    mydb.commit()
    q1 = """Create table Stock if not exists(
    SKU varchar(50) NOT NULL primary key,
    product_name varchar(40),
    Type varchar(30),
    Company varchar(30),
    Floor int,
    Rack varchar(3),
    MRP int,
    Quantity int,
    DOM date,
    Delivery int,
    Status varchar(15)
                )"""
    myc.execute(q1)
    mydb.commit()

    recs = ''
    main = tuple()
    with open('Stock.csv', 'r') as f:
        fw = csv.reader(f)
        for row in fw:
                recs = recs + str(tuple(row)) + ', '
    recs=recs[0:len(recs)-2]

    q1 = "Insert into Stock (SKU, product_name, Type, Company, Floor, Rack, MRP, Quantity, DOM, Delivery, Status) values "+recs
    print(q1)
    myc.execute(q1)
    mydb.commit()
