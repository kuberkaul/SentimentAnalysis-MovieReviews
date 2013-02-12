from train import getwords, poswords, negwords 


testset= open('test_set.csv', 'r')
testset.readline()           
#evaluate the test set
output = open("prediction_file.csv", 'w')
for line in testset:
    linesplit = line.split()
    testwords= getwords(linesplit)
    totpos, totneg= 0.0, 0.0
    for word in testwords:
        word.lower()
        #get the (+1 smooth'd) number of counts this word occurs in each class
        #smoothing is done in case this word isn't in train set, so that there 
        #is no danger in dividing by 0 later when we do a/(a+b)
        #it's a trick: we are basically artifically inflating the counts by 1.
        a= poswords.get(word,0.0) + 1.0
        b= negwords.get(word,0.0) + 1.0  
             
        totpos+= a/(a+b)
        totneg+= b/(a+b) 
        '''
        if word in positivewordlist:
            totpos=a*2/(a+b)
        if word in negativewordlist:
            totneg = b*2/(a+b)
        #increment our score counter for each class, based on this word
        ''' 
    if totneg>totpos: 
        output.write("0," + line )
     
    if totneg<totpos: 
        output.write("1," + line ) 
        
    if totneg==totpos:
        output.write("0," + line)
testset.close()
output.close()

