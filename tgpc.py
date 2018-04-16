
# coding: utf-8

# In[17]:


import itertools
import re
import logging
import math
logging.basicConfig(format='%(message)s', level=logging.ERROR)

class Normalizer012:
    """Object for normalizing ternary directive bi-sequences using the 
    new normalization algorithm.
    """
    
    def __init__(self):
        """Initialization of the normalization rules checker."""
        self._rules_checker = _Normalization012_rules_checker()
        
    def normalize(self, delta, theta):
        """Ternary normalization algorithm.
        
        Normalization function that returns the normalized directive
        bi-sequence giving the same generalized pseudostandard
        word as (delta, theta).

        Args:
            delta (str): The sequence delta of the directive bi-sequence.
                It should be composed of the letters '0', '1' and '2'.
            theta (str): The sequence theta of the directive bi-sequence.
                It should be composed from the letters 'R', '0', '1' and
                '2', where the last three stand for E_0, E_1 and E_2.

        Returns:
            Returns the tuple `(new_delta, new_theta, notchanged)` where (new_delta, new_theta)
            is the normalized bi-sequence of (delta, theta). The boolean `notchanged` is True 
            if the bi-sequence (delta, theta) was already normalized, otherwise it is False.
            
        Examples:
            >>> n = Normalizer012()
            >>> n.normalize("0011", "00RR")
            ('0011', '00RR', True)
            
            >>> n.normalize("0102110", "02R0121")
            ('01021102', '02R01201', False)
        """
        # Checking correct input
        _check_dt(delta, theta)
        
        # Changing the letters to be in order 0,1,2
        delta_t, theta_t, substitution = self._change_letters_order(delta, theta)
        
        # Interleaving delta and theta to get only one sequence from two
        biseq = "".join(d + t for d, t in zip(delta_t, theta_t))

        # Initial pre-processing of the prefix
        biseq = self._initial_normalization(biseq)

        # The main algorithm:

        # Creating a rule checker that find if a normalization rule is applicable
        # and returns its correction.
        applicable_rule = self._rules_checker.find_applicable_rule(biseq)
        
        while applicable_rule:
            biseq = self._apply_rule(biseq, applicable_rule);
            applicable_rule = self._rules_checker.find_applicable_rule(biseq)

        # Post-processing
        new_delta, new_theta = (biseq[0::2], biseq[1::2])
        logging.info("bi-sequence before changing the letters back: (" +                         new_delta + ", " + new_theta + ")")

        new_delta, new_theta = self._change_letters_order_back(new_delta, 
                                                               new_theta, substitution)
        
        notchanged = (delta == new_delta) and (theta == new_theta)
        return (new_delta, new_theta, notchanged)
    
    # Preprocessing
    @staticmethod
    def _substitute(dic, seq):
        """Substitutes letters in a word according to rules in the dictionary
        dic. If there is no rule for the letter, keeps the letter.
        """
        newseq = ""
        for l in seq:
            if l in dic:
                newseq = newseq + dic[l]
            else:
                newseq = newseq + l
        return newseq
    
    @staticmethod
    def _compose_substitutions(subs1, subs2):
        """Composes two substitutions of letters."""
        csub = {}
        for l in ["0", "1", "2"]:
            if l in subs1:
                csub[l] = subs1[l]
                if csub[l] in subs2:
                    csub[l] = subs2[csub[l]]
            elif l in subs2:
                csub[l] = subs2[l]
        return csub

    def _change_letters_order(self, delta, theta):
        """Changes (delta, theta) so that the word obtained is the same as the 
        original one, but the first symbol is 0, the second 1 and the third 2.
        """
        subs = {}
        subs2 = {"2": "1", "1": "2"}
        # changing the first letter to be 0
        if delta[0] != "0":
            subs = {delta[0]: "0", "0": delta[0]}
            delta = self._substitute(subs, delta)
            theta = self._substitute(subs, theta)
        i = 0
        l = len(delta)
        
        #changing the second letter to 1
        while i < l and delta[i] == "0":
            if theta[i] == "2":
                return [delta, theta, subs]
            if theta[i] == "1":
                delta = self._substitute(subs2, delta)
                theta = self._substitute(subs2, theta)            
                return [delta, theta, self._compose_substitutions(subs, subs2)]
            i = i + 1
            
        if i < l and delta[i] == "2":
            delta = self._substitute(subs2, delta)
            theta = self._substitute(subs2, theta) 
            return [delta, theta, self._compose_substitutions(subs, subs2)]
        return [delta, theta, subs]

    def _change_letters_order_back(self, delta, theta, subs):
        """Gives back the original letter order of delta and theta that were 
        transformed with the substitution subs.
        """
        backsubs = {v:k for k,v in subs.items()}
        delta = self._substitute(backsubs, delta)
        theta = self._substitute(backsubs, theta)
        return [delta, theta]
    
    @staticmethod
    def _initial_normalization(biseq):
        """Initial preprocessing of the directive bi-sequence so that
        the prefix (i^l, {RE_i}^l) is (i^l, E_i^l).
        """
        m = re.match("(0(R|0))+", biseq)
        if m:
            biseq = "00"*int((m.end()-m.start())/2) + biseq[m.end():]
        return biseq
    
    @staticmethod
    def _apply_rule(biseq, correction):
        """Function that applies the correction in the biseq."""
        return biseq[:correction[0]] + correction[1] + biseq[correction[0] + 2:]
    
    def print_all_factor_rules(self):
        """Prints in a readable form all the factor normalization rules"""
        self._rules_checker.print_all_factor_rules_readable
        

class _Normalization012_rules_checker:
    """Checks if some normalization rule is applicable and if so,
    returns its position and correction.   
    """
    
    def __init__(self):
        """
        Preparing and compiling all the normalization rules.
        """
        self._ei = {"0": Ei("0"), "1": Ei("1"), "2": Ei("2")}
        self._generate_factor_rules()        
        self._compile_rules()
    
    # Regex representing left sides of the prefix normalization rules,
    # their corrections (and the identifier of the rule for information).
    _bad_prefixes_and_correction = (
            ("(00)*02", "0012", 1),
            ("0010", "122100", 2),
            ("00(120R)+10", "1220", 3),
            ("0012(0R12)*01", "0R21", 4),
            ("001221(1R11)*12", "1R22", 5),
            ("0012211R(111R)*10", "1100", 6),
            ("001222", "210012", 7),
            ("0012(0R12)*00", "0R20", 8),
            ("00(120R)*11", "1221", 9),
            ("(001221)*00122R", "211R", 10),
            ("(001221)*001R","120R", 11),
            ("(001221)+0R","002R", 12),
            ("(001221)+1R2R", "222R", 13),
            ("(001221)+002R2R", "210R", 14),
            ("(001221)*00120R2R", "201R", 15),
            ("00(120R)*122111", "1R11", 16),
            ("0012(0R12)*0R2022", "2112", 17),
            ("(00)+1212", "1R02", 18),
            ("0012(0R12)+2020", "2R10", 19),
            ("(00)+1210", "1120", 20),
            ("0012(0R12)*0R2112", "1022", 21),
            ("001221(1R11)*0020", "2R10", 22),
            ("001221(1R11)*1R2201", "0021", 23),
            ("(00)+1202", "0R12", 24),
            ("(00)+001111", "1R11", 25),
            ("(00)+001020", "2R10", 26),
            ("00(120R)+202111", "120021", 27),
            ("(00)+121121", "200211", 28),
            ("00(120R)+211020", "220110", 29),
            ("001221(1R11)*1R220020", "211200", 30)
    )
            
    def find_applicable_rule(self, biseq):
        """Finds the next applicable normalization rule in the directive bi-sequence.
        
        Function looking if a prefix rules or a factor rules is applicable inside the
        pre-processed directive bi-sequence.

        Args:
            biseq (str): Directive bi-sequence (interleaved preprocessed sequences delta
                and theta).

        Returns:
            Returns None if no normalization rule is applicable. If there is, it finds
            the applicable on the shortest prefix of the directive bi-sequence and returns 
            the index and the correction to apply.
        """    
        logging.info("Checking for an applicable rule in" + str((biseq[0::2], biseq[1::2])))
        
        applicable_rule = self._find_next_prefix_rule(biseq)
        if applicable_rule:
            return applicable_rule
        
        # If there is no bad prefix, we look for a factor rule
        applicable_rule = self._find_next_factor_rule(biseq)
        if applicable_rule:
            return applicable_rule  
    
    def _find_next_prefix_rule(self, biseq):
        # Looking for a prefix rule
        for prefix_rule in self._prefix_rules:
            match = re.match(prefix_rule[0], biseq)
            if match:
                logging.info("prefix rule: " + str(prefix_rule))
                index = match.end() - 2
                return [index, prefix_rule[1]] # place and correction
    
    def _find_next_factor_rule(self, biseq):
        """Find the next applicable factor rule, i.e., the rule that can be 
        applied on the shortest prefix of the directive bi-sequence.
        """
        matches = []
        for rules_index,_rules in self._factor_rules.items():
            for rule in _rules:
                match = re.match(rule, biseq)
                if match:
                    logging.info("rule" + str(rules_index) + ": " +                     str(self._print_factor_rule(rule)) +
                    " in biseq " + str((biseq[0::2], biseq[1::2])))
                    
                    position = match.end() - 2 # The position to be corrected
                    #Index of match and correction:
                    matches.append([position, self._factor_rules_replacement(rules_index, match.group(2))])
                    biseq = biseq[:position + 3]

        logging.debug("all non-prefix matches: " + str(matches))
        
        # Finding final factor rule (leftmost)
        if matches:
            final = matches[0]
            for rule in matches[1:]:
                if rule[0] < final[0]:
                    final = rule
            logging.debug("Final change:" + str(final))
            return final 
    
    def _factor_rules_replacement(self, index, rule):
        """Finds the correction for a given factor rule, depending
        on the type of the rule (1, 2, 3 or 4).
        """
        ei = self._ei
        if index == 1:
            return rule[4]+"R"+ rule[2] + rule[3]
        elif index == 2:
            return rule[4]+rule[1]+rule[2] + "R"
        elif index == 3:
            return (rule[4]+ei[rule[1]][int(rule[3])] 
                    + ei[rule[1]][int(ei[rule[3]][int(rule[2])])] + rule[1])
        elif index == 4:
            return rule[6]+rule[1]+rule[2]+rule[3]+rule[4] + rule[5]
        else:
            logging.error("No correction found.")
    
    def _generate_factor_rules(self):
        """Creates all possible factor rules (of type 1, 2, 3 and 4)"""
        ei = self._ei
        a_b = [i[0]+i[1] for i in itertools.product('012', repeat = 2)]
        i = ["0", "1", "2"]
        
        # we consider here b as b_2
        self._rules1 = (k[0][0]+ "R" + ei[k[1]][int(k[0][1])]+ k[1] + 
                  k[0][1] + k[1] for k in itertools.product(a_b, i))
        self._rules2 = (k[0][0]+ k[1] + ei[k[1]][int(k[0][1])]+ "R" + 
                  k[0][1] +"R" for k in itertools.product(a_b, i))

        ij = itertools.permutations("012", 2)
        # we consider here b as b_1
        self._rules3 = (k[0][0] + k[1][0] + k[0][1] + 
                   k[1][1] + ei[k[1][1]][int(ei[k[1][0]][int(k[0][1])])] + k[1][0] 
                  for k in itertools.product(a_b, ij))

        ijk = itertools.permutations("012", 3)
        self._rules4 =(k[0][0] + k[1][0] + k[0][1] + k[1][1] + 
                 ei[k[1][1]][int(ei[k[1][0]][int(k[0][1])])] + k[1][2] + 
                    ei[k[1][2]][int(ei[k[1][0]][int(k[0][1])])] + k[1][2]
                 for k in itertools.product(a_b, ijk))
    def _compile_rules(self):
        """Compiles de regexes of all the normalization rules."""
        self._prefix_rules = tuple((re.compile(rule[0]),rule[1],rule[2])
                                   for rule in self._bad_prefixes_and_correction)

        self._factor_rules = {}
        self._factor_rules[1] = tuple( re.compile('^([012R]{2})*('+ rule + ')')
                                      for rule in self._rules1 )
        self._factor_rules[2] = tuple( re.compile('^([012R]{2})*('+ rule + ')')
                                      for rule in self._rules2 )
        self._factor_rules[3] = tuple( re.compile('^([012R]{2})*('+ rule + ')')
                                      for rule in self._rules3 )
        self._factor_rules[4] = tuple( re.compile('^([012R]{2})*('+ rule + ')')
                                      for rule in self._rules4 )
    
    def print_all_factor_rules_readable(self):
        """Prints all the factor rules"""
        for index in self._factor_rules:
            self._print_factor_rules(index)
            
    def _print_factor_rules(self, index):
        """Prints factor rules of one type"""
        readable_rules = []
        print("Factor rules " + str(index))
        for rule in self._factor_rules[index]:
            readable_rules.append(self._print_factor_rule(rule))
        print(tuple(readable_rules))
                                  
    def _print_factor_rule(self, rule):
        """Prints a readable factor rule"""
        rule_from_regex = rule.pattern.split("*")[1][1:-1]
        return (rule_from_regex[0::2], rule_from_regex[1::2])

class NaiveNormalizer012:
    """Object for normalizing ternary directive bi-sequences using
    a naive algorithm.
    """
        
    def normalize(self, delta, theta):
        """Ternary naive normalization algorithm.
        
        Naive normalization function that returns the normalized 
        directive bi-sequence giving the same generalized pseudostandard
        word as (delta, theta). It creates the prefixes w_i by palindromic
        closures a then checks if those are the only pseudopalindromic
        prefixes in the word created by the directive bi-sequence.

        Args:
            delta (str): The sequence delta of the directive bi-sequence.
                It should be composed of the letters '0', '1' and '2'.
            theta (str): The sequence theta of the directive bi-sequence.
                It should be composed from the letters 'R', '0', '1' and
                '2', where the last three stand for E_0, E_1 and E_2. Theta
                should be of the same length as delta.

        Returns:
            Returns the tuple `(new_delta, new_theta, notchanged)` where (new_delta, new_theta)
            is the normalized bi-sequence of (delta, theta). The boolean `notchanged` is True 
            if the bi-sequence (delta, theta) was already normalized, otherwise it is False.
            
        Examples:
            >>> nn = NaiveNormalizer012()
            >>> nn.normalize("0011", "00RR")
            ('0011', '00RR', True)
            
            >>> nn.normalize("0102110", "02R0121")
            ('01021102', '02R01201', False)
        """
        # Checking correct input
        _check_dt(delta, theta)
                         
        w = ""
        l=1
        prefixes = []
        
        # Creating the pseudopalindromic prefixes w_i
        for step in range(0,len(delta)):
            w = w + delta[step]
            if theta[step] == "R":
                w = make_pal_closure(w)
            elif theta[step] in ["0", "1", "2"]:
                w = make_eipal_closure(w, theta[step])
            else:
                logging.error("wrong symbol")
                return
            prefixes.append(w)
        logging.info("Prefixes from (delta, theta): " + str(prefixes))
        logging.info("Obtained word: " + w)
        
        # Finding all the pseudopalindromic prefixes of the word obtained
        newdelta = delta[0]
        newtheta = ""
        while l <= len(w):
            prefix = w[:l]
            res = self._test_palindromicity(prefix)
            if res[0] == True:
                logging.info(prefix)
                if l < len(w):
                    newdelta = newdelta + w[l]
                newtheta = newtheta + res[1]           
            l=l+1
            
        if newdelta == delta and newtheta == theta:
            return (newdelta, newtheta, True)
        else:
            return (newdelta, newtheta, False)
        
    @staticmethod
    def _test_palindromicity(seq):
        """Checks if a seq is an palindrome or an Ei-palindrome and 
        returns its nature. Note that the word ii..i is considered 
        here as an E_i palindrome.
        """
        if is_eipal(seq,0):
            return [True, "0"]
        elif is_eipal(seq, 1):
            return [True, "1"]
        elif is_eipal(seq, 2):
            return [True, "2"]
        elif is_pal(seq):
            return [True, "R"]
        else:
            return [False]

def Ei(i):
    """The involutory antimorphism Ei.

    Args:
        i : Either 0, 1, 2 or "0", "1", "2"
        
    Returns:
        A tuple corresponding to the involutory antimorphism Ei.

    Examples:
        >>> Ei(0)
        ('0', '2', '1')
        >>> Ei(1)
        ('2', '1', '0')
        >>> Ei(2)
        ('1', '0', '2')
    """
    # Checking correct input
    if i not in {0, 1, 2, "0", "1", "2"}:
        raise ValueError("{} is not in A = {{0,1,2}}".format(i))
        
    i = int(i)
    ei = [0,0,0]
    ei[i] = str(i)
    ei[(i+1)%3] = str((2+i)%3)
    ei[(i+2)%3] = str((1+i)%3)
    return tuple(ei)

def is_eipal(seq, i):
    """Checks if a word is an Ei-palindrome.

    Args:
        seq (string): The word checked composed 
            of the letters "0", "1" and "2".
        i: Pseudopalindromic type, can be either 0, 1, 2, or 
            "0", "1", "2", standing for E_0, E_1 and E_2.
        
    Returns:
        True if the word is an Ei-palindrome, otherwise False.

    Examples:
        >>> is_eipal("012", 1)
        True
        >>> is_eipal("002", 1)
        False
    """
    # Checking correct input
    if i not in {0, 1, 2, "0", "1", "2"}:
        raise ValueError("{} is not in A = {{0,1,2}}".format(i))
    _check_ternary(seq)
    
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

def is_pal(seq):
    """Checks if a word is an R-palindrome.

    Args:
        seq (string): The word checked.     

    Returns:
        True if the word is an Ei-palindrome, otherwise False.

    Examples:
        >>> is_pal("012")
        False
        >>> is_pal("010")
        True
    """
    l = len(seq)
    if l == 1:
        return(True)
    for x in range(0, l // 2):
        if seq[x] != seq[l - 1 - x]:
            return(False)
    return(True)

def make_pal_closure(seq):
    """Makes palindromic closure of a string.

    Args:
        seq (string): A word.
    Returns:
        The palindromic closure of the word.

    Examples:
        >>> make_pal_closure("101")
        '101'
        >>> make_pal_closure("102")
        '10201'
    """
    if is_pal(seq) == True:
        return(seq)
    i = 1
    while is_pal(seq[i:]) != True:
        i = i + 1
    logging.debug("{0} longest palindromic suffix: {1}"
                  .format(seq, seq[i:]))
    closure = seq + seq[i - 1::-1]
    return(closure)

def make_eipal_closure (seq, i):
    """Makes Ei-palindromic closure of a string.

    Args:
        seq (string): A word composed 
            of the letters "0", "1" and "2".
        i: Pseudopalindromic type, can be either 0, 1, 2, or 
            "0", "1", "2", standing for E_0, E_1 and E_2.
    Returns:
        The palindromic closure of the word.

    Examples:
        >>> make_eipal_closure("102", 0)
        '102'
        >>> make_eipal_closure("101", 1)
        '10121'
    """
    # Checking correct input
    if i not in {0, 1, 2, "0", "1", "2"}:
        raise ValueError("{} is not in A = {{0,1,2}}".format(i))
    _check_ternary(seq)
    
    ei = Ei(i)
    if is_eipal(seq, i) == True:
        return(seq)
    j = 1
    while is_eipal(seq[j:], i) != True:
        j = j+1
    logging.debug("{0} longest ei-palindromic suffix : {1}"
                  .format(seq,seq[j:]))
    closure = seq
    pref = seq[j-1::-1]
    for letter in pref:
        closure = closure + ei[int(letter)]
    return(closure)

def make_word012(delta, theta, seed = ""):
    """Makes a ternary GPS word from (delta, theta).

    Args:
        delta (str): The sequence delta of the directive bi-sequence,
            composed of the letters '0', '1' and '2'.
        theta (str): The sequence theta of the directive bi-sequence,
            composed from the letters 'R', '0', '1' and '2', where 
            the last three stand for E_0, E_1 and E_2. Must have the 
            same length as delta.
        seed (str): seed (initial w_0), optional.


    Returns:
        A string made by pseudopalidnromic closure from (delta, theta).

    Examples:
        >>> make_word012("0011", "012R")
        '00221112200'
    """
    # Checking correct input
    _check_dt(delta, theta)
    
    # Making w by pseudopalindromic closure
    w = seed
    for step in range(len(delta)):
        w = w + delta[step]
        if theta[step] == "R":
            w = make_pal_closure(w)
        elif theta[step] in ["0", "1", "2"]:
            w = make_eipal_closure(w, theta[step])
        else:
            logging.error("wrong symbol")
            return
        logging.info("w{0} = {1}".format(step+1,w))
    return(w)

def set_logging(logging_level = "ERROR"):
    """Sets the logging level of the module.
    
    If the level is set to "ERROR", the functions log only errors.
    If it is set to "INFO" or "DEBUG", the fuctions print more 
    information about how ternary words are being processed.
    
    Args:
        level(str): "ERROR" (default), "INFO" or "DEBUG"
    """
    logging.getLogger().setLevel(logging_level)

def _check_ternary(seq):
    """Raises an error if seq is not in A = {"0","1", "2"}"""
    if not all([x in set("012") for x in seq]):
        raise ValueError("{} is not in A = {{0,1,2}}".format(seq))
    
def _check_theta(seq):
    """Raises an error if seq is not in A = {"0","1", "2", "R"}"""
    if not all([x in set("012R") for x in seq]):
        raise ValueError("{} is not in A = {{0,1,2,R}}".format(seq))
        
def _check_dt(delta, theta):
    """Check if the input delta and theta are correct"""
    _check_ternary(delta)
    _check_theta(theta)
    if len(delta) != len(theta):
        raise ValueError("The length of delta and theta are not the same")
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

