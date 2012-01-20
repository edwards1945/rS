#hand_7.7.6
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
        self.hCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        mCntr = Counter(f=0,  k=0,  s=0)
        
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
    
    def play_Hand(self,  _state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        
        RETURNS hCntr(  winCnt=0, nCnt=0, fCnt=0, msClk=0)
        """        
        if not logger:  logger = logging.getLogger('myW')
        if not _state:
            _state = self.state
        
        self.hCntr.clear()  # = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        startClk =  clock()
        if logger:            
            _top =  _state.seeHeads()
            logger.warn('Beg:{0}-{1}'.format( self.tag, _top))
        
        _state.select_Moves(self,  logger)
        
        #WRAPUP     
        clk = self.hCntr['msClk'] = (clock() - startClk) *  1000
        win = self.hCntr['winCnt'] = 1 if _state.isWin else 0
        fnd = self.hCntr['fCnt'] = _state.fndCount
        n = self.hCntr['nCnt'] = 1
        tag = self.tag
        
        if logger:
            msg_hand = "  **** Hand.{tag} finished:(w,n,f,ms)-({win}, {n:>2}, {fnd:2}, {clk:3.2f})".format(  ** locals())
            _top =  _state.seeHeads()

            #msg_hand = "  **** Hand.{4} finished:(w,n,f,ms)-({0[winCnt]}, {0[nCnt]}, {2:>2}, {0[msClk]:3.2f}): Moves(N,f,k,s)-({3}, {1[f]:2}, {1[k]:2}, {1[s]:3})".format(  dict( self.hCntr) ,  dict(mCntr),  _state.fndCount,  sum(mCntr.values()),  self.tag)
            #_top =  _state.seeHeads()
            logger.warn('End:{0}-{1}'.format( self.tag, _top))
            logger.warn(msg_hand+ "\n")
        return self.hCntr
#----------------------------------------------------------------------
        
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
    """ one hand / multiple states."""
    logD = logging.getLogger('myD')
    logI = logging.getLogger('myI')
    logW = logging.getLogger('myW')
    t1 = hand.Hand(tag='t1')
    # ONE HAND:
    t1.state =  t1.state.getTS('t_3kng')
    t1.tag = 't3'  #NOTE local name still t1; tag only changed.
    t1.play_Hand(logger=logD)
    ## change tag and state
    #t1.tag = 't2'  #NOTE local name still t1; tag only changed.
    #t1.state =  t1.state.getTS('t_1fnd_sibs')
    #t1.play_Hand(logger=logW)
    #t1.state =  t1.state.getTS('t_52fnd')
    #t1.tag = 't1'  #NOTE local name still t1; tag only changed.
    #t1.play_Hand(logger=logW)
    
    #c = tData1.crdOD[Crd('D', 13)]
    #logI.info( "{tHand1.tag}: {c}".format( ** locals()))
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
    #doctest.testmod(verbose=False)
    #doctest.testfile("hand_testdocs.py")
    test_snippet()
    
    



