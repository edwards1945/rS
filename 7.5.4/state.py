""" state.7.5.4.py 
""" 
#MOD 7.5.4
#     111225 State has new OD, crd2OD: notice crd<s>, aleady populated with 52 cards
#     111225  adding TestStates
#     111225 ADDEd rS,namedtuple Ppu to avoid py name conflict with Pop
#     111225 DEPR  moveCrd() for NEW moveCrd2Nme() 
#     111225 CHANGED nt Mov FROM Mov(crd, to_stk) TO Mov(crd, stkNme)
#            because (1) seeing a Mov shows stak name and (2) it doesn't show ALL the items in the stk.


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
        >>> len(st.crd2OD) == 52
        True
        >>> len(st.stkOD)  == 11
        True
        
        """
        self.crdOD =  OrderedDict()
        self.crd2OD = OrderedDict([(Crd(s, v), None) for s in  SUITS for  v in  VALUES ] ) #MOD 7.5.4
        self.stkOD =  OrderedDict( [(nme, stack.Stack(nme)) for nme in  STACKS]) 
        pass
    #----------------------------------------------------------------------
    def moveCrd2Nme(self,  mov2):  #MOD 7.5.4
        """ faceUP Crd || Crds >TO> StackNme:
        
        # tests include:
        >>> ts = TS2()
        >>> # ********** BASIC: tbl TOP  >TO> tbl_top
        >>> ts.mov2_1
        Mov2Nme(crd=Crd(suit='S', valu=5), stkNme='T3')
        >>> ts.moveCrd2Nme(ts.mov2_1)  # UNDER TEST
        >>> ts.crd2OD[ts.mov2_1.crd].loc
        Loc(stk=[Crd(suit='S', valu=6), Crd(suit='S', valu=5)], ndx=1)
        
        >>> # ********** BASIC: tbl SLICE >TO> tbl_top
        >>> ts.mov2_2
        Mov2Nme(crd=Crd(suit='C', valu=1), stkNme='T0')
        >>> ts.ret2_2
        Stt(loc=Loc(stk=[Crd(suit='C', valu=1), Crd(suit='H', valu=10)], ndx=0), fce=True, crd=Crd(suit='C', valu=1))
        >>> ts.moveCrd2Nme(ts.mov2_2)  # UNDER TEST
        >>> ts.crd2OD[Crd('C', 1)] == ts.ret2_2
        True
        """
        def updateStt(self, crd, to_stk):
            """ updates & RETURNS a Card's state. REQR: crd NOW in to_stk.
            """
            assert crd in  to_stk, "crd[{}] not in stk[{}]. moveCrd2Nme didn't work.".format(crd,  to_stk)
            ret  =  Stt(Loc(to_stk,  to_stk.index(crd)),  True,  crd)
            return  ret
        #----------------------------------------------------------------------
        crd = mov2.crd
        # doesn't handle empty state in from card.assert  self.crd2OD[crd].fce,  "WARNING: State.moveCrd2Nme CRD {0.crd} is faceDOWN. Can't move a faceDOWN card to {0.stkNme} or any stack.".format( mov2)
        to_stk = self.stkOD[mov2.stkNme]
        frm_stk =  self.crd2OD[crd].loc.stk
        frm_stk.moveMyItems(crd, to_stk)  # >> crd now in new stack
        new_stt = updateStt(self, crd,  to_stk)
        self.crd2OD[crd] = new_stt    
        
    def moveCrd(self,  mov):    #DEPR: use moveCrd2Nme()  #MOD 7.5.4
        """ mov is frmCrd >> to_Stk.
        >>>
        """
        assert len(mov),  "WARNING: Don't call moveCrd with empty move list."
        #----------------------------------------------------------------------
        def updateStt(self, crd, to_stk):
            """ updates & RETURNS a Card's state. REQR: crd now in to_stk.
            
            """
            assert crd in  to_stk, "crd[{}] not in stk[{}]]".format(crd,  to_stk)
            ret  =  Stt(Loc(to_stk,  to_stk.index(crd)),  True,  crd)
            return  ret
        #----------------------------------------------------------------------
        crd,  to_stk =  mov
        frm_stk =  self.crdOD[crd].loc.stk
        frm_stk.moveMyItems(crd, to_stk)  # >> crd now in new stack
        new_stt = updateStt(self, crd,  to_stk)
        self.crdOD[crd] = new_stt    

    #----------------------------------------------------------------------
    def populate(self,  *pops):
        """populate State using one or more pops: Pop(stk_nme, fce, Crd)
        >>> from rS import *
        >>> import state, stack
        >>> st = state.State()
        >>> st.populate(Pop('T5',True, Crd('D', 6)))
        >>> # **** first assembled as argument
        >>> st.crd2OD[Crd('D', 6)].loc.stk.top_item == Crd(suit='D', valu=6)
        True
        >>> # **** now multiple pops 
        >>> p1 = Pop('T3', False, Crd('C', 13))
        >>> p2 = Pop('T3', False, Crd('C', 12))
        >>> p3 = Pop('H', True, Crd('C', 11))
        >>> st.populate(p1, p2, p3)
        >>> l1 = [(stkNme, len(st.stkOD[stkNme]))  for stkNme in STACKS  if len(st.stkOD[stkNme]) > 0]
        >>> l1 == [('T3', 2), ('T5', 1), ('H', 1)]
        True
        """
        def populate2(self,  pop2):
            """ crds already exist; typically with empty state.
            - USES crd2OD            
            """
            crd = pop2.crd
            stk =  self.stkOD[pop2.nme]
            stt =  Stt(Loc(stk,  len(stk)),  pop2.fce,  crd)
            stk.append(crd)
            self.crd2OD[crd] =  stt  # reassigns crd: valu.
            pass
        
        def populate1(self,  pop1):  # this populates the older crdOD not the new crd2OD
            """ """
            crd = pop1.crd
            stk =  self.stkOD[pop1.nme]
            stt =  Stt(Loc(stk,  len(stk)),  pop1.fce,  crd)
            stk.append(crd)
            self.crdOD[crd] =  stt  # creates key, crd, and reassigns value.
            pass
            
        for pop2 in  pops:
            populate2(self, pop2)
        
    
    #----------------------------------------------------------------------
        
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
        
class TS2(State):
    """ for use with new moveCrd2Nme()   #MOD 7.5.4"""
    def __init__(self):
        State.__init__(self)  # so all
        self.populate(Ppu('T5', True,  Crd('C', 1)))
        self.populate(Ppu('T5', True,  Crd('H', 10)))
        self.populate(Ppu('T5', True,  Crd('S', 5)))
        self.populate(Ppu('T3', True,  Crd('S', 6 )))  #
        # BASIC tbl_top TO tbl_top        
        self.mov2_1 = Mov2Nme(Crd('S', 5), 'T3')  # T3 will have two crds: S6 & S5
        # BASIC: tbl_slice >TO> tbl_top
        self.mov2_2 = Mov2Nme( Crd('C', 1), 'T0' )  # T0 will have C1 & H10
        self.ret2_2 = Stt(loc=Loc(stk=[Crd(suit='C', valu=1), Crd(suit='H', valu=10)], ndx=0), fce=True, crd=Crd(suit='C', valu=1))        
        
class TestStt1(State):
    """ used in now DEPR moveCrd()"""
    def __init__(self):
        State.__init__(self)  # so all 
        # mov1
        crd = Crd('S', 5)
        self.populate(Pop('T5',  True,  crd))
        to_stk = self.stkOD['T3']
        self.mov1 = Mov(crd, to_stk)
        
        

if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("deal.print.txt")
    doctest.testfile("state_testdocs.py")
