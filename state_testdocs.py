""" state_testdocs.7.7.1.py 
#MOD  7.6 
# 111226 1445
# speciality States
"""

import random
from h import *
import  stack,  state

import logging
import logging.config
############################################
def test_kng_move_newState(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING findMoves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')      
    >>> ##
    >>> ## kngMove: buried, & new Head is faceUP
    >>> ns = state.newState()
    >>> stsL = []  #Status to populate state
    >>> movsL = []
    >>> stsL.append(Status(Crd('S',2), False, 'T1'))  #  filler 
    >>> stsL.append(Status(Crd('S', 4), True, 'T2'))  # filler
    >>> stsL.append(Status(Crd('S', 6), True, 'T3'))  #  
    >>> stsL.append(Status(Crd('S', 8), True, 'T4'))  #
    >>> stsL.append(Status(Crd('S', 10), True, 'T5'))  #
    >>> stsL.append(Status(Crd('S', 13), True, 'T6'))  #  S13=> T0
    >>> stsL.append(Status(Crd('S', 12), True, 'T6'))  #
    >>> movsL.append(Move(Crd('S', 13), 'T0'))
    >>> ns.populate(stsL)
    >>> ns.move(movsL[0], logger)  #UNDER TEST
    >>> ns.stkOD['T6'].head == None
    True
    >>> ns.crdOD[Crd('S', 12)].crd == ns.stkOD['T0'].head  # new T2 head
    True
    >>>
    """
    pass

def test_fnd_move_newState(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING findMoves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')    
    >>> ##
    >>> ## fndMove: head => fnd
    >>> ns = state.newState()
    >>> stsL = []  #Status to populate state
    >>> movsL = []        
    >>> stsL.append(Status(Crd('S', 1), True, 'T0'))  #
    >>> movsL.append(Move(Crd('S', 1), 'S'))
    >>> ns.populate(stsL)
    >>> ns.move(movsL[0], logger)  #UNDER TEST
    >>> ns.stkOD['T0'].isEmpty
    True
    >>> ns.crdOD[Crd('S', 1)].stkNme == 'S'
    True
    >>> #
    """
    pass
def test_sib_move_newState(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING findMoves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')
    >>> ##
    >>> ## sibMove: buried, & new Head is faceUP
    >>> logger = logging.getLogger('myI')      
    >>> ns = state.newState()
    >>> stsL = []  #Status to populate state
    >>> movsL = []
    >>> stsL.append(Status(Crd('S', 5), False, 'T1'))  #  will be Head and fceUP  
    >>> stsL.append(Status(Crd('S', 3), True, 'T1'))  # will be in T2
    >>> stsL.append(Status(Crd('S', 2), True, 'T1'))  #  will be in T2 head
    >>> stsL.append(Status(Crd('S', 4), True, 'T2'))  #
    >>> movsL.append(Move(Crd('S', 3), 'T2'))
    >>> ns.populate(stsL)
    >>> ns.move(movsL[0], logger)  #UNDER TEST
    >>> ns.stkOD['T1'].head == Crd('S', 5)  # new T1 Head
    True
    >>> ns.crdOD[Crd('S', 5)].fce 
    True
    >>> ns.crdOD[Crd('S', 2)].crd == ns.stkOD['T2'].head  # new T2 head
    True
    >>> ##
    """

def test_kngMoves_newState(self):
    """
    >>> #(1) confirm kngMovs in findMoves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.newState()
    >>> #   EXPECTED MOVE DATA: kng ->- 1 empty; buried to head
    >>> t_ace = Crd( 'C', 1)
    >>> t_sts = Status(t_ace, True, 'T0')  # head to head
    >>> t_stsL = []
    >>> # #T0 empty
    >>> t_stsL.append(Status(Crd('S', 1), True, 'T1'))  # 
    >>> t_stsL.append(Status(Crd('S', 13), True, 'T1'))  # S13 head ->- empty T0 & T5
    >>> t_stsL.append(Status(Crd('H', 7), True, 'T2')) #h
    >>> t_stsL.append(Status(Crd('C', 4), False, 'T3'))  # 
    >>> t_stsL.append(Status(Crd('C', 13), True, 'T3'))  # C13 buried ->- empty T0 & T5
    >>> #   EXPECTED NO MOVE DATA: kng.fceDOWN; kng index 0;
    >>> t_stsL.append(Status(Crd('D', 12), False, 'T4'))  # 
    >>> t_stsL.append(Status(Crd('D', 13), False, 'T4'))  # D13 no move ->- emptyT0: faceDOWN
    >>> t_stsL.append(Status(Crd('H', 2), True, 'T4'))  # head
    >>> t_stsL.append(Status(Crd('H', 13), True, 'T6'))  # H13 no move ->-empty T0: index 0
    >>> t_stsL.append(Status(Crd('H', 4), True, 'T6'))  # h
    >>> st.populate(t_stsL)
    >>> #      SETUP COMPLETE
    >>> st.findMoves()  #UNDER TEST
    True
    >>> len( st.movesD['kng'] ) == 4 # 
    True
    >>> st.movesD['kng'][1]  == Move(crd=Crd(suit='C', valu=13), stkNme='T0')
    True
    >>> st.movesD['fnd'] == []
    True
    >>> st.movesD['sib'] == []
    True
    >>> # DONE
    """
    pass

def test_sibMoves_newState(self):
    """
    >>> #(1) confirm sibMovs in findMoves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.newState()
    >>> #   EXPECTED MOVE DATA: head TO head; buried to head
    >>> t_ace = Crd( 'C', 1)
    >>> t_sts = Status(t_ace, True, 'T0')  # head to head
    >>> t_stsL = []
    >>> t_stsL.append(Status(Crd('H', 6), True, 'T1'))  #head ->- head T2
    >>> t_stsL.append(Status(Crd('H', 7), True, 'T2')) #h
    >>> t_stsL.append(Status(Crd('C', 5), True, 'T3'))  # buried ->- head T4
    >>> t_stsL.append(Status(Crd('S', 5), True, 'T3'))
    >>> t_stsL.append(Status(Crd('C', 6), True, 'T4'))  #h
    >>> #   EXPECTED NO MOVE DATA: fceDOWN: fceDOWN, same tabl, fnd ->- tbl
    >>> t_stsL.append(Status(Crd('D', 6), False, 'T5'))  # no move ->- head T6: faceDOWN
    >>> t_stsL.append(Status(Crd('D', 7), True, 'T6'))  # h
    >>> t_stsL.append(Status(Crd('S', 2), True, 'S'))  # no move ->- head T5: fnd ->- tbl
    >>> t_stsL.append(Status(Crd('S', 2), True, 'T0'))  # no move ->- head T0: same tableau
    >>> t_stsL.append(Status(Crd('S', 3), True, 'T0'))  # h
    >>> st.populate(t_stsL)
    >>> #      SETUP COMPLETE
    >>> st.findMoves()  #UNDER TEST
    True
    >>> len( st.movesD['sib'] ) == 2 # 
    True
    >>> st.movesD['sib'][1]  == Move(crd=Crd(suit='C', valu=5), stkNme='T4')
    True
    >>> st.movesD['fnd'] == []
    True
    >>> st.movesD['kng'] == []
    True
    
    """
    pass

def test_fndMoves_newState(self):
    """
    >>> #(1) confirm fndMoves in findMoves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.newState()
    >>> #   EXPECTED MOVE DATA
    >>> t_ace = Crd( 'C', 1)
    >>> t_sts = Status(t_ace, True, 'T0')  # expect this Ace.
    >>> t_stsL = []
    >>> t_stsL.append(t_sts)
    >>> #   EXPECTED NO MOVE DATA
    >>> junk = Move(Crd('TEST', 4), 'TEST')
    >>> st.movesD['sib'].append(junk)   # PRELOAD <dict> to assure it is cleared on findMoves() call.
    >>> t_stsL.append(Status(Crd('H', 1), True, 'T2'))  # no move: buried
    >>> t_stsL.append(Status(Crd('H', 2), True, 'T2'))
    >>> st.populate(t_stsL)
    >>> #      SETUP COMPLETE
    >>> st.findMoves()  #UNDER TEST
    True
    >>> st.movesD['kng']  
    []
    >>> st.movesD['sib']  # junk movesD cleared
    []
    >>> st.movesD['fnd'] == [Move(crd=Crd(suit='C', valu=1), stkNme='C')]
    True
    
    """
    pass

def test_new_populate_newState(self):
    """
    >>> # confirm populate works using new namedtuple Status.
    >>> from h import *
    >>> import state, stack
    >>> st = state.newState()  # crd2OD & stkOD
    >>> # **** first assembled as argument
    >>> st.populate([ Status(Crd('D', 6), False, 'T5')])
    >>> st.crdOD[Crd('D', 6)] == Status(crd=Crd(suit='D', valu=6), fce=False, stkNme='T5')
    True
    >>> # **** now multiple status. 
    >>> p1 = [Status(Crd('C', 13), False, 'T3')]
    >>> p1.append( Status(Crd('C', 12), False, 'T3'))
    >>> p1.append( Status(Crd('C', 11), True, 'T3'))
    >>> st.populate(p1)
    >>> st.crdOD[Crd('C', 13)].fce == False
    True
    >>> l1 = [(stkNme, len(st.stkOD[stkNme]))  for stkNme in STACKS  if len(st.stkOD[stkNme]) > 0]
    >>> l1 == [('T3', 3), ('T5', 1)]
    True
    >>> #SUCCESSFUL POPULATING                
    """
    pass

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
        >>>
        #SUCCESSFUL POPULATING        
        """
        pass
    
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
        >>> # test_move
        """
        pass
    
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
