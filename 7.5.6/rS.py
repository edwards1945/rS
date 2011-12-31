#rS.7.5.6.py module.
#MOD 7.5.6 
# #Stack was Loc(nme, ndx) now Loc(nme, lng) for length; allowing lng==0
#      111225 rS,namedtuple Ppu to avoid py name conflict with Pop

#PLAN: complete Game and Play for simple check4_Rules AND recusion; 
#then progressively add rules and complexity

#I want to compare win rate of non-recursive play versus recursive.

#Is 5% normal for stop when no more moves?
#as if 1112 basic shift all fundMoves, then a kng move then a sib move nets 2%.
#Is 8% or better for recursive?
#Recursive means trying every option until a win. Or maybe EVERY option and compare record."""
#Regex VER *[0-9]*\.[0-9]*

import sys
from  collections import deque,  OrderedDict,  namedtuple,  Counter
import logging
import logging.config
#
Cntr =  Counter(['wonCnt', 'fCnt',  'nCnt'])
#namedtuples 
Crd = namedtuple('Crd', 'suit, valu') #  Card ('H', 3)  OR Crd_EMPTY
Loc = namedtuple('Loc', 'stk, ndx') # Location ('<Stack>', 7) 
# lng can be 0: stack numbering is zero based. Loc's always have a Stt.
Stt = namedtuple('Stt', 'loc, fce, crd') #  State (('T3', 7), True,('H', 3),)
newStt =  namedtuple('newStt', ' stkNme,  fce,  crd')
#Stk =  namedtuple('Stk', 'nme, stk' )  # Stack( 'T0', <deque>)
Stk2 =  namedtuple('Stk', 'nme, stkNme' )  # Stack( 'T0', <deque>)
#Mov = namedtuple('Mov', 'crd  to_stk')  #Move: (Crd(), Stk())
Mov2Nme = namedtuple('Mov2Nme', 'crd, stkNme')  # Mov2Nme( Crd, 'T5')
#DEPRMov = namedtuple('Mov', 'frm_lov, to_stk, crd')  
#Pop =  namedtuple('Pop',  'nme, fce, crd')  #Pop('T1', True, Crd('H', 12))

#Ppu = namedtuple('Ppu',  'nme, fce, crd')  #Pop('T1', True, Crd('H', 12)) #MOD 7.5.4 avoid py  name conflict
HndStat =  namedtuple('HndStat', 'won, f_cnt' )  #HandCount(0, 3)
SetStat =  namedtuple('SetStat', 'won, f_cnt, n_Cnt' )  #SetCount(5, 4, 50)

#string formating
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
FOUNDATION_SIZE = 13

################# 
        
if __name__ == "__main__":
        logging.config.fileConfig('myConfig.conf')        
        import doctest
        doctest.testmod(verbose=False)
        #doctest.testfile("rS_testdocs.py")

