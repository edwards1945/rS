""" state_testdocs.7.6.py 
#MOD  7.6 Tested Basic play @ 2.5- 3 %
# 111226 1445
# speciality States
"""

import random
from h import *
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
        >>> from h import *
        >>> s = state.State()
        >>> s.fndCnt == 0
        True
        >>> ff = state.FullFoundations()
        >>> ff.fndCnt == 52
        True
        >>>
        """
        pass
    
    def test_populate(self):
        """       
        >>> from h import *
        >>> import state, stack
        >>> st = state.State()  # crd2OD & stkOD
        >>> # **** first assembled as argument
        >>> st.populate([ newStt('T5',True, Crd('D', 6))])
        >>> st.crd2OD[Crd('D', 6)]
        newStt(stkNme='T5', fce=True, crd=Crd(suit='D', valu=6))
        >>> # **** now multiple pops 
        >>> p1 = [newStt('T3', False, Crd('C', 13))]
        >>> p1.append( newStt('T3', False, Crd('C', 12)))
        >>> p1.append( newStt('H', True, Crd('C', 11)))
        >>> st.populate(p1)
        
        >>> l1 = [(stkNme, len(st.stkOD[stkNme]))  for stkNme in STACKS  if len(st.stkOD[stkNme]) > 0]
        >>> l1 == [('T3', 2), ('T5', 1), ('H', 1)]
        True
        >>> #SUCCESSFUL POPULATING        
        """
    def test_move(self,  mov2, logger=None):  #MOD 7.5.4
        """ faceUP Crd[s] >TO> StackNme:
        CALLED from Hand.
        # tests include:
        >>> # ********** BASIC: tbl TOP  >TO> tbl_top
        
        >>> # ********** BASIC: tbl SLICE >TO> tbl_top
        >>> import state, stack
        >>> from h import *
        >>> st =state.State()
        >>> p1 = [newStt('T3', True, Crd('C', 13))]
        >>> p1.append( newStt('T3', True, Crd('C', 12)))  # TEST CARD. No matter what fce I choose UP or DOWN the population call will make it UP.
        >>> p1.append( newStt('T3', True, Crd('C', 1)))
        >>> st.populate(p1)
        >>> cs =st.crd2OD[Crd('C', 12)]
        >>> cs = cs._replace(fce=False)
        >>> st.crd2OD[Crd('C', 12)] = cs
        >>> st.crd2OD[Crd('C', 12)] .fce
        False
        >>> # State IS POPULATED *********
        >>> mov = Mov(Crd('C', 1), 'H')
        >>> st.move(mov)
        >>> st.crd2OD[st.stkOD['T3'].top_item].fce  #C-12 set faceUP
        True
        """
class test_FullState:   
    """
    # TESTS: include
    
    >>> import state, stack
    >>> from h import *
    
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
    >>> import state
    >>> from h import *
    >>> ff = state.FullFoundations()
    >>> ff.fndCnt == 52
    True
    >>> ff.stkOD['S'][0] == Crd(suit='S', valu=1)
    True
    >>> ff.stkOD['S'].top_item == Crd(suit='S', valu=13)
    True
    >>> ff.stkOD['C'].top_item == Crd(suit='C', valu=13)
    True
    >>>    
    
    """
    pass

if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
