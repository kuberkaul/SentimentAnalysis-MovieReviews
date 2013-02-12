from math import log
from porter import PorterStemmer

poslines = []
neglines = []

stopwords= open(r'stopwords.txt', 'r').read().splitlines()
dataset= open('training_set.csv', 'r')

dataset.readline()

poslines=[]
neglines=[]

for data in dataset:
    datalines = data.split(",")[1].strip('"').split(' ')
    DataClass = data.split(",")[0]
    if int(DataClass)==0:
        poslines.append(datalines)  
    if int(DataClass)==1:
        neglines.append(datalines)
        
print "the total positive and negative words are :", len(poslines), len(neglines)


#there is a total of 6397 positives and negatives.
#lets take first N as training set, and then testset for validation
N= 6397
poslinesTrain= poslines[:3201]
neglinesTrain= neglines[:3196]
#poslinesTest= poslines[N:]
#neglinesTest= neglines[N:]
model = open('model_file.csv', 'w')
#create the train set and the test set by attaching labels to text to form a
#list of tuples (sentence, label). Labels are 1 for positive, -1 for negative
#if you don't get this look up list comprehensions in Python
trainset= [(x,1) for x in poslinesTrain] + [(x,-1) for x in neglinesTrain]

#initialize the stemmer object for (optional) stemming later
stemmer= PorterStemmer()


def getwords(sentence):
    
    #this method returns important words from a sentence as list
    #w= sentence.split()
    w = sentence
    #remove all things that are 1 or 2 characters long (punctuation)
    w= [x for x in w if len(x)>3]
    
    #get rid of all stop words
    w= [x for x in w if not x in stopwords]
    
    #stem each word
    #w= [stemmer.stem(x,0,len(x)-1) for x in w]
    
    #add bigrams
    w= w + [w[i]+' '+w[i+1] for i in range(len(w)-1)]
    
    #get rid of duplicates by converting to set and back to list
    #this works because sets dont contain duplicates
    w= list(set(w))
    
    return w


#compute frequency of every word in the train set. We will want common words
#to count for less in our later analysis. Also while we're at it,
#build an array of processed words called trainfeatures for training reviews.
freq={}
trainfeatures= []
for line,label in trainset: #for every sentence and its label
    words= getwords(line)

    for word in words: #for every word in the sentence
        freq[word]= freq.get(word, 0) + 1   
        
    trainfeatures.append((words, label))
    
#evaluate the test set
testset= open('test_set.csv', 'r')
testset.readline()
#print testset
output = open("prediciton_file.csv", 'w') 

#    testdatalines = testdata.split()
Ntr= len(trainset)
print Ntr
wrong=0 #will store number of misslassifications
#for testdata in testset: #for each review in test set
#    print testdata
for testdata in testset:
    testwordssplit = testdata.split()
    testwords= getwords(testwordssplit)
    #print len(testwords)
    #we will store distances to all train reviews in this list as tuples
    #of (score, label). Later, we will sort by score and look at the labels
    results=[]
    

    #go over every review in train set and compute similarity
    for trainwords, trainlabel in trainfeatures:
   
    #find all words in common between these two sentences
        commonwords= [x for x in trainwords if x in testwords]
        
        #accumulate score for all overlaps. Common words count for less
        #and we achieve this by dividing by their frequency
        #the log() function squashes things down so that infrequent words
        #dont count for TOO much.
        score= 0.0
        for word in commonwords:
            score += log(Ntr/freq[word])
            model.write("word:" +str(word) + ",")
            model.write("Probablity: " + str(score))
   
        results.append((score, trainlabel))   
            #sort all similarities by their score, descending
    #print results
    results.sort(reverse=True)
            
    #look at top 5 results and do a majority vote (i.e. this is 5-NN classifier)
    toplab= [x[1] for x in results[:10]] #extract top 5 labels
    numones= toplab.count(1) #count number of ones
    numnegones= toplab.count(-1) #and negative ones
    if numnegones> numones:
        output.write("0," + testdata)
    else: 
        output.write("1," + testdata) #majority vote
output.close()

    