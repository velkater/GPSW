
# coding: utf-8

# # Zobecněný pseudopalindromický uzávěr

# ## Funkce pro vytvoření zobecněného pseudopalindromického uzávěru

# In[1]:

def isPal(seq):
    "kontroluje jestli řetězec je palindrom"
    l = len(seq)
    if l == 1:
        return(True)
    for x in range(0, l//2):
        if seq[x] != seq[l-1-x]:
            return(False)
    return(True)

def isEpal(seq):
    "kontroluje jestli řetězec je pseudopalindrom"
    l = len(seq)
    if l%2 == 1:
        return(False)
    for x in range(0, l//2):
        if seq[x] == seq[l-1-x]:
            return(False)
    return(True)


# In[15]:

def makePalClosure (seq):
    "udělá z řetězce palindromický uzávěr"
    if isPal(seq) == True:
        return(seq)
    i = 1
    while isPal(seq[i:]) != True:
        i = i+1
    #print("    {0} nejdelší palindromický uzávěr : {1}".format(seq,seq[i:]))
    print("    délka nejdelší palindromický uzávěr : {0}".format(len(seq[i:])))
    closure = seq + seq[i-1::-1]
    return(closure)

def makeEpalClosure (seq):
    "udělá z řetězce pseudopalindromický uzávěr"
    if isEpal(seq) == True:
        return(seq)
    i = 1
    while isEpal(seq[i:]) != True:
        i = i+1
    print("    {0} nejdelší pseudopalindromický uzávěr : {1}".format(seq,seq[i:]))
    closure = seq
    pref = seq[i-1::-1]
    for letter in pref:
        if letter == "0":
            closure = closure + "1"
        if letter == "1":
            closure = closure + "0"
    return(closure)


# In[3]:

def makeWord(delta, theta, steps, seed = ""):
    "vytvoří slovo pomocí řídící posloupnosti a posloupnosti uzávěrů"
    w = seed
    for step in range(0,steps):
        w = w + delta[step]
        if theta[step] == "R":
            w = makePalClosure(w)
        if theta[step] == "E":
            w = makeEpalClosure(w)
        print("w{0} = {1}".format(step+1,w))
    return(w)


# ## Příklad 1

# $\Delta = 1^{\omega}$, $\Theta = (EERR)^{w}$

# In[4]:

n = 30
delta = n * "1"
theta = n * "EERR"
print(delta)
print(theta)

word = makeWord(delta, theta, 10)
f = open('gen.txt', 'w')
f.write(word)
f.close()
print(len(word))


# ## Příklad 2

# $\Delta = (10)^{\omega}$, $\Theta = (R)^{w}, w_{0}=0011010$

# In[5]:

n = 200
delta = n * "10"
theta = n * "R"
print(delta)
print(theta)

word = makeWord(delta, theta, 10, "00110100")
f = open('gen2.txt', 'w')
f.write(word)
f.close()
print(len(word))


# In[28]:

n=500
delta = n * "1"
theta = n * "R"
print(delta)
print(theta)

word = makeWord(delta, theta, 50, "000100111000")
f = open('gen3.txt', 'w')
f.write(word)
f.close()
print(len(word))


# In[30]:

Sword = ""
for i in range(0,len(word)-1):
    Sword += str((int(word[i]) + int(word[i+1])) %2)
print(Sword)
print(len(Sword))
f = open('gen4.txt', 'w')
f.write(Sword)
f.close()


# In[ ]:




# In[ ]:



