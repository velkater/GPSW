
# coding: utf-8

# In[2]:

import itertools
import zpu as zpu
import re
import sys


# In[3]:

def subs(dic, n):
    s = dic["0"]
    i = 1
    while len(s) < n:
        s = s + dic[s[i]]
        i = i + 1
    return s[:n]


# In[4]:

cpattern = re.compile("^R+$")
dpattern = re.compile("^(01)+$")


# In[9]:

from multiprocessing import Pool
pool = Pool(processes=2)

def blaaa(rule):
    dicti = {"0": rule[0], "1": rule[1]}
    word = subs(dicti, 300)
    ret = zpu.isZps(word)
    if (ret[0]==True):
        bis = [ret[1], ret[2]]
        if not (re.match(cpattern, bis[1])) and         not (re.match(dpattern, word)):
            pass
            print(str(dicti) + str(ret[0]) + " slovo: " + word[:50])
            print(bis)
            print("")

if __name__ == '__main__':
    print("JAO")
    for rep1 in range(1,3):
        for rep2 in range(1,4):
            phi0 = ['0'+ ''.join(i) for i in itertools.product('01', repeat=rep1)]
            phi1 = [''.join(j) for j in itertools.product('01', repeat=rep2)]
            cart = [ k for k in itertools.product(phi0, phi1)]
            n = 300
            print(list(pool.map(blaaa, cart)))
            print("asdasd")


