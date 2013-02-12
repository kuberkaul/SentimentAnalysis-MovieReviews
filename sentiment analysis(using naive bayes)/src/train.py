from porter import PorterStemmer


def getwords(sentence):
    
    #this method returns important words from a sentence as list
    #w= sentence.split()
    w = sentence
    
    #get rid of all stop words
    w= [x for x in w if not x in stopwords]
    
    #remove all things that are 1 or 2 characters long (punctuation)
    w= [x for x in w if len(x)>1]    
    
    #stem each word
    w= [stemmer.stem(x,0,len(x)-1) for x in w]
    
    #add bigrams
    #w= w + [w[i]+' '+w[i+1] for i in range(len(w)-1)]
    
    #get rid of duplicates by converting to set and back to list
    #this works because sets dont contain duplicates
    #w= list(set(w))
    
    return w

if __name__ == '__main__':
    '''
    the main for preprocessing.py
    '''

poslines = []
neglines = []

stopwords= open(r'stopwords.txt', 'r').read().splitlines()
dataset= open('training_set.csv', 'r')

dataset.readline()

poslines=[]
neglines=[]

for data in dataset:
    data.lower()
    datalines = data.split(",")[1].strip('"').split(' ')
    DataClass = data.split(",")[0]
    #tokenizing the sentence
    if int(DataClass)==0:
        poslines.append(datalines)  
    if int(DataClass)==1:
        neglines.append(datalines)
    else:
        continue
print "the total positive and negative words are :", len(poslines), len(neglines)
#printing the total number of sentence in the training set
poslineedited = []
neglinesedited = []


#there is a total of 6397 positives and negatives.
poslinesTrain= poslines[:3201]
neglinesTrain= neglines[:3196]

priorknowledgepo = []
priorknowledgeneg = []

priorknowledgeneg= 3196/ 6397
priorknowledgepo = 3201/ 6397

#poslinesTest= poslines[N:]
#neglinesTest= neglines[N:]
stemmer = PorterStemmer()
model = open('model_file.csv', 'w')

#create the train set and the test set by attaching labels to text to form a
#list of tuples (sentence, label). Labels are 1 for positive, -1 for negative
trainset= [(x,1) for x in poslinesTrain] + [(x,-1) for x in neglinesTrain]
poswords={} #this dictionary will store counts for every word in positives
negwords={} #and negatives
for line,label in trainset: #for every sentence and its label
    words= getwords(line)

    for word in words: #for every word in the sentence   
        word.lower()     
        #increment the counts for this word based on the label
        #the .get(x, 0) method returns the current count for word 
        #x, of 0 if the word is not yet in the dictionary
        if label==1: poswords[word]= poswords.get(word, 0) + 1
        if label==-1: negwords[word]= negwords.get(word, 0) + 1
positivewordlist = open(r'positive-words.txt', 'r').read().splitlines()
negativewordlist = open(r'negative-words.txt', 'r').read().splitlines()

#evaluate the test set
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
        model.write("word:" +str(word) + ",")
        model.write("Positive probablity: " + str(totpos)+ ",")
        model.write("Negative probablity: "+str(totneg)+ '\n')
        #increment our score counter for each class, based on this word
