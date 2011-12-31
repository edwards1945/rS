""" state_testdocs.7.5.8.py 
#MOD  7.5.8 
# 111226 1445
# speciality States
"""

import random
from rS import *
import  stack,  state

import logging
import logging.config
####################################################
class test_State:
    """ combines 52 Cards and 11 Stacks to produce 52 States.    
    """
    def test_fndCnt(self):
        """
        >>> import state
        >>> from rS import *
        >>> s = state.State()
        >>> s.fndCnt == 0
        True
        >>> ff = state.FullFoundations()
        >>> ff.fndCnt == 52
        True
        >>>
        """
        pass
    
class test_FullState:   
    """
    # TESTS: include
    
    >>> import state, stack
    >>> from rS import *
    
    # (1) ****************** unshuffled with expected sequence.
    >>> unsfl = state.FullState(False)
    >>> t0 = unsfl.stkOD['T0']
    >>> len( t0)
    1
    >>> unsfl.crd2OD[Crd('S', 12)]  #  first crd to be faceDOWN
    newStt(stkNme='T1', fce=False, crd=Crd(suit='S', valu=12))
    
    >>> t6 = unsfl.stkOD['T6']
    >>> len(t6)  # 5 False 6 True
    11
    >>> t6.top_item  # fndMove() should  walk thru the entire deck.
    Crd(suit='C', valu=1)
    >>>  # (2) **************** shuffled
    >>> sfl = state.FullState()
    >>> t6 = sfl.stkOD['T6']
    >>> t6.top_item  != Crd(suit='C', valu=1)
    True
    >>>
    """
    pass

if __name__ == "__main__":
    import doctest
    #logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
