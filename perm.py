import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
#dummy code
#tokens is a list of keywords
with open('Stopwords.txt') as f:
    for line in f:
        stopwords = line.split(", ")
        
tokens = {}
documentID = 0
path = r"C:\Users\Anshul\Downloads\dataset"

for root, dirs, files in os.walk(path):
    for file in files:
        with open(os.path.join(path, file)) as f:
                documentID += 1
                line_tokens = []
                for line in f:
                    line_tokens = line.split(  )
                    for each in line_tokens:
                        if each not in stopwords:
                            each=ps.stem(each)
                            if each not in tokens:
                                tokens[each] = [documentID]
                            else:
                                tokens[each].append(documentID)

#add all the permuterms in a separate doc

def rot(str,n):
    return str[n:]+str[:n]

f = open("perm.txt","w")
keys = tokens.keys()
for key in sorted(keys):
    dockey = key + "$"
    for i in range(len(dockey),0,-1):
        out = rot(dockey,i)
        f.write(out)
        f.write(" ")
        f.write(key)
        f.write("\n")
f.close()
