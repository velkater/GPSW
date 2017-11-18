
# coding: utf-8

# # Normalization over the alphabet $\{0,1,2\}$

# In[1]:


import gpc # library for work with GPS words over {0,1}
import math
import itertools
import re


# ## Work with $E_i$-palindromes and closures

# In[2]:


def Ei(i):
    i = int(i)
    ei = [0,0,0]
    ei[i] = str(i)
    ei[(i+1)%3] = str((2+i)%3)
    ei[(i+2)%3] = str((1+i)%3)
    return ei


# In[3]:


# Example:
if __name__ == '__main__':
    print(Ei('1'))


# In[4]:


def isEipal(seq, i):
    """Checks if a string seq is an E_i palindrome."""
    ei = Ei(i)
    l = len(seq)
    if l == 1:
        if seq == str(i):
            return True
        else:
            return False
    for x in range(0, math.ceil(l/2)):
        if seq[x] != ei[int(seq[l-1-x])]:
            return False
    return(True)


# In[5]:


# Example:
if __name__ == '__main__':
    print(isEipal("012", 1))
    print(isEipal("002", 1))
    print(isEipal("01201", 2))


# In[6]:


def testPalindromicity(seq):
    """Checks if a seq is an palindrome or and E-palindrome and 
    returns its nature."""
    if isEipal(seq,0):
        return [True, "0"]
    elif isEipal(seq, 1):
        return [True, "1"]
    elif isEipal(seq, 2):
        return [True, "2"]
    elif gpc.isPal(seq):
        return [True, "R"]
    else:
        return [False]


# In[7]:


# Example:
if __name__ == '__main__':
    print(testPalindromicity("0210"))
    print(testPalindromicity("00")) # We want 00 to be an E_0-palindrome
    print(testPalindromicity("010"))
    print(testPalindromicity("02110"))


# In[8]:


def makeEipalClosure (seq, i):
    """Makes E_i-th palindromic closure of a string."""
    ei = Ei(i)
    if isEipal(seq, i) == True:
        return(seq)
    j = 1
    while isEipal(seq[j:], i) != True:
        j = j+1
    gpc.verboseprint(2, "    {0} longest palindromic                      suffix : {1}".format(seq,seq[j:]))
    closure = seq
    pref = seq[j-1::-1]
    for letter in pref:
        closure = closure + ei[int(letter)]
    return(closure)


# In[9]:


# Example:
if __name__ == '__main__':
    print(makeEipalClosure("01", 1))
    print(makeEipalClosure("00", 2))
    print(makeEipalClosure("00", 0))
    print(makeEipalClosure("021210", 2))


# In[10]:


def make012Word(delta, theta, steps, seed = ""):
    """Makes a GPS over {0,1,2} from sequences delta and theta."""
    w = seed
    for step in range(0,steps):
        w = w + delta[step]
        if theta[step] == "R":
            w = gpc.makePalClosure(w)
        elif theta[step] in ["0", "1", "2"]:
            w = makeEipalClosure(w, theta[step])
        else:
            print("wrong symbol")
            break
        gpc.verboseprint(1, "w{0} = {1}".format(step+1,w))
    return(w)


# In[11]:


# Example:
if __name__ == '__main__':
    make012Word("0012", "0020", 4)


# ## Naive function for checking normalization

# In[12]:


def is012NormalizedNaive(delta, theta, steps):
    """Checks if delta and theta are normalized and if not, 
    returns the beginning of the normalized sequence."""
    w = ""
    l=1
    prefixes = []
    for step in range(0,steps):
        w = w + delta[step]
        if theta[step] == "R":
            w = gpc.makePalClosure(w)
        elif theta[step] in ["0", "1", "2"]:
            w = makeEipalClosure(w, theta[step])
        else:
            print("wrong symbol")
            break
        prefixes.append(w)
    gpc.verboseprint(1, "Prefixes from (delta, theta): " + str(prefixes))
    gpc.verboseprint(1, "Obtained word: " + w)
    newdelta = delta[0]
    newtheta = ""
    while l <= len(w):
        prefix = w[:l]
        res = testPalindromicity(prefix)
        if res[0] == True:
            gpc.verboseprint(1, prefix)
            if l < len(w):
                newdelta = newdelta + w[l]
            newtheta = newtheta + res[1]           
        l=l+1
    if newdelta == delta[:steps] and newtheta == theta[:steps]:
        return [True, newdelta, newtheta]
    else:
        return [False, newdelta, newtheta]
    
    # The length of newdelta and newtheta are the same since the whole word 
    # is an palindrome because if was generated by the GPS construction
    # from delta and theta.


# In[13]:


# Example: 
if __name__ == '__main__':
    print(is012NormalizedNaive("0012", "0020", 4))
    print(is012NormalizedNaive("00120", "00210", 4))


# ## Implementation of the normalization algorithm

# ### Preprocessing of the normalized bi-sequence for our implementation

# In our implementation of the algorithm, we decided to work only with words
# that has 0 as first letter, 1 at second and 2 at third in order to make the 
# algorithm easier to read and write. Of course, we want it working for all
# the bi-sequences, so we have to preprocess the bi-sequence so that the word
# obtained has first 0, then 1 and then 2. After the result of the algorithm,
# we will go back to the original letters order. Of course, we want to do it, 
# without having to compute the infinite word.

# In[14]:


def substitute(dic, seq):
    """Substitutes letters in a word according to rules in dic, if there is
    no rule for the letter, keeps the letter."""
    newseq = ""
    for l in seq:
        if l in dic:
            newseq = newseq + dic[l]
        else:
            newseq = newseq + l
    return newseq


# In[15]:


def compose(subs1, subs2):
    """Composes two substitutions of letter."""
    csub = {}
    for l in ["0", "1", "2"]:
        if l in subs1:
            csub[l] = subs1[l]
            if csub[l] in subs2:
                csub[l] = subs2[csub[l]]
        elif l in subs2:
            csub[l] = subs2[l]
    return csub


# In[16]:


# Example:
if __name__ == '__main__':
    print(compose({}, {"1": "0", "0": "1"}))
    print(compose({"0": "1", "1": "0"}, {"1" : "2", "2" : "0", "0": "1"}))


# In[17]:


def changeLettersOrder(delta, theta):
    """ Change (delta, theta) so that the word obtained is the same as the 
    original one, but the first symbol is 0, the second 1 and the third 2."""
    subs = {}
    subs2 = {"2": "1", "1": "2"}
    if delta[0] != "0":
        subs = {delta[0]: "0", "0": delta[0]}
        delta = substitute(subs, delta)
        theta = substitute(subs, theta)
    i = 0
    l = len(delta)
    while i < l and delta[i] == "0":
        if theta[i] == "2":
            return [delta, theta, subs]
        if theta[i] == "1":
            delta = substitute(subs2, delta)
            theta = substitute(subs2, theta)            
            return [delta, theta, compose(subs, subs2)]
        #otherwise whe have to continue
        i = i + 1
    if i < l and delta[i] == "2":
        delta = substitute(subs2, delta)
        theta = substitute(subs2, theta) 
        return [delta, theta, compose(subs, subs2)]
    return [delta, theta, subs]


# In[18]:


def changeLettersOrderBack(delta, theta, subs):
    """ Give back the original delta and theta that were transformed with 
    the substitution subs"""
    backsubs = {v:k for k,v in subs.items()}
    delta = substitute(backsubs, delta)
    theta = substitute(backsubs, theta)
    return [delta, theta]


# In[19]:


# Example: 
if __name__ == '__main__':
    ex1 = changeLettersOrder("111122220000", "11111RR00112")
    print(ex1)
    print(changeLettersOrderBack(ex1[0], ex1[1], ex1[2]), "\n")
    ex2 = changeLettersOrder("000", "001")
    print(ex2)
    print(changeLettersOrderBack(ex2[0], ex2[1], ex2[2]), "\n")
    ex3 = changeLettersOrder("011", "02")
    print(ex3)
    print(changeLettersOrderBack(ex3[0], ex3[1], ex3[2]), "\n")
    ex4 = changeLettersOrder("0002", "0RR0")
    print(ex4)
    print(changeLettersOrderBack(ex4[0], ex4[1], ex4[2]), "\n")
    ex5 = changeLettersOrder("111120", "1RR10")
    print(ex5)
    print(changeLettersOrderBack(ex5[0], ex5[1], ex5[2]))


# ### Preprocessing of the beginning of the bi-sequence

# We want that every word beginning with $i^l$ (where $l$ is the largest
# possible) has a bi-directive sequence $(\Delta, \Theta)$ where the prefix
# of $\Theta$ of lenght $l$ is equal to $E^l_i$. (We only solve the cases
# when there is an $R$ instead of $E_0$ (e.g. $(0000, RE_0RE_0) \to (0000, E_0E_0E_0E_0)$).

# In[20]:


def initialNormalization(delta, theta):
    biseq = gpc.makeBiseq(delta, theta)
    m = re.match("(0(R|0))+", biseq)
    if m:
        biseq = "00"*int((m.end()-m.start())/2) + biseq[m.end():]
    return gpc.parseBiseq(biseq)


# In[21]:


if __name__ == '__main__':
    initialNormalization("000011", "R0R021")


# ### Auxiliary functions

# Here is the list of the bad prefixes rewrited for infinite word having first occurences of 0, 1 and 2 in that order.

# 
# 
# <img src="prefixesrules.jpg",width=600>
#     
#     
#     

# Now we rewrite those prefixes in Regex.

# In[134]:


# List: bad prefix regex --> the new symbols instead of the last one
bad_prefixes = [
    ["(00)*02", "0012", 1], # 1.
    ["00(120R)+10", "1220", 2], # 2.
    ["0012(0R12)*01", "0R21", 3],  # 3.
    #["00121121", "200211", 4], # 4.
    #["001210", "1120", 5], # 5. removed, special case of (sco) in 24
    #["001212", "1R02", 6], # 6. removed, sco 22
    ["001221(1R11)*12", "1R22", 7], # 7.fixed rule and rewrite
    ["0012211R(111R)*10", "1100", 8], # 8.
    #["001R", "120R", 9], # 9. ! Error, it is not a special case... removed, sco 15
    ["001222", "210012", 10], # 10.
    #["0011", "1221", 11], # 11. removed sco rule 13 when rewritten
    ["0012(0R12)*00", "0R20", 12], # 12. fixed error
    ["00(120R)*11", "1221", 13], # 13.
    ["(001221)*00122R", "211R", 14], # 14.
    ["(001221)*001R","120R", 15], # 15. * because of rule 9
    ["(001221)+0R","002R", 16], # 16.
    ["(001221)+1R2R", "222R", 17], # 17.
    ["(001221)*00120R2R", "201R", 18], # 18.
    ["(001221)+002R2R", "210R", 19], # 19.
    ["00(120R)*122111", "1R11", 20], # 20.
    ["0012(0R12)*0R2022", "2112", 21], # 21.
    ["(00)+1212", "1R02", 22], # 22.
    ["0012(0R12)+2020", "2R10", 23], # 23. (can be also + and then rule3)
    ["(00)*1210", "1120", 24], # 24.
    ["0012(0R12)*0R2112", "1022", 25], # 25.
    ["001221(1R11)*0020", "2R10", 26], # rewritten rule 26.
    ["001221(1R11)*1R2201", "0021", 27], # 27.
    ["(00)+1202", "0R12", 28], # new added rule 28. !!!!
    ["0010", "122100", 29], # new added rule 29.
    ["00(120R)+202111", "120021", 30], # 1st added rule for 2 pseudopal
    ["(00)+121121", "200211", 31], # 2nd added rule for 2 pseudopal
    ["00(120R)+211020", "220110", 32], # 3rd added rule for 2 pseudopal
    ["001221(1R11)*1R220020", "211200", 33], # 4th rules added for 2 pseudopal
    ["(00)+001111", "1R11", 34], # from (011, R11)
    ["(00)+001020", "2R10", 35] # from (012, R00)
]


# In[99]:


if __name__ == '__main__':
    print(len(bad_prefixes))


# Next, we list all the possible cases of the 4 non-prefix rules. They follow 
# below in a more readable form...

# In[24]:


a_b = [i[0]+i[1] for i in itertools.product('012', repeat = 2)]
i = ["0", "1", "2"]
# we consider here b as b_2
rules1 = [ k[0][0]+ "R" + Ei(k[1])[int(k[0][1])]+ k[1] + 
          k[0][1] +k[1] for k in itertools.product(a_b, i)]
rules2 = [ k[0][0]+ k[1] + Ei(k[1])[int(k[0][1])]+ "R" + 
          k[0][1] +"R" for k in itertools.product(a_b, i)]

ij = itertools.permutations("012", 2)
#we condider here b as b_1
rules3 = [ k[0][0] + k[1][0] + k[0][1] + 
           k[1][1] + Ei(k[1][1])[int(Ei(k[1][0])[int(k[0][1])])] + k[1][0] 
          for k in itertools.product(a_b, ij)]

ijk = itertools.permutations("012", 3)
rules4 =[ k[0][0] + k[1][0] + k[0][1] + k[1][1] + 
         Ei(k[1][1])[int(Ei(k[1][0])[int(k[0][1])])] + k[1][2] + 
            Ei(k[1][2])[int(Ei(k[1][0])[int(k[0][1])])] + k[1][2]
         for k in itertools.product(a_b, ijk)]

if __name__ == '__main__':
    print("Intern rules 1:")
    print(rules1, "\n")
    print("Intern rules 2:")
    print(rules2, "\n")
    print("Intern rules 3:")
    print(rules3, "\n")
    print("Intern rules 4:")
    print(rules4, "\n")

    # Rules in a more "readable" form
    print("-----------")
    print("More readable rules:")
    rules1Readable = [gpc.parseBiseq(rule) for rule in rules1]
    print( "Rules 1: (ab_1b_2, RE_iE_i) where b_1=E_i(b_2)")
    print(rules1Readable, "\n")

    rules2Readable = [gpc.parseBiseq(rule) for rule in rules2]
    print( "Rules 2: (ab_1b_2, E_iRR) where b_1=R(b_2) = b_2") # correction
    print(rules2Readable, "\n") 

    rules3Readable = [gpc.parseBiseq(rule) for rule in rules3]
    print( "Rules 3: (ab_1b_2, E_iE_jE_i) where E_i(b_1)=E_j(b_2)")
    print(rules3Readable, "\n")  

    rules4Readable = [gpc.parseBiseq(rule) for rule in rules4]
    print( "Rules 4: (ab_1b_2b_3, E_iE_jE_kE_k) where E_i(b_1)=E_j(b_2)= E_k(b_3)")
    print(rules4Readable, "\n") 


# In[71]:


def findNextBadFactor(biseq):
    """ Searching for the next (most left) non-prefix rule to apply."""
    matches = []
    for rule in rules1:
        match = re.match('([012R][012R])*('+ rule + ')', biseq)
        if match:
            gpc.verboseprint(1, "rule1: " +                              str(gpc.parseBiseq(rule)) +                              " in biseq " + str(gpc.parseBiseq(biseq)))
            index = match.end() - 2 # The position that would be corrected
            #Here follows the correction:
            matches.append([index, rule[4]+"R"+ rule[2] + #Ei(rule[3])[int(rule[2])] + 
                           rule[3], 2])
            biseq = biseq[:index + 3] # There is no sense searching further
    for rule in rules2:
        match = re.match('([012R][012R])*('+ rule + ')', biseq)
        if match:
            gpc.verboseprint(1, "rule2:  " +                              str(gpc.parseBiseq(rule)) +                              " in biseq " + str(gpc.parseBiseq(biseq)))
            index = match.end() - 2
            matches.append([index, rule[4]+rule[1]+rule[2]
                            + "R", 2])
            biseq = biseq[:index + 3]
    for rule in rules3:
        match = re.match('([012R][012R])*('+ rule + ')', biseq)
        if match:
            gpc.verboseprint(1, "rule3: " +                              str(gpc.parseBiseq(rule)) +                              " in biseq " + str(gpc.parseBiseq(biseq)))
            index = match.end() - 2
            matches.append([index, rule[4]+Ei(rule[1])[int(rule[3])] 
                            + Ei(rule[1])[int(Ei(rule[3])[int(rule[2])])] + 
                            rule[1], 2])
            biseq = biseq[:index + 3]
    for rule in rules4:
        match = re.match('([012R][012R])*('+ rule + ')', biseq)
        if match:
            gpc.verboseprint(1, "rule4: " +                              str(gpc.parseBiseq(rule)) +                              " in biseq " + str(gpc.parseBiseq(biseq)))
            index = match.end() - 2
            matches.append([index, rule[6]+rule[1]+rule[2]+rule[3]+rule[4] +
                            rule[5], 2]) # nema tu byt 4??? asi ne
            biseq = biseq[:index + 3]
    
    gpc.verboseprint(1, "all non-prefix matches: " + str(matches))
    # Final "leading" prefix
    final = []
    if matches:
        final = matches[0]
        for rule in matches[1:]:
            if rule[0] < final[0]:
                final = rule
    gpc.verboseprint(1, "Final change:" + str(final))
    return final  


# In[26]:


def isNormalized(biseq):
    """ Function looking is there is a bad prefix of a bad factor
    inside the preprocessed biseq. If so, it returns the bad prefix position and the
    correction to apply. If not, it returned an emply field (for now)."""
    
    gpc.verboseprint(1, "at the beginning of isNormalized:" +                     str(gpc.parseBiseq(biseq)))
    matches = []
    # Looking for bad prefixes
    for prefixRule in bad_prefixes:
        match = re.match(prefixRule[0], biseq)
        if match:
            gpc.verboseprint(1, "prefix rule: " + str(prefixRule))
            index = match.end() - 2
            return [index, prefixRule[1], 2] # bad prefix to repare
            # the third number is the length of the sequence we replace
            # so that we know where to continue in the original bi-sequence
            
    
    # If there is no bad prefix, we look for bad factors. We can do it in 
    # this way because if we have a bad prefix, everything is normalized
    # up to its end and therefore there cannot be neither bad factors nor
    # other bad prefix before
    badfactor = findNextBadFactor(biseq)
  
    return badfactor # bad factor to repare


# In[27]:


def applyRule(biseq, rule):
    """ Function that applies the correction 'rule' in the biseq."""
    return biseq[:rule[0]] + rule[1] + biseq[rule[0] + rule[2]:]


# ### Normalization algorithm

# Here follows the main normalization algorithm.

# In[28]:


def normalize012(delta1, theta1):
    """Returns the normalized directive bi-sequence giving the same GPS word
    as (delta, theta)"""
    # Normalization of the letters order
    [delta, theta, substitution] = changeLettersOrder(delta1, theta1)
    
    # Normalization of the prefix
    [delta, theta] = initialNormalization(delta, theta)
    
    # The main algorithm:
    biseq = gpc.makeBiseq(delta, theta)
    applicableRule = []
    applicableRule = isNormalized(biseq)  
    
    # We do this look until there is no normalization rule to apply
    while applicableRule:
        biseq = applyRule(biseq, applicableRule);
        applicableRule = isNormalized(biseq)
    
    [delta, theta] = gpc.parseBiseq(biseq)
    
    gpc.verboseprint(1, "at the end of isNormalized:" +                     str(gpc.parseBiseq(biseq)))
    delta, theta = changeLettersOrderBack(delta, theta, substitution)
    notchanged = (delta1 == delta) and (theta1 == theta)
    return [notchanged, delta, theta]


# In[29]:


# We set the verbose for debugging to see the results
gpc.verbose = 1


# ## Results
# 
# Only some "randomly" chosen bisequences where tested up to now...
# 
# The tested bisequences ** that now work well ** can be found in the unit tests in the file test_normalize012.ipynb and we switch directly to the non working cases...

# ## Changes:
# 
# * a new rule (28) was created: $(010, E_0E_0E_2) \rightarrow (0101, E_0E_2RE_2)$ (it had the same effect as $(010 RE_2E_2)$, which is in the non-prefix rule but is missing from the prefix rules)
# * in the rule 20, we change + to *
# * we add a new prefix rule (29) from the Pozorovani 3.7 2nd dot for $l=1$ (for $l>1$ it uses rule 28 and then uses other rules). The rule is $(01, E_0E_0) \rightarrow (0120, E_0E_2E_1E_0)$.
# * fixing rule 4 that was not normalized: rule 4 $(0112, E_0 E_2 E_1 E_1)$ instead of $(01120, E_0 E_2 E_1 E_0 E_1)$ shoud be rewritten as $(011201, E_0 E_2 E_1 E_0 E_2 E_1)$
# * the rule 26 was rewritten, because Pepa said $n$ could take the value -1. (the prefix from rules 1 $(012, E_RE_0E_0)$ did not work correctly, the final result was not normalized, it was ['01202', '02100'] instead of [False, '012021', '0210R0']
# * we checked all the rules for normalization (check once more)
# * we checked where should be * and where should be +. Now it should be correct.
# * rule 7 was corrected (2 at the end of the new delta) and rewritten to $(012(11)^n1, E_0E_2E_1(RE_1)^nE_2)$ and was corrected to be $(012(11)^n1, E_0E_2E_1(RE_1)^nE_2) \rightarrow (012(11)^n12, E_0E_2E_1(RE_1)^nRE_2)$ (the 2 in the end of $\delta$ was a 0
# * rule 9 was removed because it is a special case of rule 15
# * rule 5 was removed because it is a special case of rule 24
# * rule 6 was removed because it is a special caseof rule 22
# * rule 13 was rewritten to  (0(10)^n1, E_0(E_2R)^nE_1) a then rule we removed rule 11
# * the second non-prefix rule was rewritten so that the normalized rule is $(ab_1b_2b_1, E_iRE_iR)$
# * we added 4 new rules when two pseudopalindromes are skipped:
#     - $(0(10)^l221, E_0(E_2R)^lE_0E_1E_1) \rightarrow (0(10)^l22102, E_0(E_2R)^lE_0E_1E_2E_0E_1)$ (30)
#     - $(0^l112, E_0^lE_2E_1E_1) \rightarrow (0^l11201, E_0^lE_2E_1E_0E_2E_1)$ (31)
#     - $(0(10)^l212, E_0(E_2R)^lE_1E_0E_0) \rightarrow (0(10)^l21201, E_0(E_2R)^lE_1E_0E_2E_1E_0)$ (32)
#     - $(012(11)^l1202, E_0E_2E_1(RE_1)^lRE_2E_0E_0) \rightarrow (012(11)^l120210, E_0E_2E_1(RE_1)^lRE_2E_0E_1E_2E_0)$ (33)
# * rule 4 was removed because it is a special case of rule 31

# **TO DO**
# - test systematically all the prefixes and find good test cases (maybe ask Pepa for some of them)
# - fixing the new problematic cases
# - case of rule 29 being not normalized in rule 2

# In[143]:


#for testing
gpc.verbose = 1
delta = "0121202"
theta = "021R200"
print(is012NormalizedNaive(delta, theta,len(delta)))
print()
normalize012(delta, theta)


# In[144]:


gpc.verbose = 0


# In[ ]:




