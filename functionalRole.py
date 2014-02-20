#  
#  
import math
import sys
orderedList = []
for i in range(40):
    a = []
    a.append("E")
    a.append(0)
    orderedList.append(a)




def addToList(name,val):
    n = 0
    orderedList[n][0]=name
    orderedList[n][1]=val
    
    while n< 39  and orderedList[n][1] > orderedList[n+1][1]:
        holdn =  orderedList[n+1][0]
        holdv =  orderedList[n+1][1]
        orderedList[n+1][0] = orderedList[n][0]
        orderedList[n+1][1] = orderedList[n][1]
        orderedList[n][0] = holdn
        orderedList[n][1] = holdv
        n+=1


def getLog(a):
    if a == 0:
        return 0
    return math.log(a*1.0)


def loadSpecies(speciesFile):
    print speciesFile
    data = open(speciesFile,"r")
    count =0
    functions = {}
    types = ["N","P"]
    types = {}
    types['N'] =0;
    types['P'] =0;
    for line in data:
        row = line.strip().replace(', ','\t').replace('; ','\t').replace(' / ','\t').split("\t")
        if(row[3] in types):
            types[row[3]]+=1
            typesc = []
            print ("%s\t%s\t%s\t%s\t%s\t%d"%(row[0],row[1],row[2],row[3],row[4],len(row)-4))
            for i in range (5, len(row)-4):
                #print row[i]
                if typesc.count(row[i]) == 0 :
                    typesc.append(row[i])
                    if (row[i] in functions)==False:
                        functions[row[i]]={}
                        functions[row[i]]['N']=0
                        functions[row[i]]['P']=0
                        
                    functions[row[i]][row[3]] += 1

    data.close()
    print len(functions)
    #mi = 0
    #for each value x taken by f1:
    #{  sum = 0
   #for each value y taken by f2:
   #{  p_xy = number of examples where f1=x and f2=y
   #  p_x = number of examples where f1=x
   #   p_y = number of examples where f2=y
   #   sum += p_xy * log(p_xy/(p_x*p_y))
   #}
   #mi += sum
   #}
    
    
    counter = 0
    t = types['N']+types['P']
    tn = float(types['N'])/t
    tp = float(types['P'])/t
    for f in functions:
        n = float(functions[f]['N'])/t
        p = float(functions[f]['P'])/t
        tt = float(functions[f]['P']+functions[f]['N'])/t
        if n > 0 :
            rn =  n * math.log( n/ ((tt) * tn))
        else:
            rn = 0
        if p > 0:
            rp =  p * math.log( p / ((tt) * tp))
        else:
            rp = 0
        v = rn+rp
        addToList(f,v)

    for i in range(1,40):
        print orderedList[i][1],"\t",functions[orderedList[i][0]]['N'],"\t",functions[orderedList[i][0]]['P'],"\t",orderedList[i][0]
    return 0


def main():
    dataFile = sys.argv[1]
    loadSpecies(dataFile)
    

    return 0

if __name__ == '__main__':
    main()

