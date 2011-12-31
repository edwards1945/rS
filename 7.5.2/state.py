""" state.7.5.2.py 
#MOD 7.5.2     added moveMyItems() and DEPR moveItem()
# 111223 building a State.moveCrd() 
"""

import random
from rS import *
import  stack
import logging
import logging.config
################################################

class State:
    """
    """
    def __init__(self):
        """ rS deal of 52 states: stt @ (crd, loc, fce)>(('C', 3), ('T4', 4), True)
        
        >>> from rS import *
        >>> import state, stack
        >>> st = state.State()
        >>> len(st.crdOD) == 0
        True
        >>> len(st.stkOD)  == 11
        True
        
        """
        self.crdOD =  OrderedDict()
        self.stkOD =  OrderedDict( [(nme, stack.Stack(nme)) for nme in  STACKS])
        pass
    #----------------------------------------------------------------------
    def moveCrd(self,  crd, to_stk):
        """
        >>> from rS import *
        >>> import state, stack
        >>> st = state.State()
        >>> crd =Crd('S', 5)
        >>> stk = st.stkOD['T5']
        >>> stk.PUSH(crd)
        >>> st.crdOD[crd] = Stt(Loc(stk, stk.index(crd)), False, crd)
        >>> to_stk = st.stkOD['T3']
        >>> # ***********  setup complete 
        >>> st.moveCrd(crd, to_stk)
        >>> st.crdOD[crd].loc.stk.nme == 'T3' 
        True
        >>> st.crdOD[crd].loc.ndx == 0
        True
        """
        _moveCrd(self, crd, to_stk)
        
    #----------------------------------------------------------------------
def _moveCrd(state, crd,  to_stk):
    """ move me, a Crd, from my State's Stack to another Stack: update my State with new fce and Location.
    
    """
    #tests in State.moveCrd()
    #----------------------------------------------------------------------
    def updateStt(state, crd, to_stk):
        """ updates & RETURNS a Card's state. REQR: crd now in to_stk.
        
        """
        assert crd in  to_stk, "crd[{}] not in stk[{}]]".format(crd,  to_stk)
        ret  =  Stt(Loc(to_stk,  to_stk.index(crd)),  True,  crd)
        return  ret
    #----------------------------------------------------------------------    
    state.crdOD[crd].loc.stk.moveMyItems(crd, to_stk)  # >> crd now in new stack
    new_stt = updateStt(state, crd,  to_stk)
    state.crdOD[crd] = new_stt    
        
class FullState(State):
    """ shuffled or sequenced rS state.
    
    >>> from rS import *
    >>> import state, stack
    >>> st = state.FullState(False)
    >>> stt = st.crdOD[Crd('S', 2)] 
    >>> len(stt.loc.stk) == 6
    True
    >>> stt.fce
    False
    """
    
    def __init__(self, shuffle=True):
        State.__init__(self)
        #BUILD RUSSIAN ROULETTE INIT STATE
        def build_full(self, shuffle ):
            """ """
            STACK_FACE_DICT = OrderedDict(sorted({'T0':[UP]
                                          , 'T1': 1 * [False] + 5 * [True]
                                          , 'T2': 2 * [False] + 5 * [True]
                                          , 'T3': 3 * [False] + 5 * [True]
                                          , 'T4': 4 * [False] + 5 * [True]
                                          , 'T5': 5 * [False] + 5 * [True]
                                          , 'T6': 6 * [False] + 5 * [UP]
                                          ,  'S': [],  'H': [], 'D': [], 'C': []
                                          }.items(), key=lambda t: t[0])) #{'T0':[True], 'T1':[False, True, True, True, True, True], ,,,}
            crd52L = [Crd(s, v) for s in  SUITS for  v in  VALUES ]              
            if shuffle: random.shuffle(crd52L)
            crdG = (crd for  crd in  crd52L)
            
            # ****** now Glue or Move crds to stacks
            for stk_nme,  fceL in STACK_FACE_DICT.items():
                # NOTE: the length of each fceL determines the State:loc, fce, crd
                for fce in  fceL:  #this is the pacer, the sync driver
                    crd =  crdG.__next__() # want new_crd from crd52L
                    stk = self.stkOD[stk_nme]
                    stk.PUSH(crd)  # want to stk.PUSH(new_crd)
                    new_stt =  Stt(Loc(stk,  stk.top_ndx), fce, crd)  # build new Stt
                    self.crdOD[crd] =  new_stt  # want to crdD[crd] = new_stt
                    pass      
            pass
    
        #----------------------------------------------------------------------    
        build_full(self,  shuffle)
        
if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("deal.print.txt")
    doctest.testfile("state_testdocs.py")
