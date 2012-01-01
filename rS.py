#rS.7.5.9.py
#MOD 7.5.9
## namedtuple Mov2Nme now Mov
#MOD 7.5.8  implemented uncovered Card in tableau set to faceUP in State and Stack

#I want to compare win rate of non-recursive play versus recursive play.

#Is 5% normal for stop when no more moves?
#as of 1112 basic play of shift all fundMoves, then a kng move then a sib move nets 2%.
#Is 8% or better for recursive?
#Recursive means trying every option until a win. Or maybe EVERY option and compare record."""
#Regex VER *[0-9]*\.[0-9]*

import sys
from  collections import deque,  OrderedDict,  namedtuple,  Counter
import logging
import logging.config
#
Cntr =  Counter(['winCnt', 'fCnt',  'nCnt'])
# ****************** namedtuples 
Crd = namedtuple('Crd', 'suit, valu') #  Card ('H', 3)  OR Crd_EMPTY
Stt = namedtuple('Stt', 'loc, fce, crd') #  State (('T3', 7), True,('H', 3),)
newStt =  namedtuple('newStt', ' stkNme,  fce,  crd')
Mov = namedtuple('Mov', 'crd, stkNme')  # Mov( Crd, 'T5')
HndStat =  namedtuple('HndStat', 'won, f_cnt' )  #HandCount(0, 3)
SetStat =  namedtuple('SetStat', 'won, f_cnt, n_Cnt' )  #SetCount(5, 4, 50)
# ***************string formating
Tmplt_Stt = "(({0.crd.suit:^6}, {0.crd.valu:02}), ({0.loc.nme:>2.2}, {0.loc.lng:02}), {0.fce:3<}, {0.top:3<})"
Tmplt_StkD = "(({0.loc.nme:>2.2}, {0.loc.lng:02}): " + Tmplt_Stt + ")"

#CONSTANTS
UP= TEST_TRUE = True
DOWN = TEST = TEST_FALSE = False
FACES = {'UP': True, 'DOWN':  False}
KING_CARDS =  [('S', 12),  ('H', 12),  ('D', 12),  ('C', 12)]
SUITS =[  'S', 'H', 'D',  'C'] #MOD 60.1 alpha order: THUS S, H,D,C ; NOT S,H,C,D
VALUES =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,  13]
TABLEAUS = [  'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6']
FOUNDATIONS = SUITS  
STACKS = TABLEAUS + FOUNDATIONS

################# 
        
if __name__ == "__main__":
        logging.config.fileConfig('myConfig.conf')        
        import doctest
        doctest.testmod(verbose=False)
        #doctest.testfile("rS_testdocs.py")

