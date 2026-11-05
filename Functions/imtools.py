# Self-built Functions
headings = []
headings.append(['Sno', 'Type', 'Company', 'MRP', 'Status'])

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
