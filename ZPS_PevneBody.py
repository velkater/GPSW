
# coding: utf-8

# In[1]:

import itertools
import zpu as zpu
import re
import sys
import time


# In[2]:

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return(ret)
    return wrap


# In[3]:

def subs(dic, n):
    s = dic["0"]
    i = 1
    while len(s) < n:
        s = s + dic[s[i]]
        i = i + 1
    return s[:n]


# In[37]:

cpattern = re.compile("^R+$") # sama R
dpattern = re.compile("^(01)+$") # slovo 0101010101
epattern = re.compile("((0R){20})|((0E){20})|((1R){20})|((1E){20})$")
fpattern = re.compile("((((0R)+1E){10})|(((0E)+1R){10})|(((1E)+0R){10})|((((1E)+0R){10})))$")


# In[85]:

from multiprocessing import Pool
l = 300

def testwords(rule):
    dicti = {"0": rule[0], "1": rule[1]}
    word = subs(dicti, l)
    ret = zpu.isZps2(word)
    if (ret[0]==True):
        bis = [ret[1], ret[2]]
        bis_c = zpu.makeBiseq(ret[1], ret[2])
        bisR = zpu.maximizeRinBiseq(ret[1], ret[2])
        if not (re.match(cpattern, bisR[1])) and         not (re.match(dpattern, word))and         not (re.search(epattern, bis_c)) and not (re.match(fpattern, bis_c)):
            return  str(dicti) + " "+ " slovo: " + word[:40] + " " + str(bis)

@timing
def getresults(lphi0, lphi1):
    pool = Pool(processes=4)
    results = []
    for rep1 in range(1,lphi0):
        for rep2 in range(1,lphi1+1):
            phi0 = ['0'+ ''.join(i) for i in itertools.product('01', repeat=rep1)]
            phi1 = [''.join(j) for j in itertools.product('01', repeat=rep2)]
            cart = [ k for k in itertools.product(phi0, phi1)]
            r = pool.map_async(testwords, cart)
            results.append(list(filter(lambda x: x != None, r.get())))
    return results

results = getresults(14, 14)

for result in results:
    for words in result:
        print(words)
