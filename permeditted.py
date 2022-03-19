import os
import numpy as np, glob, re,os, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
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
        word=ps.stem(word)
        if word not in uniqueWords:
            uniqueWords.append(word)
    for word in uniqueWords:
        freq[word] = doc.count(word)
    return freq

with open('Stopwords.txt') as f:
    for line in f:
        Stopwords = line.split(", ")

wordsInDocs = {}
docFolder = 'C:\\Users\\Anshul\\Downloads\\dataset\*'
DocID = 1
fileIndex = {}
#using another method for opening files
for file in glob.glob(docFolder):
            fname = file
            file = open(file , "r")
            doc = file.read()
            regex = re.compile('[^a-zA-Z\s]')
            doc = re.sub(regex,'',doc)
            words = word_tokenize(doc)
            for word in words:
                if word not in Stopwords:
                    word=ps.stem(word)
                    word.lower()
                    words.append(word)
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
    words=ps.stem(word)
    words = [word.lower() for word in words if word not in Stopwords]
    wordsInDocs=uniqueWordFreq(words)
    for word in wordsInDocs.keys():
        current = wordLinkedList[word].head
        while current.nextval is not None:
            current = current.nextval
        current.nextval = Node(DocID ,wordsInDocs[word])
    DocID = DocID + 1


#add all the permuterms in a separate doc

def rot(str,n):
    return str[n:]+str[:n]

f = open("PermutermIndex.txt","w")
for key in uniqueWords:
    dockey = key + "$"
    for i in range(len(dockey),0,-1):
        out = rot(dockey,i)
        f.write(out)
        f.write(" ")
        f.write(key)
        f.write("\n")
f.close()
