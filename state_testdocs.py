""" state_testdocs_7.7.5.py 
#MOD  7.6 
# 111226 1445
# speciality States
"""

import random
from h import *
import  stack,  state

import logging
import logging.config
########################################
def test_FullState(State):
    """
    # UNDER TEST: FullState
    >>> # SETUP
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')      
    >>> ## init
    >>> nfs = state.FullState( False)
    >>> nfs.stkOD['T6'].head == Crd('C', 1)
    True
    >>> nfs.crdOD[Crd('H', 12)].fce
    False
    >>>
    """ 
    pass

def test_kng_move_State(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING find_Moves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')      
    >>> ##
    >>> ## kngMove: buried, & new Head is faceUP
    >>> ns = state.State()
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

def test_fnd_move_State(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING find_Moves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')    
    >>> ##
    >>> ## fndMove: head => fnd
    >>> ns = state.State()
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
def test_sib_move_State(self):
    """ improve monitoring of moves.
    # UNDER TEST: move()  #NOT TESTING find_Moves()
    >>> # EXPECTED GOOD 
    >>> from h import *
    >>> import state, stack
    >>> logger = logging.getLogger('myI')
    >>> ##
    >>> ## sibMove: buried, & new Head is faceUP
    >>> logger = logging.getLogger('myI')      
    >>> ns = state.State()
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

def test_kngMoves_State(self):
    """
    >>> #(1) confirm kngMovs in find_Moves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()
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
    >>> st.find_Moves()  #UNDER TEST
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

def test_sibMoves_State(self):
    """
    >>> #(1) confirm sibMovs in find_Moves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()
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
    >>> st.find_Moves()  #UNDER TEST
    True
    >>> len( st.movesD['sib'] ) == 2 # 
    True
    >>> st.movesD['sib'][1]  == Move(crd=Crd(suit='C', valu=5), stkNme='T4')
    True
    >>> st.movesD['kng'] == []
    True
    
    """
    pass

def test_fndMoves_State(self):
    """
    >>> #(1) confirm fndMoves in find_Moves().
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()
    >>> #   EXPECTED MOVE DATA
    >>> t_ace = Crd( 'C', 1)
    >>> t_sts = Status(t_ace, True, 'T0')  # expect this Ace.
    >>> t_stsL = []
    >>> t_stsL.append(t_sts)
    >>> #   EXPECTED NO MOVE DATA
    >>> junk = Move(Crd('TEST', 4), 'TEST')
    >>> st.movesD['sib'].append(junk)   # PRELOAD <dict> to assure it is cleared on find_Moves() call.
    >>> t_stsL.append(Status(Crd('H', 1), True, 'T2'))  # no move: buried
    >>> t_stsL.append(Status(Crd('H', 2), True, 'T2'))
    >>> st.populate(t_stsL)
    >>> #      SETUP COMPLETE
    >>> st.find_Moves()  #UNDER TEST
    True
    >>> st.movesD['kng']  
    []
    >>> st.movesD['sib']  # junk movesD cleared
    []
    >>> st.movesD['fnd'] == [Move(crd=Crd(suit='C', valu=1), stkNme='C')]
    True
    
    """
    pass

def test_new_populate_State(self):
    """
    >>> # confirm populate works using new namedtuple Status.
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()  # crd2OD & stkOD
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
    >>> t6.head  # fndMove() should  walk thru the entire deck.
    Crd(suit='C', valu=1)
    >>>  # (2) **************** shuffled
    >>> sfl = state.FullState()
    >>> t6 = sfl.stkOD['T6']
    >>> t6.head  != Crd(suit='C', valu=1)
    True
    >>>
    >>> import state
    >>> from h import *
    >>> ff = state.FullFoundations()
    >>> ff.fndCnt == 52
    True
    >>> ff.stkOD['S'][0] == Crd(suit='S', valu=1)
    True
    >>> ff.stkOD['S'].head == Crd(suit='S', valu=13)
    True
    >>> ff.stkOD['C'].head == Crd(suit='C', valu=13)
    True
    >>>    
    
    """
    pass

if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
