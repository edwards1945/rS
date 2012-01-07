""" state.7.6.py 
"""
# MOD 7.5.8 implemented uncovered Card in tableau set to faceUP in State and Stack
#MOD 7.5.6 working on play_1 and play_n Hands
#    111228.1325 finally rid of Stt, using newStt everywhere - Ihope.
#         and redid populate() using newStt - ie without Loc term
# #    111227  adding collections.Counters
#MOD 7.5.5 switching to Stk2(name of stack ) from Stk(actural stack ref): and all it's ramifications
##  all three moves work
#MOD 7.5.4 
#     111225 State has new OD, crd2OD: notice crd<s>, aleady populated with 52 cards
#     111225  adding TestStates
#     111225 ADDEd rS,namedtuple Ppu to avoid py name conflict with Pop
#     111225 DEPR  moveCrd() for NEW move() 
#     111225 CHANGED nt Mov FROM Mov(crd, to_stk) TO Mov(crd, stkNme)
#            because (1) seeing a Mov shows stak name and (2) it doesn't show ALL the items in the stk.


import random
from h import *
import  stack
import logging
import logging.config
################################################
class State:
    """ the meld on 11 Stacks and 52 Crds populated - read dealt - is a specific pattern.
    """
    def __init__(self):
        """ populating it's two dicts: 52 named Crds w/o state and 11 named but empty Stacks.)
        
         """
        self.crd2OD = OrderedDict([(Crd(s, v), None) for s in  SUITS for  v in  VALUES ] ) #MOD 7.5.4
        self.stkOD =  OrderedDict( [(nme, stack.Stack(nme)) for nme in  STACKS]) 
        pass
    #----------------------------------------------------------------------
    @property
    def isEmpty(self):
        return len(self) == 0
    @property
    def fndCnt(self):
        return sum([len(self.stkOD[nme]) for nme in FOUNDATIONS])
    @property
    def haveWon(self):
        return  True if self.fndCnt ==  52 else False
    def seeTops(self):
        """ returns formated str of top 11 stacks."""
        x =  lambda stk: stk[-1] if stk else None
        t = [ (nme,  x(stk)) for nme,  stk in  list(self.stkOD.items())]
        ret = 'Top-'
        for top in  t:
            if top[1]:
                ret += "{0}:{1.suit}{1.valu}, ".format(top[0], top[1])
            else:
                ret +=  "{0}:--,".format(top[0], top[1])
        return ret
        
    def move(self,  mov2, logger=None):  #MOD 7.5.4
        """ faceUP Crd[s] >TO> StackNme:
        CALLED from Hand.
 
        """
       #
       # the call  frm_stk.moveMyItem() handles the <dict> stkOD pop and push
       # # snd updates the <dict> crd2OD via the passed function: updateItem_function().
        
        crd = mov2.crd
        to_stk_nme =  mov2.stkNme
        to_stk = self.stkOD[to_stk_nme]
        to_stk_orig_top_crd = to_stk.top_item
        frm_stk_nme =  self.crd2OD[crd].stkNme
        frm_stk = self.stkOD[frm_stk_nme]
        
        imsg = "\n<<[{}]-{}\n...[{}]-{}\n>>[{}]-{}".format( frm_stk_nme, frm_stk, frm_stk_nme,  crd, to_stk_nme,  to_stk )
        
        def updateItem_function( crd,  to_stk):
            """ """
            self.crd2OD[crd] = newStt(to_stk.name,  True,  crd)
                  
        frm_stk.moveMyItems(crd, to_stk,  updateItem_function)  # >> crd now switched & newStt updated.
        
        imsg += "\n>>[{}]-{}".format(to_stk_nme,  to_stk )
        if logger:
            logger.debug("**** moved {}-[{}] onto [{}] {}  ****************".format(crd, frm_stk_nme, to_stk_nme, to_stk_orig_top_crd))            
            logger.debug(imsg)
            #logger.info(self.seeTops())
        pass    
    #----------------------------------------------------------------------
    def populate(self,  newSttL):
        """populate State using a <list> one or more newStts: newStt(stk_nme, fce, Crd)
        """
        for nxt in  newSttL:
            crd = nxt.crd  
            stk_nme = nxt.stkNme  
            # DEPR Mod 7.5.6 WAS: stt =  Stt(Loc(stk,  len(stk)),  newStt.fce,  crd)
            self.crd2OD[crd]  =   newStt( stk_nme, True, crd )  # all top cards are true.
            self.stkOD[stk_nme].append(crd)  # append makes every new card the top MIGHT TRY Stack.moveMyItems()
            pass
          
        
    
    #----------------------------------------------------------------------
        
class FullState(State):
    """ shuffled or sequenced rS state.  
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
            VALUES.reverse()  # TO GET T6 with C-Ace on top.
            crd52L = [Crd(s, v) for s in  SUITS for  v in  VALUES ]              
            if shuffle: random.shuffle(crd52L)
            crdG = (crd for  crd in  crd52L)
            
            # ****** now Glue or Move crds to stacks
            for stk_nme,  fceL in STACK_FACE_DICT.items():
                # NOTE: the length of each fceL determines the State:loc, fce, crd
                for fce in  fceL:  #this is the pacer, the sync driver
                    crd =  crdG.__next__() # want new_crd from crd52L
                    #stk = self.stkOD[stk_nme]
                    self.stkOD[stk_nme].PUSH(crd)  # want to stk.PUSH(new_crd)
                    #new_stt =  newStt(stk_nme, fce, crd)  # build newStt
                    self.crd2OD[crd] =  newStt(stk_nme, fce, crd)
                    pass      
            return  self
    
        #----------------------------------------------------------------------    
        build_full(self,  shuffle)
        
#class TS2(State):
    #""" for use with new move()   #MOD 7.5.4"""
    #def __init__(self):
        #State.__init__(self)  # so all
        #self.populate(Ppu('T5', True,  Crd('C', 1)))
        #self.populate(Ppu('T5', True,  Crd('H', 10)))
        #self.populate(Ppu('T5', True,  Crd('S', 5)))
        #self.populate(Ppu('T3', True,  Crd('S', 6 )))  #
        ## BASIC tbl_top TO tbl_top        
        #self.mov2_1 = Mov(Crd('S', 5), 'T3')  # T3 will have two crds: S6 & S5
        ## BASIC: tbl_slice >TO> tbl_top
        #self.mov2_2 = Mov( Crd('C', 1), 'T0' )  # T0 will have C1 & H10
        #self.ret2_2 = Stt(loc=Loc(stk=[Crd(suit='C', valu=1), Crd(suit='H', valu=10)], ndx=0), fce=True, crd=Crd(suit='C', valu=1))        
        
class FullFoundations(State):
    """ 

    """
    def __init__(self):
        State.__init__(self)
        self.populate([( newStt(nme, True, Crd(nme, i))) for i in range(1,14) for nme in SUITS])
        
if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("state_testdocs.py")
    #doctest.testfile("deal.print.txt")
