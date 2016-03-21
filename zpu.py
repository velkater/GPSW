
# coding: utf-8

# # Zobecněný pseudopalindromický uzávěr

# ## Funkce pro vytvoření zobecněného pseudopalindromického uzávěru

# In[1]:

import time
import re


# In[2]:

verbose = 0
verboseprint = lambda x,y: print(y) if verbose >= x else None


# In[3]:

def isPal(seq):
    '''kontroluje jestli řetězec je palindrom'''
    l = len(seq)
    if l == 1:
        return(True)
    for x in range(0, l//2):
        if seq[x] != seq[l-1-x]:
            return(False)
    return(True)

def isEpal(seq):
    '''kontroluje jestli řetězec je pseudopalindrom'''
    l = len(seq)
    if l%2 == 1:
        return(False)
    for x in range(0, l//2):
        if seq[x] == seq[l-1-x]:
            return(False)
    return(True)


# In[4]:

def makePalClosure (seq):
    '''udělá z řetězce palindromický uzávěr'''
    if isPal(seq) == True:
        return(seq)
    i = 1
    while isPal(seq[i:]) != True:
        i = i+1
    verboseprint(2, "    {0} nejdelší palindromický uzávěr : {1}".format(seq,seq[i:]))
    verboseprint(2, "    délka nejdelší palindromický uzávěr : {0}".format(len(seq[i:])))
    closure = seq + seq[i-1::-1]
    return(closure)

def makeEpalClosure (seq):
    "udělá z řetězce pseudopalindromický uzávěr"
    if isEpal(seq) == True:
        return(seq)
    i = 1
    while isEpal(seq[i:]) != True:
        i = i+1
    verboseprint(2, "    {0} nejdelší E- palindromický uzávěr : {1}".format(seq,seq[i:]))
    closure = seq
    pref = seq[i-1::-1]
    for letter in pref:
        if letter == "0":
            closure = closure + "1"
        if letter == "1":
            closure = closure + "0"
    return(closure)


# In[5]:

def makeWord(delta, theta, steps, seed = ""):
    "vytvoří slovo pomocí řídící posloupnosti a posloupnosti uzávěrů"
    w = seed
    for step in range(0,steps):
        w = w + delta[step]
        if theta[step] == "R":
            w = makePalClosure(w)
        elif theta[step] == "E":
            w = makeEpalClosure(w)
        else:
            print("wrong symbol")
            break
        verboseprint(2, "w{0} = {1}".format(step+1,w))
    return(w)


# In[6]:

def makeS(word):
    "udělá operaci S na slovo"
    Sword = ""
    for i in range(0,len(word)-1):
        Sword += str((int(word[i]) + int(word[i+1])) %2)
    return Sword


# In[7]:

def isZps(word, closure = "ER", max_no_matters_closure_type = 0):
    '''kontroluje, jestli možné, aby slovo bylo získané zobec. pal. uzávěrem,
    pokud ano, vrací normalizovanou bidirektivní posloupnost''' 
    maximum = max_no_matters_closure_type
    l=1
    prefixes = []
    while l <= len(word):
        if ((l<=maximum or closure != "E") and isPal(word[:l])) or         ((l<=maximum or closure != "R") and isEpal(word[:l])):
            prefixes.append(word[:l])
        l=l+1
    verboseprint(1, prefixes)
    
    if not prefixes:
        verboseprint(1, "No prefixes of type " + str(closure) + " were found")
        return([False])
    if (len(prefixes[0]) > 2) or (len(prefixes[-1]) < len(word)//2) :
        return([False])        
        
    iszps = True
    i=0
    if closure != "E":
        newtheta = "R"
        newdelta = prefixes[0]
    else:
        newtheta = "E"
        newdelta = prefixes[0][0]
        
    while(i+1 < len(prefixes) and iszps == True):
        newletter = prefixes[i+1][len(prefixes[i])]
        condition_noE = (len(prefixes[i+1]) <= maximum) or (closure != "E")
        condition_noR = (len(prefixes[i+1]) <= maximum) or (closure != "R")
        if (condition_noE):
            palclo = makePalClosure(prefixes[i]+ newletter)
        if (condition_noR):
            epalclo = makeEpalClosure(prefixes[i]+ newletter)

        if(condition_noE and palclo == prefixes[i+1]):
            newtheta = newtheta + "R"
            newdelta = newdelta + newletter
        elif(condition_noR and epalclo == prefixes[i+1]):
            newtheta = newtheta + "E"
            newdelta = newdelta + newletter
        else:
            iszps = False
        i = i+1
    return([iszps, newdelta, newtheta])


# In[20]:

def rindex(mylist, myvalue):
    return len(mylist) - mylist[::-1].index(myvalue) - 1
def isZps2(word, closure = "ER", max_no_matters_closure_type = 0):
    '''kontroluje, jestli možné, aby slovo bylo získané zobec. pal. uzávěrem,
    pokud ano, vrací normalizovanou bidirektivní posloupnost''' 
    maximum = max_no_matters_closure_type
    length = len(word)
    l=1
    prefixes = [["R", word[0]],["E", word[0]]]
    lengths = [0, 0]
    iszps = True
    newT = ""
    
    while l <= len(word) and iszps == True:
        
        while l <= len(word):
            if ((l<=maximum or closure != "E") and isPal(word[:l])):
                newT = "R"
                break
            elif ((l<=maximum or closure != "R") and isEpal(word[:l])):
                newT = "E"
                break
            l = l+1
        if l < length:
            prefixes.append([newT, word[l]])
            lengths.append(l)
        elif l == length:
            prefixes.append([newT, None])
            lengths.append(l)
        l = l + 1
        
        if not prefixes:
            verboseprint(1, "No prefixes of type " + str(closure) + " were found")
            return([False])
        if (len(prefixes[0][1]) > 2):
            return([False])
                
        new_wk = prefixes[-1]
        wk = prefixes[-2]
        goodlpps = [new_wk[0], wk[1] if new_wk[0]==wk[0] else str((int(wk[1])+1)%2)]
        verboseprint(1, "{0} {1}".format(goodlpps, goodlpps in prefixes[:-2]))
        if (goodlpps in prefixes[:-2]):
            llps = lengths[rindex(prefixes[:-2],goodlpps)]
            if 2*lengths[-2] - llps != lengths[-1]:
                iszps = False
        elif (new_wk[0] == "R") and (2*lengths[-2] + 1 == lengths[-1]):
            pass
        elif (new_wk[0] == "E") and (2*lengths[-2] + 2 == lengths[-1]):
            pass
        else:
            iszps = False
                
    if ((lengths[-1]+2) < length//2):
        return([False])
        
    
    newdelta = word[0]
    newtheta = ""
    llist = list(zip(*prefixes))
    newtheta = newtheta + ''.join(llist[0][2:])
    newdelta = newdelta + ''.join(llist[1][2:-1])
    return([iszps, newdelta, newtheta])


# In[21]:

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return(ret)
    return wrap


# ## Normalizace a bi-posloupnosti

# In[9]:

bad_prefixes = ["(0R)*0E", "(1R)*1E", "(0R)+1E1E", "(1R)+0E0E"]
bad_factors = ["1R0E1E", "1R1E0E", "0R0E1E", "0R1E0E", "1E0R1R", "1E1R0R", "0E0R1R", "0E1R0R"]


# In[10]:

def makeBiseq(delta, theta):
    """Makes one sequence from the bi-sequence delta andm theta"""
    if len(delta) != len(theta):
            print("délky delta a theta nejsou stejné")
            return 
    s = ""
    for i in range(len(delta)):
        s = s + delta[i] + theta[i]
    return s
def parseBiseq(biseq):
    """Makes from one sequence the bi-sequence delta and theta"""
    delta = ""
    theta = ""
    for i in range(len(biseq)):
        if i%2 == 0:
            delta = delta + biseq[i]
        else:
            theta = theta + biseq[i]
    return [delta, theta]


# In[11]:

def repare_ii(match, a):
    a_bar = ["1", "0"]
    length = match.end()
    s = match.string
    s = s[length:]
    s = a_bar[int(a)] + "E" + s
    s = (a + "R") * int(length/2) + s
    return s
    
def repare_iii(match, a):
    a_bar = ["1", "0"]
    length = match.end()
    s = match.string
    s = s[length:]
    s = a_bar[int(a)] + "E" + a_bar[int(a)] + "R" + a + "E" + s
    s = (a + "R") * int((length-4)/2) + s
    return s
    
def rep_0(match):
    return repare_ii(match, "0")
    
def rep_1(match):
    return repare_ii(match, "1")
    
def rep_2(match):
    return repare_iii(match, "0")
    
def rep_3(match):
    return repare_iii(match, "1")
    
norm_replace_functions = [rep_0, rep_1, rep_2, rep_3]


# In[12]:

def Normalize(delta, theta):
    biseq = makeBiseq(delta, theta)
    if biseq.startswith("0R1R"):
        biseq = biseq.replace("0R1R", "0R1E0R", 1)
    elif biseq.startswith("1R0R"):
        biseq = biseq.replace("1R0R", "1R0E1R", 1)
    else:
        i = 0
        matched = re.match(bad_prefixes[i], biseq)
        #print(matched)
        while (i<4) and (matched == None):
            i = i+1
            if i<4:
                matched = re.match(bad_prefixes[i], biseq)
                #print(matched)
            
        if i < 4:
            #print("pattern: " + str(i))
            biseq = norm_replace_functions[i](matched)
    
    i=0
    while (i < len(biseq) - 5):
        j = 0
        while (j <  8) and (biseq[i:i+6] != bad_factors[j]):
            j = j+1
        if (j == 8):
            i = i+1
        else:
            bad = bad_factors[j]
            #print(parseBiseq(bad))
            biseq = biseq.replace(bad, bad[0:5] + bad[1] + bad[2:4], 1)
            #print(parseBiseq(biseq))
            i = max(0, i+2)
    return parseBiseq(biseq)


# In[13]:

def isNormalized(delta, theta, verbose = "False"):
    biseq = makeBiseq(delta, theta)
    if biseq.startswith("0R1R") or biseq.startswith("1R0R"):
        if verbose:
            print("je tam RR aa*")
        return False
    elif (re.match(bad_prefixes[0], biseq) != None) or (re.match(bad_prefixes[1], biseq) != None):
        if verbose:
            print("je tam R^iE a^i")
        return False
    elif (re.match(bad_prefixes[2], biseq) != None) or (re.match(bad_prefixes[3], biseq) != None):
        if verbose:
            print("je tam R^iEE a^ia*a*")
        return False
    elif any(x in biseq for x in bad_factors):
        if verbose:
            print("ve slove je tt*t* abb*")
        return False
    else:
        return True


# In[14]:

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


# In[4]:

def maximizeRinBiseq(delta, theta):
    delta, theta = Normalize(delta, theta)
    biseq = makeBiseq(delta, theta)
    #print(biseq)
    badfact = ["0E0R1E0R", "0E1R0E1R", "1E0R1E0R", "1E1R0E1R" ]
    replacement = ["0E0R1R", "0E1R0R", "1E0R1R", "1E1R0R" ]
    l = len(biseq)
    if l >= 8:
        i = l-8
        while (i >= 0):
            j=0
            substring = biseq[i:i+8]
            while (j <  4) and (substring != badfact[j]):
                j = j+1
            if (j == 4):
                i = i-1
            else:
                bad = badfact[j]
                #print(parseBiseq(bad))
                biseq = rreplace(biseq, substring, replacement[j],1)
                #print(parseBiseq(biseq))
                i = i-2
    if biseq.startswith("0R1E0R"):
        biseq = biseq.replace("0R1E0R", "0R1R", 1)
    elif biseq.startswith("1R0E1R"):
        biseq = biseq.replace("1R0E1R", "1R0R", 1)
        
    return parseBiseq(biseq)


# ## Testování

# In[16]:

def _testGPW(deltas, thetas, steps, seed = "", normalized = False, 
                      closure = "RE", max_no_matters_closure_type = 0, additional_operation = ""):
    """Funkce, která všechny delty a thety otestuje, uděla prefixy, (případně další operaci) a pak vyzkouší,
    jestli získané slovo může být z zobec. pal. uz."""
    
    number_of_true = 0
    printed = False
    for delta in deltas:
        for theta in thetas:
            if(normalized == False or isNormalized(delta, theta)):
                word = makeWord(delta, theta, steps, seed)
                testedword = word
                if additional_operation == "S":
                    testedword = makeS(word)
                result = isZps(testedword, closure, max_no_matters_closure_type)
                if result[0]==True:
                    #print("Slovo u:" + word)
                    #print(additional_operation + "(u):" + testedword)
                    print("delta = {0}, theta = {1} : {2} ".format(delta, theta, result))
                    number_of_true += 1
    print("počet biposloupností:" + str(number_of_true))


# In[17]:

@timing
def testGPW_S_on_GPW(deltas, thetas, steps, seed = "", normalized = False, 
                      closure = "RE", max_no_matters_closure_type = 0):
    """Funkce, která všechny delty a thety otestuje, uděla prefixy, operaci S a pak vyzkouší,
    jestli získané slovo může být z zobec. pal. uz."""
    
    _testGPW(deltas, thetas, steps, seed, normalized, closure, max_no_matters_closure_type, "S")


# In[18]:

@timing
def testGPW(deltas, thetas, steps, seed = "", normalized = False, 
                      closure = "RE", max_no_matters_closure_type = 0):
    """Funkce, která všechny delty a thety otestuje, uděla prefixy a pak vyzkouší,
    jestli získané slovo může být z zobec. pal. uz."""
    
    _testGPW(deltas, thetas, steps, seed, normalized, closure, max_no_matters_closure_type)

