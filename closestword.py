# Correcting user queries to recieve the right answers using  minimum edit distance algorithm (Levenshtein distance)

# INCOMPLETE!! still needs to be coded

import numpy as np

def minEditDistance(target,source):

    #target - The correct/closest correct word
    #source - The given/inputted word

    #Build empty matrix of correct size

    target = [k for k in target]
    source = [k for k in source]

    solution = np.zeros((len(source), len(target)))

    solution[0] = [j for j in range (len(target))]
    solution[:,0] = [j for j in range(len(source))]

    #Adding in an anchor value

    if target[1] != source[1]:
        solution[1,1] = 2

    #Filling in the rest of the values

    #Through every column
    for c in range(1, len(target)):

        #Through every row
        for r in range (1, len(source)):

            #Not same letter
            if target[c] != source[r]:
                solution[r,c] = min(solution[r-1,c], solution[r,c-1]) + 1

            #Same letter
            else:
                solution[r,c] = solution[r-1, c-1]
            
        
    return solution 

#Levenshtein Distance is found in bottom right corner of each matrix
# 1 for each insertion, 1 for deletion and 2 for substitution

print(minEditDistance("#piano", "#pianos")) # 1 insert
print(minEditDistance("#piano", "#pian")) # 1 delete
print(minEditDistance("#piano", "#piand")) # 1 substitution
        
            







# Another possible implementation

# def levenshteinDistance(s1, s2):
#     if len(s1) > len(s2):
#         s1, s2 = s2, s1

#     distances = range(len(s1) + 1)
#     for i2, c2 in enumerate(s2):
#         distances_ = [i2+1]
#         for i1, c1 in enumerate(s1):
#             if c1 == c2:
#                 distances_.append(distances[i1])
#             else:
#                 distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
#         distances = distances_
#     return distances[-1] 




# Algo to find best match from a set of words


# distance = -1;
 
# for(words as word){  
#  lev = levenshtein(input, word);  
 

# Exact match found

#  if(lev == 0){  
#   closest = word;  
#   distance = 0;  
#   #No need to continue as an exact match is found
#   break;  
#  }  
 
# # if distance is less than the currently stored distance and it is less than our initial value
#  if(lev <= distance || distance < 0){
#   closest  = word;  
#   distance = lev;  
#  }

#  if (distance > 0) {
#   # Did you mean 'closest match'
# }