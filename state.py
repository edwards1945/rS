""" state_7.7.6.py 
"""
import random
from h import *
import  stack
import  copy
import  os
import  io
import pickle
import logging
import logging.config
#############################################
#-------------------------------------------------------------------------
class State():
    """ rS State: .move activities base class for various full and test States..
    """
    def __init__(self, shuffle=True):
        self.movesD = {'fnd': list(), 'kng': list(),  'sib': list()}  
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
        frmStk_nme = frmSts.stkNme
        frmStk = self.stkOD[frmStk_nme]
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
            
            log_movStr += ("\n" +  "*" *  10 + "**** moved {curCrd}-[{curStkNme}] onto [{toStk_nme}]-{toStk_curHead}" +  "*"  * 0).format( ** locals())
            
        if not  frmStk.isEmpty:
            curHead =  frmStk.head  ##REFACT??? method name ?
            self.crdOD[curHead] = Status(curHead,  True,  frmStk_nme)
            
        log_after_seeHeadsStr = self.seeHeads() 
        
        if logger:
            logger.debug(log_before_seeHeadsStr)
            logger.debug(log_movStr )           
            logger.debug(log_after_seeHeadsStr + "\n")  #REFACT: may not want ending \n when I get to Hands & Sets
        pass
    
    def find_Moves(self):
        """ rebuilds fnd.., kng..., sibMoves. RET: at least one move.
        """
        _notEmpty_tblHeadsL = self.partial_tbl_HeadsL
        # NOTE: one call vs 4: maybe better
        hasMoves = self.fndMoves(_notEmpty_tblHeadsL) 
        hasMoves = self.kngMoves(_notEmpty_tblHeadsL)  or hasMoves
        hasMoves = self.sibMoves(_notEmpty_tblHeadsL)  or hasMoves
        return hasMoves 
    #----------------------------------------------------------------------
    def select_Moves(self,  _hand, logger=None):
        """ chooses and executes moves.  The strategy is included in whiles and loops.
        """
        # INIT 
        mCntr = Counter(f=0,  k=0,  s=0)
        stop =  Counter(i=1)
        _top =  self.seeHeads()
        if logger:
            logger.info('Beg:{0}-{1}'.format( _hand.tag, _top ))
            
        _has_mov =  True  # for sure one pass
        # MAIN
        while _has_mov:
            stop['i'] +=  1  #TESTING Cntr
            while self.fndMoves(self.partial_tbl_HeadsL):  #do a whole seq if possible.
                mCntr['f'] += 1
                movsL =  self.movesD['fnd']
                if logger:
                    logger.info("--fndMove.{} now sees {} fndMoves:{}...".format(_hand.tag, len(movsL), movsL[:2]))
                self.move(movsL[0], logger)  # arbitary use [0]
                continue
                               
            if self.sibMoves(self.partial_tbl_HeadsL):  # do 1, then look other movs
                mCntr['s'] +=  1
                movsL =  self.movesD['sib']
                if logger:
                    logger.debug("--sibMove.{} now sees {} sibMoves:{}...".format(_hand.tag, len(movsL), movsL[:1]))
                self.move(movsL[0], logger)
                #continue  #bypasses kngMove
                
            if self.kngMoves(self.partial_tbl_HeadsL):  ###one for sure; maybe branch and play all Hands; 
                mCntr['k'] +=  1                                
                movsL = self.movesD['kng']
                if logger:
                    msg = "==== kngMove.{0} now sees {1} kngMoves:".format(  _hand.tag,  len(movsL))
                    for m in movsL:
                        msg +=  "\n{}".format(m)
                    logger.warn(msg)
                                   
                self.branch_kngMove(_hand, movsL,  logger)
                break  # the while _has_mov: loop. could fall thru but this is more obvious.
            #end while _has_mov: loop
            
            # EXIT 
            if self.isWin or  self.isStymied:
                if logger:
                    _top =  self.seeHeads()                   
                    logger.info('End:{0}-{1}'.format( _hand.tag, _top))  
                break  # the while _has_mov: loop.
            #TESTING EXIT
            stopMax =  20
            if stop['i'] >=  stopMax:  # TESTING RESTRAINT ONLY
                if logger:
                    logger.warn('\nEXCEEDED STOP COUNT OF {0}\n'.format(stopMax))
                break
            # FOR DEBUG
            pass 
        _has_mov = self.find_Moves()

    def branch_kngMove(self,  _hand, movsL,  logger=None):
        """ play all permutations of king move list: movsL.
        expect at least one mov.
        """
        #
        i = 1
        _base_heads = self.seeHeads()
        _base_state = copy.deepcopy(self)
        _base_tag = _hand.tag
        #_base_cntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)  #CHANGE TO ATTRIBUTE
        #_base_cntr = self.cntr
        # 
        #if logger: 
            #logger.warn("\n===newbeg@{}:{}".format( _hand.tag,      _base_heads ))
        #self.move(movsL[0], logger)
        #_new_cntr = _hand.play_Hand(self, logger=logger)
        # fall thru if other moves.
        for mov in movsL[:-1]:
            # there are more moves
            i += 1            
            _new_tag = "{_base_tag}.{i}  ".format( ** locals())
            _new_state =  copy.deepcopy(_base_state)  
            _new_state.move(mov,  logger)
            _new_state_heads = _new_state.seeHeads()
            _hand.tag = "{_hand.tag}.{i}".format( ** locals())
            _hand.tag = _new_tag  #TESTING
            if logger: 
                logger.warn("\n===newbeg@{}:{}".format( _hand.tag,      _new_state_heads ))
            _new_cntr = _hand.play_Hand(_new_state, logger=logger)
            pass
        # move and pass back to original state
        #self.tag = "{_hand.tag}.{i}".format( ** locals())
        _base_state.move(movsL[-1], logger)
        pass
    def sibMoves(self, partial_tbl_HeadsL):
        """SETS self.sibMovesL &&  RETURNS True if there are moves.
        
        - faceUP, buried or not, sib_crd in tableau
        MOVES TO a notEmpty notAce tableau Crd
        IF sib,  not in head tableau or foundation and faceUP
        """
        _movsL = []
        del self.movesD['sib'] [:]  
        for   tbl_headCrd, tbl_stkNme in  partial_tbl_HeadsL:
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
    
    def kngMoves(self, partial_tbl_HeadsL):
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
                and _kngSts.stkNme in [(stkNme) for crd, stkNme in partial_tbl_HeadsL]\
                and self.stkOD[_kngSts.stkNme].index(_kngCrd) > 0:
                    _mov = Move(_kngCrd,  mt_tblNme)
                    _movsL.append(_mov)                    
        if _movsL:
            self.movesD['kng'] = _movsL
        return len(_movsL) > 0
    
    def fndMoves(self, partial_tbl_HeadsL):
        """SETS movesD['fnd']  and RET True if there were moves.
               
            -  head_crd in notEmpty tableau
            MOVES TO   notEmpty_foundation head_crd
            IF tbl_Crd is older sib of fnd_Crd.
            """
        _notEmpty_fndHeadsL =  [ (head, nme)  for head, nme in self.getHeadsL('FND') if head]
        _movsL = []
        del self.movesD['fnd'] [:]  

        for  tblHead, tblNme in partial_tbl_HeadsL:
            if tblHead.valu ==  1:  # Ace
                _movsL.append( Move(tblHead, tblHead.suit) )      
            else:
                for  fndHead, fndNme in _notEmpty_fndHeadsL:
                    if tblHead.valu == fndHead.valu + 1 \
                    and tblHead.suit == fndNme: 
                        _movsL.append(Move(tblHead,  fndNme))
        if _movsL:
            self.movesD['fnd'] = _movsL
        return len(_movsL) > 0
    def pickleMyState(self, stateNme,  ):
        """ creates a deepcopy of self; names, pickles and RETURNS it."""
        pNme = stateNme + ".pickle"
        with  open(pNme, 'wb') as f:
            pickle.dump(self,  f,  pickle.HIGHEST_PROTOCOL) 
        with  open(pNme,  'rb') as f:
            _ts = pickle.load(f)
        return _ts
    
    #----------------------------------------------------------------------
    @property
    def fndCount(self):
        """ """
        d = self.stkOD
        return (len(d['C']) + len(d['D']) + len(d['H']) + len(d['S']) )
    @property
    def isWin(self):
        return self.fndCount == 52
    
    def _movCount(self):
        d =  self.movesD
        return (len(d['fnd']) + len(d['kng']) + len(d['sib']) )
    @property
    def hasMoves(self):
        return self._movCount() > 0
    @property
    def has_fndMove(self):
        return len(self.movesD['fnd'])
    @property
    def has_kngMove(self):
        return len(self.movesD['kng'])
    @property
    def has_sibMove(self):
        return len(self.movesD['sib'])
    @property
    def isStymied(self):
        return  self._movCount() == 0
    @property
    def partial_tbl_HeadsL(self):
        """ used in finding xxxMoves()"""
        return  [ (head, nme)  for head, nme in self.getHeadsL('TBL') if head]
    #----------------------------------------------------------------------
    def getTS(self, file,  folder=None,  shuffle=True):
        """ retreives existing pickled state OR creates new one."""
        folder =  "./{folder}/" if folder else ""           
        pNme = "{folder}{file!s}.pickle".format( ** locals())
        try:
            with  open(pNme,  'rb') as f:
                _ts = pickle.load(f)
            pass
            return _ts
        except IOError:
            #self._makeTS(file,  shuffle)
            ateststate =  FullState(shuffle)
            with  open(pNme, 'wb') as f:
                pickle.dump(ateststate,  f,  pickle.HIGHEST_PROTOCOL)                
            with  open(pNme,  'rb') as f:
                _ts = pickle.load(f)
            return _ts
        #----------------------------------------------------------------------
    def test_State(self):
        """ improve monitoring of moves.
        # UNDER TEST: move()
        # NOT TESTING find_Moves()
        # EXPECTED GOOD 
        >>> from h import *
        >>> import state, stack
        >>> logger = logging.getLogger('myI')      
        >>> ##
        >>>
        """
        pass
    
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
            tl =   [ (hdCrd(stk),  stkNme) for stkNme,  stk in  list(self.stkOD.items()) if stkNme[0].lower()  !=  't']
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
        crd =  copy.copy(CARDS52L)
        if shuffle: random.shuffle(crd)
        #crd = CARDS52L
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

            
#-------------------------------------------------------------------------
class TestStates(FullState):
    """ a series of fixed states.
    """
    def __init__(self, shuffle=True):
        """ direct from StateFull which for some reason isn't working. OR ts10.python carries the original state which confuses python."""
        FullState.__init__(self, shuffle)
        ##BUILD RUSSIAN SOLITAIRE STATE 
    
    #@property
    #def ts10(self):
        #with  open('ts10.pickle',  'rb') as f:
            #_ts10 = pickle.load(f)
        #return _ts10
         
#----------------------------------------------------------------------
def getTS(file,  folder=None,  shuffle=True):
    """ retreives existing pickled state OR creates new one."""
    folder =  "./{folder}/".format( **locals()) if folder else ""           
    pNme = "{folder}{file!s}.pickle".format( ** locals())
    try:
        with  open(pNme,  'rb') as f:
            _ts = pickle.load(f)
        pass
        return _ts
    except IOError:
        #self._makeTS(file,  shuffle)
        ateststate =  FullState(shuffle)
        with  open(pNme, 'wb') as f:
            pickle.dump(ateststate,  f,  pickle.HIGHEST_PROTOCOL)                
        with  open(pNme,  'rb') as f:
            _ts = pickle.load(f)
        return _ts
    #----------------------------------------------------------------------

    

def test_pickling(self):
    """
    >>> import os
    >>> import state, pickle
    >>> ##### are test states immutable???
    >>> ### first and existing pickle file using Class Method getTS()
    >>> ts = state.TestStates()
    
    >>> ts10 = ts.getTS('ts10', False)
    >>> ts10.crdOD[Crd('S', 13)]
    Status(crd=Crd(suit='S', valu=13), fce=True, stkNme='T3')
    >>> ts10.crdOD[Crd('S', 13)].fce
    True
    >>> sts = ts10.crdOD[Crd('S', 13)]._replace(fce=False)
    >>> ts10.crdOD[Crd('S', 13)] = sts
    >>> ts10.crdOD[Crd('S', 13)].fce
    False
    >>> ts10 =ts.getTS('ts10')  # second call: ts10 back to original
    >>> ts10.crdOD[Crd('S', 13)].fce
    True
    >>> ### now a pickle file using module function getTS()
    >>> ts2 = getTS('TEST', False)
    >>> os.remove ('TEST.pickle')
    
    >>> #### test states are immutable !!!
    >>>
  
    """
      
if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("state_testdocs.py")
    #doctest.testfile("deal.print.txt")
