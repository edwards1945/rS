""" state_testdocs.7.5.5.py 
#MOD  7.5.4 
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
    """
class FullState_testdocs:   
    """
    >>> from rS import *
    >>> import  state
    >>> s = state.FullState()    # a test state
    >>> len(s.crdOD) == 52
    True
    >>> len(s.stkOD) == 11
    True
    >>> s.stkOD['H'].nme == 'H'
    True
    >>> s.stkOD['H'].PUSH('something')
    >>> len( s.stkOD['H'])  == 1
    True
    
    """
if __name__ == "__main__":
    import doctest
    #logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
