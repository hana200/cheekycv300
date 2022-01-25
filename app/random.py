import random
import string
import datetime

def randomN(): 
    randomlist = []
    ls=[4,5,7]
    dt = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f') 
    k=[]
    for j in range(len(dt)):
        k.append(dt[j])

    results = list(map(int, k))

    for i in range(2,17):

        n = results[i]
        
        randomlist.append(n)
    for m in range(4):
        n = random.randint(0,9)
        randomlist.append(n)

    string_r1 = [str(int) for int in randomlist]
    str_of_ints = "".join(string_r1)

    #str_of_ints = str_of_ints2+str_of_ints1
   
    return str_of_ints
