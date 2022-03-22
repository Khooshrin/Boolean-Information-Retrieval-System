import numpy as np, glob, re,os, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.metrics.distance import edit_distance
nltk.download('words')
from nltk.corpus import words

class Node:
    def __init__(self ,DocID, freq = None):
        self.freq = freq
        self.doc = DocID
        self.nextval = None
    
class LinkedList:
    def __init__(self ,head = None):
        self.head = head

def uniqueWordFreq(doc):
    uniqueWords = []
    freq = {}
    for word in doc:
        if word not in uniqueWords:
            ps.stem(word)
            lemmatizer.lemmatize(word)
            uniqueWords.append(word)
    for word in uniqueWords:
        freq[word] = doc.count(word)
    return freq

def rot(str,n):
    return str[n:]+str[:n]

Stopwords = set(stopwords.words('english'))
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
correctSpelling=words.words()

wordsInDocs = {}
docFolder = 'C:/Users/KHOOSHRIN/Documents/Python Programs/Data Set Files/*'
DocID = 1
fileIndex = {}
for file in glob.glob(docFolder):
    fname = file
    file = open(file , "r")
    doc = file.read()
    regex = re.compile('[^a-zA-Z\s]')
    doc = re.sub(regex,'',doc)
    words = word_tokenize(doc)
    words = [word for word in words if word not in Stopwords]
    words = [word.lower() for word in words]
    words = [ps.stem(word) for word in words]
    words = [lemmatizer.lemmatize(word) for word in words]
    wordsInDocs.update(uniqueWordFreq(words))
    fileIndex[DocID] = os.path.basename(fname)
    DocID = DocID + 1
    
uniqueWords = set(wordsInDocs.keys())


wordLinkedList = {}
permuterm = {}
termPermuterm={}
for word in uniqueWords:
    wordLinkedList[word] = LinkedList()
    wordLinkedList[word].head = Node(1,Node)
DocID = 1
for file in glob.glob(docFolder):
    file = open(file, "r")
    doc = file.read()
    regex = re.compile('[^a-zA-Z\s]')
    doc = re.sub(regex,'',doc)
    words = word_tokenize(doc)
    words = [word for word in words if word not in Stopwords]
    words = [word.lower() for word in words]
    words = [ps.stem(word) for word in words]
    words = [lemmatizer.lemmatize(word) for word in words]
    wordsInDocs=uniqueWordFreq(words)
    for word in wordsInDocs.keys():
        current = wordLinkedList[word].head
        while current.nextval is not None:
            current = current.nextval
        current.nextval = Node(DocID ,wordsInDocs[word])
        for i in range(len(word+"$"),0,-1):
            pterm = rot(word+"$",i)
            uniqueWords.add(pterm)
            wordLinkedList[pterm] = wordLinkedList[word]
    DocID = DocID + 1


booleanQuery = input('Enter your query:')
regex = re.compile('[^a-zA-Z*\s]')
booleanQuery = re.sub(regex,'',booleanQuery)
query = booleanQuery.split()
queryWords = []
booleanWords = []
for word in query:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":          
        queryWords.append(word.lower())
    else:
        booleanWords.append(word.lower())

queryWords = [ps.stem(word) for word in queryWords]
queryWords = [lemmatizer.lemmatize(word) for word in queryWords]
queryWords = [word+"$" for word in queryWords]


countQueryWords = 0
for word in queryWords:
        for i in range(len(word),0,-1):
            pterm = rot(word,i)
            if pterm[-1]=='*':
                queryWords.remove(word)
                queryWords.insert(countQueryWords,pterm)
        countQueryWords = countQueryWords + 1
print(queryWords)

TermDocumentValue = []
TermDocumentIncidenceMatrix = []
PermuTermIncidenceMatrix = []

for word in queryWords:
    if word[-1] == '*':
      TermDocumentValue = [0] * len(fileIndex)
      for uniqueWord in uniqueWords:
          if uniqueWord.lower().startswith(word[:len(word)-1]):
            doc = wordLinkedList[uniqueWord].head
            while doc.nextval is not None:
                TermDocumentValue[doc.nextval.doc - 1] = 1
                doc = doc.nextval
            TermDocumentIncidenceMatrix.append(TermDocumentValue)
    elif word.lower() in uniqueWords:
        TermDocumentValue = [0] * len(fileIndex)
        doc = wordLinkedList[word].head
        while doc.nextval is not None:
            TermDocumentValue[doc.nextval.doc - 1] = 1
            doc = doc.nextval
        TermDocumentIncidenceMatrix.append(TermDocumentValue)

for word in booleanWords:
    list1 = TermDocumentIncidenceMatrix[0]
    list2 = TermDocumentIncidenceMatrix[1]
    if word == "and":
        res = [w1 & w2 for (w1,w2) in zip(list1,list2)]
        TermDocumentIncidenceMatrix.remove(list1)
        TermDocumentIncidenceMatrix.remove(list2)
        TermDocumentIncidenceMatrix.insert(0, res);
    elif word == "or":
        res = [w1 | w2 for (w1,w2) in zip(list1,list2)]
        TermDocumentIncidenceMatrix.remove(list1)
        TermDocumentIncidenceMatrix.remove(list2)
        TermDocumentIncidenceMatrix.insert(0, res);
    elif word == "not":
        res = [not w1 for w1 in list2]
        res = [int(b == True) for b in res]
        TermDocumentIncidenceMatrix.remove(list2)
        TermDocumentIncidenceMatrix.remove(list1)
        res = [w1 & w2 for (w1,w2) in zip(list1,res)]
        TermDocumentIncidenceMatrix.insert(0, res);

result = TermDocumentIncidenceMatrix[0]
cnt = 1
for index in result:
    if index == 1:
        print(fileIndex[cnt])
    cnt = cnt+1
