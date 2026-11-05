import csv
def establish_table(mydb, myc):
    myc.execute('Drop Table if exists Stock;')
    q1 = """CREATE TABLE stock (
        SKU VARCHAR(50) NOT NULL PRIMARY KEY,
        product_name VARCHAR(40),
        Type VARCHAR(30),
        Company VARCHAR(30),
        Floor INT,
        Rack VARCHAR(3),
        MRP INT,
        Quantity INT,
        DOM DATE,
        Delivery INT,
        Status VARCHAR(15)
    )"""
    myc.execute(q1)
    mydb.commit()
    
    with open('Stock.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)

        for row in csv_reader:
            q2 = """INSERT INTO stock (SKU, product_name, Type, Company, Floor, Rack, MRP, Quantity, DOM, Delivery, Status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    product_name=VALUES(product_name),
                    Type=VALUES(Type),
                    Company=VALUES(Company),
                    Floor=VALUES(Floor),
                    Rack=VALUES(Rack),
                    MRP=VALUES(MRP),
                    Quantity=VALUES(Quantity),
                    DOM=VALUES(DOM),
                    Delivery=VALUES(Delivery),
                    Status=VALUES(Status)"""
            myc.execute(q2, row)