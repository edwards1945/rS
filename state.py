""" state.7.7.2.py 
"""
import random
from h import *
import  stack
import logging
import logging.config
#############################################
#-------------------------------------------------------------------------
class State():
    """ move finding and executing to State.
    """
    def __init__(self, shuffle=True):
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
       # NOTE: LITTLE checking in Move(); just assert can't move faceDOWN
       #
                
        frmCrd = a_Move.crd
        frmSts =  self.crdOD[frmCrd]
        assert  frmSts.fce , " Move ERROR: face is DOWN in Status{}".format(frmSts)
        frmStk = self.stkOD[frmSts.stkNme]
        frmSlice = frmStk[frmStk.index(frmCrd):]

        toStk_nme =  a_Move.stkNme
        toStk = self.stkOD[toStk_nme]
        
        # MAJOR CALL
        log_before_seeHeadsStr = self.seeHeads()
        log_movStr = ""
        while frmSlice:
            toStk_curHead = toStk.head  # for log
            curCrd = frmSlice.pop(0)
            curSts = self.crdOD[curCrd]
            curStkNme =  curSts.stkNme
            self.crdOD[curCrd] = Status(curCrd, curSts.fce, toStk_nme)
            # let the stackMoveMyItems handle stk pops and pushes.
            frmStk.moveItem(curCrd, toStk, logger)  #NOTE requires Stack not name.
            
            log_movStr += ("\n" +  "*" *  10 + "**** moved {curCrd}-[{curStkNme}] onto [{toStk_nme}]-{toStk_curHead}" +  "*"  * 10).format( ** locals())
            
        if not  frmStk.isEmpty:
            curHead =  frmStk.head  ##REFACT??? method name ?
            self.crdOD[curHead] = Status(curHead,  True,  toStk_nme)
            
        log_after_seeHeadsStr = self.seeHeads() 
        
        if logger:
            logger.info(log_before_seeHeadsStr)
            logger.info(log_movStr )           
            logger.info(log_after_seeHeadsStr + "\n")  #REFACT: may not want ending \n when I get to Hands & Sets
        pass
    
    def test_State(self):
        """ improve monitoring of moves.
        # UNDER TEST: move()
        # NOT TESTING findMoves()
        # EXPECTED GOOD 
        >>> from h import *
        >>> import state, stack
        >>> logger = logging.getLogger('myI')      
        >>> ##
        >>>
        """
        pass
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
    
    def kngMoves(self, _notEmpty_tblHeadsL):
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
    
    #----------------------------------------------------------------------
    def getHeadsL(self, stk_typeStr=None):
        """ RET: <list>  ( topCrd, stkNme ) for stk types: FND | TBL or all stacks.
        """
        # NOTE: the list return ORDER is reverse that of old State.
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
    def seeHeads(self):
        """ RET: formated str of  11 stack heads."""
        ret = 'Top-'
        for head, stkNme in  self.getHeadsL():
            if head:
                ret += "{stkNme}:{head.suit}{head.valu}, ".format(** locals())
            else:
                ret +=  "{stkNme}:---,".format(** locals())
        return ret
    
            
#-------------------------------------------------------------------------
class FullState(State):
    """ shuffled or sequenced rS state.  
    """    
    def __init__(self, shuffle=True):
        State.__init__(self)
        #BUILD RUSSIAN SOLITAIRE STATE 
        self.movesD = {'fnd': list(), 'kng': list(),  'sib': list()}  # NEW 7.7
        
        # build crdOD
        if shuffle: random.shuffle(CARDS52L)
        crd = CARDS52L
        fce = FACES52L
        stk = STAKES52L
        cfs = list(zip(crd,  fce,  stk))
        sts = [Status(crd,  fce, stk) for crd,  fce,  stk in  cfs]
        d = OrderedDict(zip(crd, sts))  # used in stkOD
        self.crdOD =  d
        
        # build stkOD
        self.stkOD =  OrderedDict( [(nme, stack.Stack(nme)) for nme in  STACKS])
        [self.stkOD[sts.stkNme].append(crd)  for crd,  sts in  d.items()]  # populate stkOD
        pass
       
if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("state_testdocs.py")
    #doctest.testfile("deal.print.txt")
