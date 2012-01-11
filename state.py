""" state.7.7.1.py 
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
        """ RET: <list>  ( stkNme, topCrd) for stk types: FND | TBL or all stacks.
        """
        # NOTE: stk_typeStr just uses stk_typeStr[0] against 'f' or 't'

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
        self.movesD = {'fnd': list(), 'kng': list(),  'sib': list()}  # NEW 7.7
        self.crdOD = OrderedDict([(Crd(s, v), None) for s in  SUITS for  v in  VALUES ] ) 
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
    def move(self,  a_Move, logger=None): 
        """ Move(Crd, stkNme).
        has a lot of logging for my debugging and monitoring. """
       # NOTE: NO checking the Move.
       #


        if logger:
            logger.info("**** moved {0}-[...] onto [{1}] ...  ****************".format(crd, to_stk_nme))
                
        frmCrd = a_Move.crd
        frmSts =  self.crdOD[frmCrd]
        frmStk = self.stkOD[frmSts.stkNme]
        frmSlice = frmStk[frmStk.index(frmCrd):]

        toStk_nme =  a_Move.stkNme
        toStk = self.stkOD[toStk_nme]

              
        #imsg = "\n<<[{}]-{}\n...[{}]-{}\n>>[{}]-{}".format( frm_stk_nme, frm_stk, frm_stk_nme,  crd, toStk_nme,  toStk )
        
        # MAJOR CALL
        while frmSlice:
            newCrd = frmSlice.pop(0)
            newSts = self.crdOD[newCrd]
            newStkNme =  newSts.stkNme
            newSts= Status(newCrd, newSts.fce, toStk_nme)
            toStk_curHead = toStk.top_item
            # let the stackMoveMyItems handle stk pops and pushes.
            frmStk.moveItem(newCrd, toStk, logger)  #NOTE requires Stack not name.
            
            movStr = "**** moved {newCrd}-[{newStkNme}] onto [{toStk_nme}] {toStk_curHead}  ****************".format()
        if not  frmStk.isEmpty:
            newHead =  frmStk.top_item  ##REFACT??? method?
            frmStk.crdOD[crd] = Status(newHead,  True,  toStk_nme)
            
        #imsg += "\n>>[{}]-{}".format(to_stk_nme,  to_stk )
        
        if logger:
            logger.info(movStr )           
            #logger.debug(imsg)
            logger.info(self.seeTops())
        pass
    
    def test_move_newState(self):
        """ improve monitoring of moves.
        # UNDER TEST: move()
        >>> from h import *
        >>> import state, stack
        >>> ns = state.newState()
        >>> stsL = []  #Status to populate state
        >>> movsL = []
        >>> # EXPECTED GOOD MOVES
        >>> stsL.append(Status(Crd('S', 1), True, 'T0'))  #
        >>> movsL.append(Move(Crd('S', 1), 'S'))
        >>> 
        >>> ns.populate(stsL)
        >>> ns.move(movsL[0])
        
        """
    #----------------------------------------------------------------------
    def getHeadsL(self, stk_typeStr=None):
        """ RET: <list>  ( topCrd, stkNme ) for stk types: FND | TBL or all stacks.
        """
        #NOTE: the list return ORDER is reverse that of State.
        # NOTE: stk_typeStr just uses stk_typeStr[0] against 'f' or 't'

        hdCrd =  lambda stk: stk[-1] if stk else None
        typ =    stk_typeStr and stk_typeStr[0].lower()
        if typ ==  't':
            tl =   [ (hdCrd(stk),  stkNme) for stkNme,  stk in  list(self.stkOD.items()) if stkNme[0].lower()  ==  't']
        elif  typ ==  'f':
            tl =   [ (hdCrd(stk),  stkNme) for stkNme,  stk in  list(self.stkOD.items()) if stkNme[0].lower()  ==  'f']
        else:
            tl =   [ (hdCrd(stk),  stkNme) for stkNme,  stk in  list(self.stkOD.items())]
        return tl

    def findMoves(self):
        """ rebuilds fnd.., kng..., sibMoves. RET: at least one move.
        """
        _notEmpty_tblHeadsL = [ (head, nme)  for head, nme in self.getHeadsL('TBL') if head]
        hasMoves = self.fndMoves(_notEmpty_tblHeadsL) 
        hasMoves = self.kngMoves(_notEmpty_tblHeadsL)  or hasMoves
        hasMoves = self.sibMoves(_notEmpty_tblHeadsL)  or hasMoves
        return hasMoves
    
    def sibMoves(self, _notEmpty_tblHeadsL):
        """SETS self.sibMovesL &&  RETURNS True if there are moves.
        
        - faceUP, buried or not, sib_crd in tableau
        MOVES TO a notEmpty notAce tableau Crd
        IF sib,  not in head tableau or foundation and faceUP
        """
        _movsL = []
        del self.movesD['sib'] [:]  
        for   tbl_headCrd, tbl_stkNme in  _notEmpty_tblHeadsL:
            if tbl_headCrd.valu > 1:    #not Ace head card         
                _sibCrd =  Crd(tbl_headCrd.suit,  tbl_headCrd.valu - 1)  
                _sibSts =  self.crdOD[_sibCrd]
                # sib not in foundation, sib not in same tbl, sib faceUP
                if _sibSts\
                and _sibSts.stkNme != tbl_stkNme \
                and _sibSts.stkNme[0] == 'T' \
                and _sibSts.fce:
                    _mov = Move(_sibCrd,  tbl_stkNme)
                    _movsL.append(_mov)                    
        if _movsL:
           self.movesD['sib'] = _movsL
        return len(_movsL) > 0
    
    def kngMoves(self,  _notEmpty_tblHeadsL):
        """SETS self.kngMovesL &&  RETURNS True if there are moves
        
        - king Crd IsFaceUp, in a tableau, and not its first card.
       MOVES TO empty tableau."""
        _empty_tblsNmesL = [(tblNme) for xheadCrd, tblNme in  self.getHeadsL('TBL') if not  xheadCrd]  # just want stack name, so I can use tops. For kngs, tops don't signify.
        _movsL = []
        del self.movesD['kng'] [:]  
        for mt_tblNme in _empty_tblsNmesL:  #NOTE: the first if _kngCrd only None in testing State.
            for _kngCrd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)]:
                _kngSts = self.crdOD[_kngCrd]
                if _kngSts \
                and _kngSts.fce \
                and _kngSts.stkNme in [(stkNme) for crd, stkNme in _notEmpty_tblHeadsL]\
                and self.stkOD[_kngSts.stkNme].index(_kngCrd) > 0:
                    _mov = Move(_kngCrd,  mt_tblNme)
                    _movsL.append(_mov)                    
        if _movsL:
           self.movesD['kng'] = _movsL
        return len(_movsL) > 0
    
    def fndMoves(self, _notEmpty_tblHeadsL):
        """SETS movesD['fnd']  and RET True if there were moves.
               
            -  head_crd in notEmpty tableau
            MOVES TO   notEmpty_foundation head_crd
            IF tbl_Crd is older sib of fnd_Crd.
            """
        _notEmpty_fndHeadsL =  [ (head, nme)  for head, nme in self.getHeadsL('FND') if head]
        _movsL = []
        del self.movesD['fnd'] [:]  
        for  tblHead, tblNme in _notEmpty_tblHeadsL:
            if tblHead.valu ==  1:  # Ace
                _movsL.append( Move(tblHead, tblHead.suit) )      
            else:
                for  fndHead, fndNme in _notEmpty_fndHeadsL:
                    if tblHead.valu == fndHead.valu + 1 \
                    and tblHead.suit == fndNme: 
                        _movsL.append(Move(fndHead,  tblNme))
        if _movsL:
           self.movesD['fnd'] = _movsL
        return len(_movsL) > 0
        
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
