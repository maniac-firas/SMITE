with open('Company Codes.txt', 'r') as f:
        fr = f.read().split('\n')
        for i in range(len(fr)):        fr[i] = fr[i][7::]      
print(fr)
