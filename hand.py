#hand.7.7.2
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
        """ NOTE: if mystate not given this makes a NEW STATE. """
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
        dt = setCntr['msClk']
        w =  setCntr['winCnt']
        winMean = w / n  # mean
        std = calculate_std2(nCnt, winMean)
        setCntr['std'] =  std  # new
        ret = "  **** {:2} WINS mean/std [{:.1%}/{:1.2}]  in {} HANDS; {} FndCnt @AVG:fnd:{:.1f} & AVG:ms:{:3.1f}.\n".format( w, std, w / n ,  n, f,  f / n,  dt / n )
        if logger: logger.info(ret)
        return  setCntr
    
    def test_play_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.  RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        
        >>> import logging
        >>> import pickle
        >>> import state
        >>> import hand
        
        #>>> hand.test_snippet()        
        >>> ts = state.TestStates(False)
        >>> ts.makeTS('ts2')
        >>> ts.getTS('ts2')
        >>> th = hand.Hand(mystate=ts, tag='1')
        >>>
        
        >>> logI = logging.getLogger('myI')
        >>> th.play_Hand(logger=logI)
            
        """   
    def play_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        
        RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        """        
        if not logger:  logger = logging.getLogger('myW')
        if not state:
            state = self.state
        
        hCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        mCntr = Counter(f=0,  k=0,  s=0)
        startClk =  clock()
        
        still_has_Movs = True  # assure one time. REFACT maybe call state.moves instead.
        while still_has_Movs:
            if logger:
                logger.info(self.state.seeHeads())
            #while self.fndMove(state,  logger):  #do a whole seq if possible.
                #mCntr['f'] += 1
                #movsL =  self.fndMovesL
                #if logger:
                    #logger.info("--fndMove.{} now sees {} fndMoves:{}...".format(self.tag, len(movsL), movsL[:2]))
                #self.state.move(self.fndMovesL[0], logger)
                
            #if self.sibMove(state,  logger):  # do one, then look for fndMove
                #mCntr['s'] +=  1
                #movsL =  self.sibMovesL
                #if logger:
                    #logger.info("--sibMove.{} now sees {} sibMoves:{}...".format(self.tag, len(movsL), movsL[:2]))
                #self.state.move(self.sibMovesL[0], logger)
                #continue  #bypasses kngMove
                
            #if self.kngMove(state,  logger):  #do at least one, maybe spawn a play_1_hand; then look for fndMove
                #mCntr['k'] +=  1                                
                #movsL = self.kngMovesL
                #if logger:
                    #logger.info("--kngMove.{} now sees {} kngMoves:{}...".format(self.tag, len(movsL), movsL[:1]))                    
                #self.state = self._do_best_kngMove(movsL,  logger)

            ##refresh and try again:
            if self.state.isWin:
                break
            still_has_Movs = self.state.hasMoves
            
        hCntr['msClk'] = (clock() - startClk) *  1000
        hCntr['winCnt'] = 1 if state.isWin else 0
        #assert  mCntr['f'] ==  state.fndCnt
        hCntr['fCnt'] = state.fndCount
        hCntr['nCnt'] = 1
        
        if logger:
            msg = "  **** Hand.{4} finished:(f,n,w,ms)-({2:>2}, {0[nCnt]}, {0[winCnt]}, {0[msClk]:3.2f}): Moves(N,f,k,s)-({3}, {1[f]:2}, {1[k]:2}, {1[s]:3}) ***************".format(  dict( hCntr) ,  dict(mCntr),  state.fndCount,  sum(mCntr.values()),  self.tag)
            logger.warn(msg)
            logger.info(self.state.seeHeads())
        return hCntr

    #----------------------------------------------------------------------

def test_snippet():
    """"""
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
    """    
    s =  state.State()
    h =  Hand(s)
    
    setCnt = 50
    gmeCnt = 20
    
    tstCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
    f =  open('testPrintout.txt', mode='a')
    
    for i in range(gmeCnt):
        tstCntr += h.play_Set(setCnt)
        
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
    
    



