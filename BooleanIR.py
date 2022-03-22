import numpy as np, glob, re, os, nltk, sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.metrics.distance import edit_distance

class Node:

    """ Class which defines a node of the linked list.
        Each node has a document ID along with the frequency
        which stores the frequency of the term in the document
        with the respective document ID """
    
    def __init__(self ,DocID, freq = None):
        self.freq = freq
        self.doc = DocID
        self.nextval = None
    
class LinkedList:

    """ Class to store the frequency of the term in a
        particular document ID only if the document
        contains the word at least once """
    
    def __init__(self ,head = None):
        self.head = head

def uniqueWordFreq(doc):

    """ Function to find all the unique words in the document
        passed as a parameter and then calculate the frequency
        of the unique word in the document and returns it """
    
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

    """ Function to rotate the string passed as a parameter
        by n places and then return it. It is used to
        calculate all the permuterm combinations possible
        of the string that is passed as a parameter. """
    
    return str[n:]+str[:n]

Stopwords = set(stopwords.words('english'))
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

""" Iterate through the list of documents in the folder to find
    all the unique words present after deleting numbers and
    special characters. Ignore the stopwords while finding the
    unique words. """

wordsInDocs = {}
docFolder = 'C:/Users/KHOOSHRIN/Documents/PythonPrograms/DataSetFiles/*'
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

""" Iterate through the list of unique words stemming and lemmatizing
    each termto create the linked list for each term and then find all
    the permuterms for the given term and copy the same linked list
    for the permuterms. This helps in wildcard query handling. """

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

""" Accepting query as input from the user and splitting
    the query into boolean words (and, or, not) and
    query words(all other words with the exception of the
    three boolean words). """

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

""" Performing Stemming and Lemmatization on each query
    word and then add a $ to the end of the word indicating
    it is the end of the word. """

queryWords = [ps.stem(word) for word in queryWords]
queryWords = [lemmatizer.lemmatize(word) for word in queryWords]
queryWords = [word+"$" for word in queryWords]

""" Performing a spell check and correction on all the query
    words if the spelling is wrong. This is done by comparing
    the edit distance between the query words with all the
    unique words across all the documents. The word is then
    replaced by the word which has the minimum edit distance.
    If the query word exists in the documents, the minimum edit
    distance is zero and the word remains unchanged. """


countQueryWords = 0
for word in queryWords:
    distance = -1
    minDistance = sys.maxsize
    minWord = ""
    for w in uniqueWords:
        distance = edit_distance(word,w)
        if distance<minDistance :
            minDistance = distance
            minWord = w
    queryWords.remove(word)
    word = minWord
    queryWords.insert(countQueryWords,word)
    countQueryWords = countQueryWords + 1

""" In case the query is a wildcard query, we find its permuterms
    by performing rotations until '*' is the last character. We
    then replace the query word with its perumterm that has '*'
    as the last character which helps in wildcard query processing. """

countQueryWords = 0
for word in queryWords:
        for i in range(len(word),0,-1):
            pterm = rot(word,i)
            if pterm[-1]=='*':
                queryWords.remove(word)
                queryWords.insert(countQueryWords,pterm)
        countQueryWords = countQueryWords + 1

TermDocumentValue = []
TermDocumentIncidenceMatrix = []
PermuTermIncidenceMatrix = []

""" The term document incidence matrix is created by first creating
    the vector for that term across all documents using the linked
    list created for that term. The vector which is in the form of
    list is then added to another list which contains the vectors
    for all query words. In this way, the term document incidence
    matrix is created for all the query terms. """

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

""" Applies the unary not operator on the relevant query term.
    This is used to invert the values present in the vector
    for that term. The uninverted vector is then deleted from
    incidence matrix and the inverted vector is inserted into
    it at the same index. """

countQueryWords = 0
for word in booleanWords:
    if word == "not" :
        print(countQueryWords)
        list1 = TermDocumentIncidenceMatrix[countQueryWords]
        res = []
        for doc in list1 :
            if doc == 0 :
                res.append(1)
            else :
                res.append(0)
        TermDocumentIncidenceMatrix.remove(list1)
        TermDocumentIncidenceMatrix.insert(countQueryWords, res)
        TermDocumentValue = res
        booleanWords.remove(word)
    else :
        countQueryWords = countQueryWords + 1

""" Used to perform the 'and' and 'or' boolean query operations.
    Two lists are created which store the first 2 rows of the
    incidence matrix. Depending on the boolean word either
    bitwise and operation or bitwise or operation is applied
    on the query word vectors. The result is then replaced as
    the first row of the incidence matrix and the second row is deleted. """

for word in booleanWords:
    list1 = TermDocumentIncidenceMatrix[0]
    list2 = TermDocumentIncidenceMatrix[1]
    if word == "and":
        res = [w1 & w2 for (w1,w2) in zip(list1,list2)]
        TermDocumentIncidenceMatrix.remove(list1)
        TermDocumentIncidenceMatrix.remove(list2)
        TermDocumentIncidenceMatrix.insert(0, res)
    elif word == "or":
        res = [w1 | w2 for (w1,w2) in zip(list1,list2)]
        TermDocumentIncidenceMatrix.remove(list1)
        
        TermDocumentIncidenceMatrix.remove(list2)
        TermDocumentIncidenceMatrix.insert(0, res)

""" The final result is calculated and stored in the first row
    of the incidence matrix. This list is then iterated through
    and whenever the value is 1, it implies that the document
    satisfies the given boolean query and its name is displayed.
    If the value is 0, it skips to the value of the next document
    in the resultant vector. """

result = TermDocumentIncidenceMatrix[0]
cnt = 1
for index in result:
    if index == 1:
        print(fileIndex[cnt])
    cnt = cnt+1
