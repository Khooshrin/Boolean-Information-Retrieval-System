import numpy as np, glob, re,os, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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
            uniqueWords.append(word)
    for word in uniqueWords:
        freq[word] = doc.count(word)
    return freq

Stopwords = set(stopwords.words('english'))

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
    words = [word.lower() for word in words if word not in Stopwords]
    wordsInDocs.update(uniqueWordFreq(words))
    fileIndex[DocID] = os.path.basename(fname)
    DocID = DocID + 1
    
uniqueWords = set(wordsInDocs.keys())

wordLinkedList = {}
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
    words = [word.lower() for word in words if word not in Stopwords]
    wordsInDocs=uniqueWordFreq(words)
    for word in wordsInDocs.keys():
        current = wordLinkedList[word].head
        while current.nextval is not None:
            current = current.nextval
        current.nextval = Node(DocID ,wordsInDocs[word])
    DocID = DocID + 1


query = input('Enter your query:')
query = word_tokenize(query)
queryWords = []
booleanWords = []
for word in query:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        booleanWords.append(word.lower())
    else:
        queryWords.append(word.lower())

TermDocumentValue = []
TermDocumentIncidenceMatrix = []
for word in (booleanWords):
    if word.lower() in uniqueWords:
        TermDocumentValue = [0] * len(fileIndex)
        doc = wordLinkedList[word].head
        print(word)
        while doc.nextval is not None:
            TermDocumentValue[doc.nextval.doc - 1] = 1
            doc = doc.nextval
        TermDocumentIncidenceMatrix.append(TermDocumentValue)
for word in queryWords:
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
