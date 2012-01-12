#h.7.7.py 
#MOD 7.7 enhanced State  enhanced State.
# Tested Basic play @ 2.5- 3 %

import sys,  math
from  collections import deque,  OrderedDict,  namedtuple,  Counter
import logging
import logging.config

#
#Cntr =  (fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
# ****************** namedtuples 
Crd = namedtuple('Crd', 'suit, valu') #  Card ('H', 3)  OR Crd_EMPTY
Stt = namedtuple('Stt', 'loc, fce, crd') #  State (('T3', 7), True,('H', 3),)
newStt =  namedtuple('newStt', ' stkNme,  fce,  crd')
Status =  namedtuple('Status', 'crd, fce, stkNme')  #began in v7.7 REVERSED ORDER.
Mov = namedtuple('Mov', 'crd, stkNme')  # Mov( Crd, 'T5')
Move = namedtuple('Move', 'crd, stkNme')  # Mov( Crd, 'T5')  #began in v7.7

# ***************string formating
Tmplt_Stt = "(({0.crd.suit:^6}, {0.crd.valu:02}), ({0.loc.nme:>2.2}, {0.loc.lng:02}), {0.fce:3<}, {0.top:3<})"
Tmplt_StkD = "(({0.loc.nme:>2.2}, {0.loc.lng:02}): " + Tmplt_Stt + ")"

#CONSTANTS
UP= TEST_TRUE = True
DOWN = TEST = TEST_FALSE = False
FACES = {'UP': True, 'DOWN':  False}
KING_CARDS =  [('S', 12),  ('H', 12),  ('D', 12),  ('C', 12)]
SUITS =[  'S', 'H', 'D',  'C'] 
VALUES =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,  13]
TABLEAUS = [  'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6']
FOUNDATIONS = SUITS  
STACKS = TABLEAUS + FOUNDATIONS
STAKES52L = ['T0', 'T1', 'T1', 'T1', 'T1', 'T1', 'T1', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T3', 'T3', 'T3', 'T3', 'T3', 'T3', 'T3', 'T3', 'T4', 'T4', 'T4', 'T4', 'T4', 'T4', 'T4', 'T4', 'T4', 'T5', 'T5', 'T5', 'T5', 'T5', 'T5', 'T5', 'T5', 'T5', 'T5', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6', 'T6']
FACES52L =  [True, False, True, True, True, True, True, False, False, True, True, True, True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True]
CARDS52L = [Crd(suit='S', valu=13), Crd(suit='S', valu=12), Crd(suit='S', valu=11), Crd(suit='S', valu=10), Crd(suit='S', valu=9), Crd(suit='S', valu=8), Crd(suit='S', valu=7), Crd(suit='S', valu=6), Crd(suit='S', valu=5), Crd(suit='S', valu=4), Crd(suit='S', valu=3), Crd(suit='S', valu=2), Crd(suit='S', valu=1), Crd(suit='H', valu=13), Crd(suit='H', valu=12), Crd(suit='H', valu=11), Crd(suit='H', valu=10), Crd(suit='H', valu=9), Crd(suit='H', valu=8), Crd(suit='H', valu=7), Crd(suit='H', valu=6), Crd(suit='H', valu=5), Crd(suit='H', valu=4), Crd(suit='H', valu=3), Crd(suit='H', valu=2), Crd(suit='H', valu=1), Crd(suit='D', valu=13), Crd(suit='D', valu=12), Crd(suit='D', valu=11), Crd(suit='D', valu=10), Crd(suit='D', valu=9), Crd(suit='D', valu=8), Crd(suit='D', valu=7), Crd(suit='D', valu=6), Crd(suit='D', valu=5), Crd(suit='D', valu=4), Crd(suit='D', valu=3), Crd(suit='D', valu=2), Crd(suit='D', valu=1), Crd(suit='C', valu=13), Crd(suit='C', valu=12), Crd(suit='C', valu=11), Crd(suit='C', valu=10), Crd(suit='C', valu=9), Crd(suit='C', valu=8), Crd(suit='C', valu=7), Crd(suit='C', valu=6), Crd(suit='C', valu=5), Crd(suit='C', valu=4), Crd(suit='C', valu=3), Crd(suit='C', valu=2), Crd(suit='C', valu=1)]
#FUNCTIONS

#----------------------------------------------------------------------
def calculate_std1(nL, mean):
    """ sqrt(var>>sum(w-mean)^2 / ( n-1))
    """
    total =  0
    n =  len(nL)
    for x in nL:
        total +=  (x -  mean) **2   # 
    var1 = total /  (len(nL) - 1)
    return math.sqrt(var1)
def calculate_std2(nCnt, winMean):
    """ sqrt(var>> N*mean(1-mean)/(N-1))
    
    >>> nL = [1,0,1,0,1,0,1,0,1,0]
    >>> n = len(nL)
    >>> m = .5
    >>> s1 = calculate_std1(nL, m)
    >>> s1
    0.5270462766947299
    >>> s2 = calculate_std2(n, m)
    >>> s2
    0.5270462766947299
    >>> (s1-s2)**.5
    0.0
    """
    var2 =  nCnt * winMean * (1 - winMean) / (nCnt - 1)
    return math.sqrt(var2)

