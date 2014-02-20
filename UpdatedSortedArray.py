'''
Created on Feb 20, 2014

@author: ric
'''

class UpdatedSortedArray(object):
    '''
    classdocs
    '''
    def addData(self,id,val):
        if self.full():
            self.update(id,val)
        else:
            self.add(id, val)
        self.data.sort(key=lambda x: x[1])
        
    def getSize(self):
        return len(self.data)-1

    def full(self):
        return self.getSize()==self.maxSize-1
    
    def empty(self):
        return
    
    def notEmpty(self):
        return len(self.data[0])>0
        # this will be 0 if array empty
    
    
    def add(self,id,val):
        if self.notEmpty(): 
            self.data.append([])
        x = self.getSize()
        self.data[x].append(id)
        self.data[x].append(val)
        
    def update(self,id, val):
        if val > self.data[0][1]:
            self.data[0][0] = id
            self.data[0][1] = val
            
    def getArray(self):
        return self.data
    
    def __init__(self, maxSize):
        '''
        Constructor
        '''
        self.data =[[]]
        self.maxSize = maxSize
        
        


def main():
    import random
    x = UpdatedSortedArray(3)
    for i in range(8):
        y = random.random()
        x.addData(i,y)
        print y
        y = x.getArray()
        for i in range(len(y)):
            print y[i][0], y[i][1]
        print
    

    return 0

if __name__ == '__main__':
    main()