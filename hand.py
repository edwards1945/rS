#hand_7.7.5
#MOD 7.7 enhanced State

from h import *
from  time import  clock  
import pickle
import copy
import logging
import logging.config

import state
import hand
#########################################################
class Hand:
    """ a Hand selects and initiates State.Moves until there are no more Moves: either state.stymied or state.WON.
    """
    def __init__(self, mystate=state.State(),  tag=None):
        """ NOTE: if mystate not given this makes a NEW simple, not FullState STATE. """
        logger = logging.getLogger('myW') #  myD, myI OR myW 
        self.state = mystate
        self._tag =  tag
        # REFACT remove these three aftr state enhances
        
    #----------------------------------------------------------------------
    @property
    def tag(self):
        return self._tag
    @ tag.setter
    def tag(self, tag):
        self._tag =  tag
    def play_Set(self,  N_hands=50,   logger=None):
        """PLAYS  1 Set: N Hands, and REPORTS and RETURNS setStats: won, foundationCnt, handCnt
        
        One Hand FINDS & EXECUTES Moves until stymied or WON.    
        """
        if not logger: logger = logging.getLogger('myW')
        #  myD OR myI OR myW
        setCntr =  Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0, std=0)
        for n in  range(N_hands):
            self.state = state.FullState(True)  #new shuffled state.
            setCntr += self.play_Hand(logger=logger)            
            pass
            
        n = nCnt =  setCntr['nCnt']
        f = setCntr['fCnt']
        fMean =  f / n
        dt = setCntr['msClk']
        dtMean = dt / n
        w =  setCntr['winCnt']
        winMean = w / n  # mean
        std = calculate_std2(nCnt, winMean)
        setCntr['std'] =  std  # new
        ret = "  **** {:2} WINS mean/std [{:.1%}/{:1.2}]  in {} HANDS; {} FndCnt @AVG:fnd:{:.1f} & AVG:ms:{:3.1f}.\n".format( w, winMean, std,  n, f,  fMean,  dtMean )
        if logger: logger.warn(ret)
        return  setCntr
    
    def play_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        
        RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        """        
        if not logger:  logger = logging.getLogger('myW')
        if not state:
            _state = self.state
        
        hCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        mCntr = Counter(f=0,  k=0,  s=0)
        startClk =  clock()
        
        if logger:
            _top =  _state.seeHeads()
            logger.warn('Beg:{0}-{1}'.format( self.tag, _top ))
        stop =  Counter(i=1)
        _has_mov =  True
        while _has_mov:
            #if logger:
                #logger.info(_state.seeHeads())
            stop['i'] +=  1
            while _state.fndMoves(_state.partial_tbl_HeadsL):  #do a whole seq if possible.
                mCntr['f'] += 1
                movsL =  _state.movesD['fnd']
                if logger:
                    logger.info("--fndMove.{} now sees {} fndMoves:{}...".format(self.tag, len(movsL), movsL[:2]))
                _state.move(movsL[0], logger)  # arbitary use [0]
                continue
                               
            if _state.sibMoves(_state.partial_tbl_HeadsL):  # do 1, then look other movs
                mCntr['s'] +=  1
                movsL =  _state.movesD['sib']
                if logger:
                    logger.debug("--sibMove.{} now sees {} sibMoves:{}...".format(self.tag, len(movsL), movsL[:1]))
                _state.move(movsL[0], logger)
                #continue  #bypasses kngMove
                
            if _state.kngMoves(_state.partial_tbl_HeadsL):  #maybe branch and play all Hands; 
                mCntr['k'] +=  1                                
                movsL = _state.movesD['kng']
                if logger:
                    msg = "==== kngMove.{0} now sees {1} kngMoves:".format(  self.tag,  len(movsL))
                    for m in movsL:
                        msg +=  "\n{}".format(m)
                    logger.warn(msg)
                    if len(movsL) > 1:
                        logger.warn('End:{0}-{1}'.format( self.tag, _top))        
                    
                
                #if len(movsL) > 1:
                    #_state.move(movsL[0],  logger)               
                    # and now leave this hand for good.
                self.branch_kngMove(_state, movsL,  logger)
                break  # the while _has_mov: loop.
                #else:
                    #_state.move(movsL[0],  logger)
            #end while _has_mov: loop
            
            if _state.isWin or  _state.isStymied:
                break  # the while _has_mov: loop.
            
            stopMax =  10
            if stop['i'] >=  stopMax:  # TESTING RESTRAINT ONLY
                if logger:
                    logger.warn('\nEXCEEDED STOP COUNT OF {0}\n'.format(stopMax))
                break
            pass # TESTING
        _has_mov = _state.find_Moves()
            
        hCntr['msClk'] = (clock() - startClk) *  1000
        hCntr['winCnt'] = 1 if _state.isWin else 0
        hCntr['fCnt'] = _state.fndCount
        hCntr['nCnt'] = 1
        
        if logger:
            msg_hand = "  **** Hand.{4} finished:(w,n,f,ms)-({0[winCnt]}, {0[nCnt]}, {2:>2}, {0[msClk]:3.2f}): Moves(N,f,k,s)-({3}, {1[f]:2}, {1[k]:2}, {1[s]:3})".format(  dict( hCntr) ,  dict(mCntr),  _state.fndCount,  sum(mCntr.values()),  self.tag)
            _top =  _state.seeHeads()
            logger.warn('End:{0}-{1}'.format( self.tag, _top))
            logger.warn(msg_hand+ "\n")
        return hCntr
#----------------------------------------------------------------------
    def branch_kngMove(self,  _state, movsL,  logger=None):
        """ play all permutations of king move list: movsL"""
        _top = _state.seeHeads()
        i = 0
        for mov in movsL:
            _base_state = copy.deepcopy(_state)
            _base_cntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
            _tag = "{self.tag}.{i}  ".format( ** locals())
            i += 1            
            if logger:  # 
                logger.warn("b@" + _tag +
                            _base_state.seeHeads() + "\n")
            _base_state.move(mov,  logger) 
            _tag = "{self.tag}.{i}".format( ** locals())
            _h = hand.Hand(_base_state,  _tag)  
            _base_cntr = _h.play_Hand(logger=logger)
        
        
    def test_play_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.  RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        >>> from h import *       
        >>> import logging
        >>> import pickle
        >>> import state
        >>> import hand
        >>> tCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0, std=0)
        >>> logW = logging.getLogger('myW')
        >>> logI = logging.getLogger('myI')
        >>> logI.info("#### now add kngMoves()  ")
        
        
        >>> logI.info("#### ts4 State has ?? king moves  AND ??!")
        >>> ts4 = state.getTS(file='ts4')
        >>> th = hand.Hand(ts4, tag='ts4')
        >>> tCntr = th.play_Hand(logger=logW)
        
        #>>> logI.info("#### ts5 State has 4 king moves  AND 4 Stymies!")
        #>>> ts5 = state.getTS(file='ts5', folder='ts5')
        #>>> th = hand.Hand(mystate = ts5, tag='ts5')
        #>>> tCntr = th.play_Hand(logger=logI)
        
        #>>> logI.info("#### ts3 State has 1 king moves  AND wins!")
        #>>> ts3 = state.getTS('ts3')
        #>>> th = hand.Hand(mystate = ts3, tag='ts3')
        #>>> tCntr = th.play_Hand(logger=logW)
        #>>> #    
        """
        pass
    #----------------------------------------------------------------------
def test_snippet():
    """ """
    ts =  state.TestStates(False)
    #ts.makeTS('tData1')
    tData1 = ts.getTS('tData1')
    tHand1 = hand.Hand(mystate=tData1, tag='tHand1')
    logI = logging.getLogger('myI')
    tHand1.play_Hand(logger=logI)
    c = tData1.crdOD[Crd('D', 13)]
    logI.info( "{tHand1.tag}: {c}".format( ** locals()))
    #assert  tData1.crdOD[Crd('S', 13)] ==  Status(Crd('S', 13),  True,  'T0')
    pass

def test():
    """ Test: PLAYS n Sets of m Hands & prints stats.
    PRINTS summary stats.
    #>>> x = hand.test()
    """    
    s =  state.FullState()
    h =  Hand(s)
    
    setCnt = 20
    gmeCnt = 50
    
    tstCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
    f =  open('testPrintout.txt', mode='a')
    
    logE = logging.getLogger('root')
    for i in range(gmeCnt):
        tstCntr += h.play_Set(setCnt,  logger=logE)
        
    n = tstCntr['nCnt']
    msg = ( "Test - {: .1%}/{:.1%} - {} WINS:AVG: {:<.1f} FndMovs in {:<4.1f}ms  for {} Games/{} Hands.\n".format(tstCntr['winCnt']/n, tstCntr['std'] / n, tstCntr['winCnt'], tstCntr['fCnt']/n, tstCntr['msClk'] /n,  gmeCnt, setCnt ))
    
    print(msg)
    f.write(msg)
    f.close()
    
    

      
#----------------------------------------------------------------------
if __name__ == "__main__":
    logging.config.fileConfig('myConfig.conf')        
    import doctest
    doctest.testmod(verbose=False)
    #doctest.testfile("hand_testdocs.py")
    
    



