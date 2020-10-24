def LD_Recursive(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD_Recursive(s[:-1], t)+1,
               LD_Recursive(s, t[:-1])+1, 
               LD_Recursive(s[:-1], t[:-1]) + cost])

    return res

def LD_Iter(word1, word2, costDeletion, costAddition, costSubstiution):
    n = len(word1)+1
    m = len(word2)+1
    
    matrix = [None] * n
    
    for i in range(n):
        matrix[i] = [None] * m
        for j in range(m):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
            else:
                cost1 = matrix[i-1][j] + costAddition
                cost2 = matrix[i][j-1] + costDeletion
                cost3 = matrix[i-1][j-1] + (0 if word1[i-1] == word2[j-1] else costSubstiution);
                matrix[i][j] = min(cost1, cost2, cost3)
    
    return matrix[n-1][m-1]
    

word1 = "intent"
word2 = "execute"
print("MED between " + word1 + " and " + word2 + " is: " + str(LD_Iter(word1, word2, 2, 2, 1)))
print("MED between " + word1 + " and " + word2 + " is: " + str(LD_Recursive(word1, word2)))
