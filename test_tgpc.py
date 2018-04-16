
# coding: utf-8

# In[1]:


import unittest

from tgpc import *

testcases = (
    ("0011", "00RR", ('0011', '00RR', True)),
    ("0012", "0020", ('00120', '00210', False)),
    ("0210", "0122", ('021021', '012012', False)),
    ("0112", "0211", ('011201', '021021', False)),
    ("0102110", "02R0121", ('01021102', '02R01201', False)),
    ("00210", "00122", ('0021021', '0012012', False)),
    ("010", "022", ('0101', '02R2', False)),
    ("011", "R11", ('01211', '021R1', False)),
    ("0112", "0211", ('011201', '021021', False)),
    ("01202", "02100", ('012021', '0210R0', False)),
    ("0121", "0212", ('01212', '021R2', False)),
    ("012111", "021R12", ('0121112', '021R1R2', False)),
    ("01", "0R", ('010', '02R', False)),
    ("011", "020", ('0112', '0210', False)),
    ("011", "022", ('0110', '02R2', False)),
    ("01", "01", ('012', '021', False)),
    ("0101", "02R1", ('01012', '02R21', False)),
    ("010101", "02R2R1", ('0101012', '02R2R21', False)),
    ("0101", "02RR", ('01010', '02R2R', False)),
    ("010221", "02R011", ('01022102', '02R01201', False)),
    ("00112", "00211", ('0011201', '0021021', False)),
    ("010212", "02R100", ('01021201', '02R10210', False)),
    ("0121202", "021R200", ('012120210', '021R20120', False)),
    ("012111202", "021R1R200", ('01211120210', '021R1R20120', False)),
    ("21022101", "RR021210", ('21202210210', '20R02120120', False)),
    ("01022101", "RR021210", ('01002210210', '02R02120120', False))
)

class TestNormalization012(unittest.TestCase):
    def test_Ei(self):
        self.assertEqual(Ei('1'), ('2', '1', '0'))
        self.assertEqual(Ei('0'), ('0', '2', '1'))
        self.assertEqual(Ei('2'), ('1', '0', '2'))
    
    def test_is_eipal(self):
        self.assertTrue(is_eipal("012", 1))        
        
    def test_Normalizer012(self):
        n = Normalizer012()
        for d, t, result in testcases:
            self.assertEqual(n.normalize(d,t), result, 
                             msg = "problem: ({0}, {1})".format(d, t))
                                 
    def test_NaiveNormalizer(self):
        nn = NaiveNormalizer012()
        for d, t, result in testcases:
            self.assertEqual(nn.normalize(d,t), result)

if __name__ == '__main__':
    unittest.main()

