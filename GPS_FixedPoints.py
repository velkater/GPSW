
# coding: utf-8

# # GPS words and fixed points of morphisms

# In[40]:

import re
import zpu
def writetofile(text):
    with open("out.txt", "a") as ofile:
        ofile.write(str(text) + "\n")
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        writetofile('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return(ret)
    return wrap


# ## Substitution

# In[16]:

def subs(dic, n):
    s = dic["0"]
    i = 1
    while len(s) < n:
        s = s + dic[s[i]]
        i = i + 1
    return s[:n]


# ## Patterns we want to avoid in the bi-sequence

# In[17]:

cpattern = re.compile("^R+$") # sama R
dpattern = re.compile("^(01)+$") # slovo 0101010101
epattern = re.compile("((0R){20})|((0E){20})|((1R){20})|((1E){20})$")
fpattern = re.compile("((((0R)+1E){10})|(((0E)+1R){10})|(((1R)+0E){10})|(((1E)+0R){10}))$")


# ## Testing functions

# In[41]:

from multiprocessing import Pool
l = 300
def testword(rule, file = None):
    dicti = {"0": rule[0], "1": rule[1]}
    word = subs(dicti, l)
    ret = zpu.isZps2(word)
    if (ret[0]==True):
        bis = [ret[1], ret[2]]
        bis_c = zpu.makeBiseq(ret[1], ret[2])
        bisR = zpu.maximizeRinBiseq(ret[1], ret[2])
        if not (re.match(cpattern, bisR[1])) and         not (re.match(dpattern, word))and         not (re.search(epattern, bis_c)) and         not (re.search(fpattern, bis_c)):
            return  [True, dicti, bis, word[:40]]
        else:
            return None
    else:
        return None
@timing
def getresults(lphi0, lphi1, file = None):
    pool = Pool(processes=4)
    results = []
    for rep1 in range(1,lphi0):
        for rep2 in range(1,lphi1+1):
            phi0 = ['0'+ ''.join(i) for i in itertools.product('01', repeat=rep1)]
            phi1 = [''.join(j) for j in itertools.product('01', repeat=rep2)]
            cart = [ k for k in itertools.product(phi0, phi1)]
            r = pool.map_async(testword, cart)
            filteredresults = list(filter(lambda x: x != None, r.get()))
            if filteredresults != []:
                for res in filteredresults:
                    writetofile(res)
                    results.append(res)
    return results


# ## Results

# In[42]:

results = getresults(5,5)
#for result in results:
    #print(result)


# In[ ]:



