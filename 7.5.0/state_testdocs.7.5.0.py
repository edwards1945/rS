""" state_testdocs.7.5.0.py 
#MOD 7.5.0
# 111217.1800
# 11 new class Stacks and 52 Crd
"""

import random
from rS import *
import  stack,  state

import logging
import logging.config
####################################################
class State_testdocs:
    """ combines 52 Cards and 11 Stacks to produce 52 States.
    
    >>> from rS import *
    >>> import  state
    >>> s = state.State(False)    # a test state
    >>> len(s.crdOD) == 52
    True
    >>> len(s.dekOD) == 11
    True
    >>> len( s.fnd_dekOD) == 4
    True
    >>> s.fnd_dekOD['H'].nme == 'H'
    True
    >>> s.fnd_dekOD['H'].PUSH('something')
    >>> s.fnd_dekOD['H'].length  == 1
    True
    >>> s.fnd_Count == 0  #NOT IMPLEMENTED
    True
    
    """
class TestState_testdocs:   
    """
    #>>> print("********** testing state.State.UPDATE_State")
    #********** testing state.State.UPDATE_State
    #>>> from rS import *
    #>>> import  state
    #>>> t = state.TestState()
    #>>> mov00 = Mov( Stt(Loc('T2', 10), False, Crd('C', 13)), 'C')
    #>>> mov10 = Mov( Stt(Loc(None, None), True, Crd('C', 12)), 'C')
    #>>> mov11 = Mov( Stt(Loc('T1', 1), True, Crd('C', 11)), 'C')
    #>>> movDk = deque([ mov11, mov10])
    #>>> t.UPDATE_State(movDk)
    #>>> len(t.dekOD['C']) == 2
    #True
    #>>> len(t.dekOD['T1234']) == 2
    #Traceback (most recent call last):
    #...
    #KeyError: 'T1234'
    #>>> #*** testing state.State.MOVE_Stt(mov, logger)"
    #>>> # *******first dek move of a top_item Stt: like fndMoves
    #>>> t = state.TestState()    
    #>>> mov00 = Mov( Stt(Loc(None, None), False, Crd('C', 13)), 'C')
    #>>> t.MOVE_Stt(mov00)
    #>>> Loc('C', 0) in t.crdOD[Crd('C', 13)]   # stt in dek
    #True
    #>>> Loc('C', 0) == t.dekOD['C'].top_item.loc
    #True
    
    
    """

if __name__ == "__main__":
    import doctest
    #logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
