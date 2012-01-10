""" state.7.7.py 
"""
import random
from h import *
import  stack
import logging
import logging.config
###############################################
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
    def getTopsL(self, stk_typeStr=None):
        """ RET: <list> of [ ALL | FND | TBL]  ( stkNme, crd)
        stk_typeStr just uses stk_typeStr[0] against 'f' or 't'
        """

        x =  lambda stk: stk[-1] if stk else None
        typ =    stk_typeStr and stk_typeStr[0].lower()
        if typ ==  't':
            tl =   [ (nme,  x(stk)) for nme,  stk in  list(self.stkOD.items()) if nme[0].lower()  ==  't']
        elif  typ ==  'f':
            tl =   [ (nme,  x(stk)) for nme,  stk in  list(self.stkOD.items()) if nme[0].lower()  ==  'f']
        else:
            tl =   [ (nme,  x(stk)) for nme,  stk in  list(self.stkOD.items())]
        return tl
            
    def seeTops(self):
        """ returns formated str of top 11 stacks."""
        #x =  lambda stk: stk[-1] if stk else None
        #t = [ (nme,  x(stk)) for nme,  stk in  list(self.stkOD.items())]
        ret = 'Top-'
        for top in  self.getTops():
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
        assert True
        imsg = "\n<<[{}]-{}\n...[{}]-{}\n>>[{}]-{}".format( frm_stk_nme, frm_stk, frm_stk_nme,  crd, to_stk_nme,  to_stk )
        
        def updateItem_function( crd,  to_stk,  logger):
            """ """
            self.crd2OD[crd] = newStt(to_stk.name,  True,  crd)
            if logger:
                logger.info("**** moved {0}-[...] onto [{1}] ...  ****************".format(crd, to_stk_nme))                        
                  
        frm_stk.moveMyItems(crd, to_stk,  updateItem_function,  logger)  # >> crd now switched & newStt updated.
        
        imsg += "\n>>[{}]-{}".format(to_stk_nme,  to_stk )
        if logger:
            logger.info("**** moved {}-[{}] onto [{}] {}  ****************".format(crd, frm_stk_nme, to_stk_nme, to_stk_orig_top_crd))            
            logger.debug(imsg)
            logger.info(self.seeTops())
        pass    
    #----------------------------------------------------------------------
    def populate(self,  newSttL):
        """populate State using a <list> one or more newStts: newStt(stk_nme, fce, Crd)
        """
        for nxt in  newSttL:
            crd = nxt.crd  
            stk_nme = nxt.stkNme  
            self.crd2OD[crd]  =   newStt( stk_nme, True, crd )  # all top cards are true.
            self.stkOD[stk_nme].append(crd)  # append makes every new card the top MIGHT TRY Stack.moveMyItems()
            pass
          
        
    
    #----------------------------------------------------------------------
class newState(State):
    """ move finding and executing to State.
    """
    def __init__(self, shuffle=True):
        State.__init__(self)
        self.movesD = {'fnd': list(), 'kng': list(),  'sib': list()}  # NEW
        self.crdOD = OrderedDict([(Crd(s, v), None) for s in  SUITS for  v in  VALUES ] ) #MOD 7.7
        self.stkOD =  OrderedDict( [(nme, stack.Stack(nme)) for nme in  STACKS]) 
    def populate(self,  StatusL):
        """sequencially populates State from a <list> of Status:
        this mod preserves fce
        Status(stk_nme, fce, Crd)
        """
        for sts in  StatusL:
            crd = sts.crd  
            stk_nme = sts.stkNme  
            self.crdOD[crd]  =   sts 
            self.stkOD[stk_nme].append(crd)  
    def findMoves(self):
        """ rebuilds fnd.., kng..., sibMoves.
       sib & fndMoves from tbl_heads; kngMoves from empty tableaus."""
        for nme, mL in  self.movesD.items():
            del self.movesD[nme] [:]  
        # REFACT THINK JUST movesD[xxx] = dict(list) 
        # clear prior xxxMoves
     
        
        _notEmpty_tblHeadsL = [ (nme, head)  for nme, head in self.getTopsL('TBL') if head]
      
        for nme, head in _notEmpty_tblHeadsL:
            if head and head.valu ==  1:  #Ace
                aceMoves(nme,  head)
                
        fndMoves(_notEmpty_tblHeadsL)
        findKngMoves()  #SMELLS: WASTED LOOP
        
    def kngMoves(self):
        """SETS self.kngMovesL &&  RETURNS True if there are moves
        - king IsFaceUp, in a tableau, and not its first card.
       Moves(kng,empty tableau)."""
        # crd moves TO empty_tblsNme in:
        _empty_tblsNmesL = [(tblNme) for tblNme, xheadCrd in  self.getTopsL('TBL') if not  xheadCrd]  # just want stack name, so I can use tops. For kngs, tops don't signify.
        
        # KING Crd moved TO empty_tblsNme:
        _full_tbl_NmesL =  [(tblNme) for tblNme, xheadCrd in  self.getTopsL('TBL') if  xheadCrd]  # just want stack name, so I can use tops. For kngs, heads don't signify.
          
        _faceUP_not1st_tbl_kngL = [(crd) \
                     for crd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)] \
                     for sts in self.crdOD[crd] \
                     if sts.fce \
                     and sts.stkNme in _full_tbl_NmesL\
                     and self.stkOD[kngSts.stkNme].index(kngCrd) >  0]        
        # MOVES 
        _movsL = [Move(kngCrd,  mtTbl) for kngCrd in  _faceUP_not1st_tbl_kngL for  mtTbl in  _empty_tblsNmesL]
        self.movesd['kng'] = dict(_movsL)
        _
        
    def aceMoves(self,  stkNme, hdCrd):
        """ tbl head with valu == 1 IS a foundation move."""
        mov = Move(hd, hd.suit)
        self.movesD['fnd'].append(mov)
    def fndMoves(self, _notEmpty_tblHeads):
        """SETS movesD['fnd']  and RET True if there were moves.
               
            -MOVES  faceUP, head_crd in notEmpty tableau TO   notEmpty_foundation head_crd if tbl_Crd is older sib of fnd_Crd and not in the same tableau.
            """
        #NOTE: Ace Rule handles empty_foundation heads
        _notEmpty_fndHeadsL = [(nme,  head) for nme,  head in self.getTopsL('FND') ]
        movs =  [( tblHead,  fndNme) \
                 for tblNme,  tblHead in _notEmpty_tblHeads \
                 for fndNme,  fndHead in  _notEmpty_fndHeadsL\
                 if tblHead.valu == fndHead.valu + 1
                 and tblNme != fndNme ]
         
        
        pass
    def test_newState(self):
        """
        >>> #(1) confirm simple Ace fndMovs in findMoves().
        >>> from h import *
        >>> import state, stack
        >>> st = state.newState()
        >>> #   MOVE DATA
        >>> t_ace = Crd( 'C', 1)
        >>> t_sts = Status(t_ace, True, 'T0')  # expect this Ace.
        >>> t_stsL = []
        >>> t_stsL.append(t_sts)
        >>> #     NO MOVE DATA
        >>> junk = Move(Crd('TEST', 4), 'TEST')
        >>> st.movesD['sib'].append(junk)   # PRELOAD <dict> to assure it is cleared on findMoves() call.
        >>> # TEST LOGIC ERROR: top or head are always fceUP>>t_stsL.append(Status(Crd('D', 1), False, 'T1'))  # no move: fceDOWN
        >>> t_stsL.append(Status(Crd('H', 1), True, 'T2'))  # no move: buried
        >>> t_stsL.append(Status(Crd('H', 2), True, 'T2'))
        >>> st.populate(t_stsL)
        >>> #      SETUP COMPLETE
        >>> st.findMoves()  #UNDER TEST
        >>> st.movesD['sib']
        []
        >>> st.movesD['fnd'] == [Move(crd=Crd(suit='C', valu=1), stkNme='C')]
        True
        """
class FullState(State):
    """ shuffled or sequenced rS state.  
    """    
    def __init__(self, shuffle=True):
        State.__init__(self)
        #BUILD RUSSIAN SOLITAIRE STATE 
        # 
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
  
class FullFoundations(State):
    """ a WON state.     """
    def __init__(self):
        State.__init__(self)
        self.populate([( newStt(nme, True, Crd(nme, i))) for i in range(1,14) for nme in SUITS])
        
if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    doctest.testfile("state_testdocs.py")
    #doctest.testfile("deal.print.txt")
