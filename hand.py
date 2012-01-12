#hand.7.7.2
#MOD 7.7 enhanced State


from h import *
from  time import  clock  
import state,  copy
import logging
import logging.config

#########################################################
class Hand:
    """ a Hand selects and initiates State.Moves until there are no more Moves: either state.stymied or state.WON.
    """
    def __init__(self, mystate=state.State(),  tag=None):
        """ """
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
    def play_1_Set(self,  N_hands=50,   logger=None):
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
    
    def play_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
    
        """        
        if not logger:  logger = logging.getLogger('myW')
        if not state: state = self.state
        
        hCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        mCntr = Counter(f=0,  k=0,  s=0)
        startClk =  clock()
        
        still_has_Movs = True  
        while still_has_Movs:
            if logger:
                logger.info(self.state.seeTops())
            while self.fndMove(state,  logger):  #do a whole seq if possible.
                mCntr['f'] += 1
                movsL =  self.fndMovesL
                if logger:
                    logger.info("--fndMove.{} now sees {} fndMoves:{}...".format(self.tag, len(movsL), movsL[:2]))
                self.state.move(self.fndMovesL[0], logger)
                
            if self.sibMove(state,  logger):  # do one, then look for fndMove
                mCntr['s'] +=  1
                movsL =  self.sibMovesL
                if logger:
                    logger.info("--sibMove.{} now sees {} sibMoves:{}...".format(self.tag, len(movsL), movsL[:2]))
                self.state.move(self.sibMovesL[0], logger)
                continue  #bypasses kngMove
                
            if self.kngMove(state,  logger):  #do at least one, maybe spawn a play_1_hand; then look for fndMove
                mCntr['k'] +=  1                                
                movsL = self.kngMovesL
                if logger:
                    logger.info("--kngMove.{} now sees {} kngMoves:{}...".format(self.tag, len(movsL), movsL[:1]))                    
                self.state = self._do_best_kngMove(movsL,  logger)

            #refresh and try again:
            if self.state.fndCnt ==  52:
                break
            still_has_Movs = (self.fndMove(state,  logger)\
                or  self.kngMove(state,  logger)\
                or self.sibMove(state,  logger))
                        
        hCntr['msClk'] = (clock() - startClk) *  1000
        hCntr['winCnt'] = 1 if state.haveWon else 0
        #assert  mCntr['f'] ==  state.fndCnt
        hCntr['fCnt'] = mCntr['f']  #   MOD:   state.fndCnt
        hCntr['nCnt'] = 1
        

        if logger: logger.warn("  **** Hand.{4} finished:(f,n,w,ms)-({2:>2}, {0[nCnt]}, {0[winCnt]}, {0[msClk]:3.2f}): Moves(N,f,k,s)-({3}, {1[f]:2}, {1[k]:2}, {1[s]:3}) ***************".format(  dict( hCntr) ,  dict(mCntr),  state.fndCnt,  sum(mCntr.values()),  self.tag))

        return hCntr

    #----------------------------------------------------------------------
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
        tstCntr += h.play_1_Set(setCnt)
        
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
    #doctest.testfile("hand_testdocs.py"
    
    



