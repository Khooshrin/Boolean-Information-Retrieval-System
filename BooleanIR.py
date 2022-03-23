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
    
    def __init__(self ,DocID, freq = None):     #Constructor to initialize node
        self.freq = freq                        #with frequency of a term freq in 
        self.doc = DocID                        #a particular document having DocID as the document ID
        self.nextval = None                     #the next pointer points to NULL
    
class LinkedList:

    """ Class to store the frequency of the term in a
        particular document ID only if the document
        contains the word at least once """
    
    def __init__(self ,head = None):            #Constructor to define a linked list
        self.head = head                        #in which the head points to the first element of the linked list

def uniqueWordFreq(doc):

    """ Function to find all the unique words in the document
        passed as a parameter and then calculate the frequency
        of the unique word in the document and returns it """
    
    uniqueWords = []                            #List that contains the unique words across all documents and their permuterms
    freq = {}                                   #List that contains the frequency of the corresponding word in unique words
    for word in doc:
        if word not in uniqueWords:
            ps.stem(word)                       #Performing stemming operation using PorterStemmer in nltk
            lemmatizer.lemmatize(word)          #Performing lemmatization operation using WordNetLemmatizer in nltk
            uniqueWords.append(word)            #Adding a word to the uniqueWords list if it did not exist in the list
    for word in uniqueWords:
        freq[word] = doc.count(word)            #Calculating the frequency of a term in the document
    return freq

def rot(str,n):

    """ Function to rotate the string passed as a parameter
        by n places and then return it. It is used to
        calculate all the permuterm combinations possible
        of the string that is passed as a parameter. """
    
    return str[n:]+str[:n]                      #Returns the string after reforming right rotation n times

Stopwords = set(stopwords.words('english'))     #Creating a list of all the stop words in the english language
ps = PorterStemmer()                            #Defining the stemmer to use it to perform stemming on the words in the document and the query
lemmatizer = WordNetLemmatizer()                #Defining the lemmatizer to use it to perform lemmatization on the words in the document and the query

""" Iterate through the list of documents in the folder to find
    all the unique words present after deleting numbers and
    special characters. Ignore the stopwords while finding the
    unique words. Creates a dictionary of the document ID and
    the respective document name. """

wordsInDocs = {}                                #Dictionary to store the unique words in all the douments as the key and their frequecies as the value
docFolder = 'C:/Users/KHOOSHRIN/Documents/PythonPrograms/DataSetFiles/*'        #Path for all the documents in the retrieval system
DocID = 1
fileIndex = {}                                  #Dictionary to store th file index number as the key and the file name as the frequency
for file in glob.glob(docFolder):               #Iterating through all files in the folder
    fname = file                                #To store the name of the file
    file = open(file , "r")                     #Granting only reading permissions
    doc = file.read()                           #Reading all the text in the docoument
    regex = re.compile('[^a-zA-Z\s]')           #Creating a regex to remove all characters except letters and whitespaces from the document
    doc = re.sub(regex,'',doc)                  #Removing all digits and special characters from the document
    words = word_tokenize(doc)                  #Tokenizing the words in the document to get all the unique words in the document
    words = [word for word in words if word not in Stopwords]       #Eliminating the stopwords from the document
    words = [word.lower() for word in words]                        #Converting all the words to lower case to maintain uniformity
    words = [ps.stem(word) for word in words]                       #Stemming all the unique non-stopwords in the document
    words = [lemmatizer.lemmatize(word) for word in words]          #Lemmatizing all the unique non-stopwords in the document
    wordsInDocs.update(uniqueWordFreq(words))                       #Invoking function to calculate frequency of the unique words and the modify it in the dictionary
    fileIndex[DocID] = os.path.basename(fname)                      #Storing the corresponding file name and document ID in a dictionary
    DocID = DocID + 1                           #Incrementing to the next document ID
    
uniqueWords = set(wordsInDocs.keys())           #Set which stores all the unique words and their permuterm combinations

""" Iterate through the list of unique words stemming and lemmatizing
    each termto create the linked list for each term and then find all
    the permuterms for the given term and copy the same linked list
    for the permuterms. This helps in wildcard query handling. """

wordLinkedList = {}                             #Linked list of each term in the document which stores the Document ID of the document
#permuterm = {}
#termPermuterm={}
for word in uniqueWords:                        #Iterating through all the unique words across the documents
    wordLinkedList[word] = LinkedList()         #Initialising a linked list for each unique word
    wordLinkedList[word].head = Node(1,Node)
DocID = 1
for file in glob.glob(docFolder):               #Iterating through all files in the folder
    file = open(file, "r")                      #To store the name of the file
    doc = file.read()                           #Reading all the text in the docoument
    regex = re.compile('[^a-zA-Z\s]')           #Creating a regex to remove all characters except letters and whitespaces from the document
    doc = re.sub(regex,'',doc)                  #Removing all digits and special characters from the document
    words = word_tokenize(doc)                  #Tokenizing the words in the document to get all the unique words in the document
    words = [word for word in words if word not in Stopwords]       #Eliminating the stopwords from the document
    words = [word.lower() for word in words]                        #Converting all the words to lower case to maintain uniformity
    words = [ps.stem(word) for word in words]                       #Stemming all the unique non-stopwords in the document
    words = [lemmatizer.lemmatize(word) for word in words]          #Lemmatizing all the unique non-stopwords in the document
    wordsInDocs=uniqueWordFreq(words)                               #Invoking function to calculate frequency of the unique words and the modify it in the dictionary
    for word in wordsInDocs.keys():                                 #Iterating through each unique word to create its linked list
        current = wordLinkedList[word].head                         #Initialising pointer to point at the head of the linked list for that unique word
        while current.nextval is not None:                          #Traversing through the nodes to reach the last node
            current = current.nextval
        current.nextval = Node(DocID ,wordsInDocs[word])            #Adding a node at the end indictaing the document ID and the frequency of the word in that document ID
        for i in range(len(word+"$"),0,-1):                         #Iterating through the length of the unique word
            pterm = rot(word+"$",i)                                 #Invoking function to create the permuterm and then store it
            uniqueWords.add(pterm)                                  #Adding all combinations of the permuterm to the list of unique words
            wordLinkedList[pterm] = wordLinkedList[word]            #Creating a linked list for the the permuterms of the unique word which is the same linked list as the unique word
    DocID = DocID + 1                           #Incrementing to the next document ID

""" Accepting query as input from the user and splitting
    the query into boolean words (and, or, not) and
    query words(all other words with the exception of the
    three boolean words). """

booleanQuery = input('Enter your query:')           #Prompting user to enter a query and then accepting and storing the query entered by the user
regex = re.compile('[^a-zA-Z*\s]')                  #Creating a regex to remove all characters except letters, wildcard characters and whitespaces from the query
booleanQuery = re.sub(regex,'',booleanQuery)        #Removing all digits and special characters except '*' from the query
query = booleanQuery.split()                        #Tokenizing the words in the query to get all the unique words in the query
queryWords = []                                     #List to store the query words in the query entered by the user
booleanWords = []                                   #List to store the boolean words (and, or, not) entered by the user in the query
for word in query:                                  #Iterating through all the words in the query
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":    #If the word is not a boolean word       
        queryWords.append(word.lower())             #Add the word to the list of query words
    else:
        booleanWords.append(word.lower())           #Add the word to the list of boolean words

""" Performing Stemming and Lemmatization on each query
    word and then add a $ to the end of the word indicating
    it is the end of the word. """

queryWords = [ps.stem(word) for word in queryWords]                 #Stemming all the query words in the query
queryWords = [lemmatizer.lemmatize(word) for word in queryWords]    #Lemmatizing all the query words in the query
queryWords = [word+"$" for word in queryWords]                      #Adding a '$' at the end of the query word signifying the end of the query word

""" Performing a spell check and correction on all the query
    words if the spelling is wrong. This is done by comparing
    the edit distance between the query words with all the
    unique words across all the documents. The word is then
    replaced by the word which has the minimum edit distance.
    If the query word exists in the documents, the minimum edit
    distance is zero and the word remains unchanged. """


countQueryWords = 0                             #Counter to count the number of query words
for word in queryWords:                         #Iterating through all the words in query words
    distance = -1                               #int variable to store edit distance
    minDistance = sys.maxsize                   #int variable to store minimum edit distance
    minWord = ""                                #string variable to store word having the minmum edit distance
    for w in uniqueWords:                       #Iterating through all the words in unique words
        distance = edit_distance(word,w)        #Calculate the edit distance between the current query word and every word in unique words
        if distance<minDistance :               #Relacing the minimum word and minumum edit distance
            minDistance = distance              #if the calculated edit distnace is smaller
            minWord = w
    queryWords.remove(word)                     #Removing the misspelt word from the list of query words
    word = minWord                              #The rightly spelt word is the word which will have minimum edit distance value from the orginial word so it is replaced
    queryWords.insert(countQueryWords,word)     #The rightly spelt word is added into the query words list
    countQueryWords = countQueryWords + 1       #Incrementing the count of query words

""" In case the query is a wildcard query, we find its permuterms
    by performing rotations until '*' is the last character. We
    then replace the query word with its perumterm that has '*'
    as the last character which helps in wildcard query processing. """

countQueryWords = 0                                             #Counter to count the number of query words
for word in queryWords:                                         #Iterating through all the words in query words
        for i in range(len(word),0,-1):                         #Iterating throught the length of the string to create the permuterms
            pterm = rot(word,i)                                 #Invoking function to create the permuterm and then store it
            if pterm[-1]=='*':                                  #Checking if the permuterms of the query word contains '*'as the last character
                queryWords.remove(word)                         #If true then the orginal word is removed
                queryWords.insert(countQueryWords,pterm)        #It is replaced by its permuterm having '*' as the last character
        countQueryWords = countQueryWords + 1                   #Incrementing the count of query words

TermDocumentValue = []                                          #List to store the vector of each term across all documents
TermDocumentIncidenceMatrix = []                                #List to store the vectors of all terms across all documents therby making a matrix
#PermuTermIncidenceMatrix = []

""" The term document incidence matrix is created by first creating
    the vector for that term across all documents using the linked
    list created for that term. The vector which is in the form of
    list is then added to another list which contains the vectors
    for all query words. In this way, the term document incidence
    matrix is created for all the query terms. """

for word in queryWords:                                                 #Iterating through all the words in query words
    if word[-1] == '*':                                                 #Checking if the query word contains '*'as the last character
      TermDocumentValue = [0] * len(fileIndex)                          #Initialising the vector for the query to term to be zero for all documents
      for uniqueWord in uniqueWords:                                    #Iterating through all the words in unique words
          if uniqueWord.lower().startswith(word[:len(word)-1]):         #Checking if there is a match between the wildcard query containing permuterm and a unique word
            doc = wordLinkedList[uniqueWord].head                       #If true then a pointer which points to the head of the linked list of all such matching unique words is created
            while doc.nextval is not None:                              #If the frequency in the document is not equal to None 
                TermDocumentValue[doc.nextval.doc - 1] = 1              #then replace the initialised 0 by 1 as it exists in that document
                doc = doc.nextval                                       #Incrementing to the next node in a linked list
            TermDocumentIncidenceMatrix.append(TermDocumentValue)       #Adding the vector to the incidence matrix
    elif word.lower() in uniqueWords:                                   #If the word does not contain '*'as the last character, it is checked if it is present in unique words list
        TermDocumentValue = [0] * len(fileIndex)                        #Initialising the vector for the query to term to be zero for all documents
        doc = wordLinkedList[word].head                                 #Pointer which points to the head of the linked list of the word
        while doc.nextval is not None:                                  #If the frequency in the document is not equal to None
            TermDocumentValue[doc.nextval.doc - 1] = 1                  #then replace the initialised 0 by 1 as it exists in that document
            doc = doc.nextval                                           #Incrementing to the next node in a linked list
        TermDocumentIncidenceMatrix.append(TermDocumentValue)           #Adding the vector to the incidence matrix

""" Applies the unary not operator on the relevant query term.
    This is used to invert the values present in the vector
    for that term. The uninverted vector is then deleted from
    incidence matrix and the inverted vector is inserted into
    it at the same index. """

countQueryWords = 0                                                    #Counter to count the number of query words
for word in booleanWords:                                              #Iterating through all the words in boolean words
    if word == "not" :                                                 #If the boolean term is not
        #print(countQueryWords)
        list1 = TermDocumentIncidenceMatrix[countQueryWords]           #A copy is made of the vector of the query word on which the not operator is to be applied
        res = []                                                       #To store the vector after the not operation has been carried out
        for doc in list1 :                                             #for every int value in the vector list
            if doc == 0 :                                              #if the value is zero
                res.append(1)                                          #the value 1 is added to the resultant vector
            else :
                res.append(0)                                          #else the value 0 is added to the resultant vector
        TermDocumentIncidenceMatrix.remove(list1)                      #Remove the univerted vector from the incidence matrix
        TermDocumentIncidenceMatrix.insert(countQueryWords, res)       #Add the inverted vector at the same index position
        TermDocumentValue = res
        booleanWords.remove(word)                                      #Removing the not from the list of boolean words as its operation has been carried out
    else :
        countQueryWords = countQueryWords + 1                          #Incrementing the count of query words

""" Used to perform the 'and' and 'or' boolean query operations.
    Two lists are created which store the first 2 rows of the
    incidence matrix. Depending on the boolean word either
    bitwise and operation or bitwise or operation is applied
    on the query word vectors. The result is then replaced as
    the first row of the incidence matrix and the second row is deleted. """

for word in booleanWords:                                           #Iterating through all the words in boolean words
    list1 = TermDocumentIncidenceMatrix[0]                          #In a separate list store the first vector in the incidence matrix
    list2 = TermDocumentIncidenceMatrix[1]                          #In a separate list store the second vector in the incidence matrix
    if word == "and":                                               #Check if the boolean word entered is and
        res = [w1 & w2 for (w1,w2) in zip(list1,list2)]             #Performing bitwise and on the two vectors and storing their result
        TermDocumentIncidenceMatrix.remove(list1)                   #Removing the first vector from the incidence matrix
        TermDocumentIncidenceMatrix.remove(list2)                   #Removing the second vector from the incidence matrix
        TermDocumentIncidenceMatrix.insert(0, res)                  #Inserting the resultant vector at the first position
    elif word == "or":                                              #Check if the boolean word entered is or
        res = [w1 | w2 for (w1,w2) in zip(list1,list2)]             #Performing bitwise or on the two vectors and storing their result
        TermDocumentIncidenceMatrix.remove(list1)                   #Removing the first vector from the incidence matrix
        TermDocumentIncidenceMatrix.remove(list2)                   #Removing the second vector from the incidence matrix
        TermDocumentIncidenceMatrix.insert(0, res)                  #Inserting the resultant vector at the first position

""" The final result is calculated and stored in the first row
    of the incidence matrix. This list is then iterated through
    and whenever the value is 1, it implies that the document
    satisfies the given boolean query and its name is displayed.
    If the value is 0, it skips to the value of the next document
    in the resultant vector. """

result = TermDocumentIncidenceMatrix[0]       #Storing the resultant vector in a list
DocID = 1                                     #int variable to store document ID
for index in result:                          #for every int value in the resultant vector list
    if index == 1:                            #if the value is 1 then that document satifies the boolean query entered
        print(fileIndex[DocID])               #Name of the file is printed out
    DocID = DocID+1
