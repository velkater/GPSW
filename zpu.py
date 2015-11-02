
# coding: utf-8

# # Zobecněný pseudopalindromický uzávěr

# ## Funkce pro vytvoření zobecněného pseudopalindromického uzávěru

# In[9]:

import time


# In[2]:

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


# In[3]:

def makePalClosure (seq):
    "udělá z řetězce palindromický uzávěr"
    if isPal(seq) == True:
        return(seq)
    i = 1
    while isPal(seq[i:]) != True:
        i = i+1
    #print("    {0} nejdelší palindromický uzávěr : {1}".format(seq,seq[i:]))
    #print("    délka nejdelší palindromický uzávěr : {0}".format(len(seq[i:])))
    closure = seq + seq[i-1::-1]
    return(closure)

def makeEpalClosure (seq):
    "udělá z řetězce pseudopalindromický uzávěr"
    if isEpal(seq) == True:
        return(seq)
    i = 1
    while isEpal(seq[i:]) != True:
        i = i+1
    #print("    {0} nejdelší pseudopalindromický uzávěr : {1}".format(seq,seq[i:]))
    closure = seq
    pref = seq[i-1::-1]
    for letter in pref:
        if letter == "0":
            closure = closure + "1"
        if letter == "1":
            closure = closure + "0"
    return(closure)


# In[4]:

def makeWord(delta, theta, steps, seed = ""):
    "vytvoří slovo pomocí řídící posloupnosti a posloupnosti uzávěrů"
    w = seed
    for step in range(0,steps):
        w = w + delta[step]
        if theta[step] == "R":
            w = makePalClosure(w)
        if theta[step] == "E":
            w = makeEpalClosure(w)
        #print("w{0} = {1}".format(step+1,w))
    return(w)


# In[5]:

def makeS(word):
    "udělá operaci S na slovo"
    Sword = ""
    for i in range(0,len(word)-1):
        Sword += str((int(word[i]) + int(word[i+1])) %2)
    return Sword


# In[6]:

def isZps(word):
    '''kontroluje, jestli možné, aby slovo bylo získané zobec. pal. uzávěrem,
    pokud ano, vrací normalizovanou bidirektivní posloupnost''' 
    l=1
    prefixes = []
    while l <= len(word):
        if isPal(word[:l]) or isEpal(word[:l]):
            prefixes.append(word[:l])
        l=l+1
    #print(prefixes)
        
    iszps = True
    i=0
    newtheta= "R"
    newdelta= prefixes[0]
    while(i+1 < len(prefixes) and iszps == True):
        newletter = prefixes[i+1][len(prefixes[i])]
        palclo = makePalClosure(prefixes[i]+ newletter)
        epalclo = makeEpalClosure(prefixes[i]+ newletter)

        if(palclo == prefixes[i+1]):
            newtheta = newtheta + "R"
            newdelta = newdelta + newletter
        elif(epalclo == prefixes[i+1]):
            newtheta = newtheta + "E"
            newdelta = newdelta + newletter
        else:
            iszps = False
        i = i+1
    return([iszps, newdelta, newtheta])


# In[7]:

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return(ret)
    return wrap


# In[8]:

@timing
def testPrefixes(deltas, thetas, steps, seed):
    """Funkce, která všechny delty a thety otestuje, uděla prefixy, operaci S a pak vyzkouší,
    jestli získané slovo může být z zobec. pal. uz."""
    
    printed = False
    for delta in deltas:
        for theta in thetas:
            word = makeWord(delta, theta, steps, seed)
            Sword = makeS(word)
            result = isZps(Sword)
            if result[0]==True:
                #print("Slovo u:" + word)
                #print("S(u):" + Sword)
                if printed == False:
                    #print("delta = " + delta)
                    printed = True
                print("delta = {0}, theta = {1} : {2} ".format(delta, theta, result))
        if printed == True:
                print("")
        printed = False

