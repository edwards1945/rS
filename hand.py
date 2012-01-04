#hand.7.6


#MOD 7.6  Tested Basic play @ 2.5- 3 %
# # stops after one pass thru PLAY_1_Hand: need anonther while suit
# # Hand.state is now default to basic State()
# #implementing fnd, kng and sib moves.  111225-


from h import *
from  time import  clock  
import state
import logging
import logging.config

#########################################################
class Hand:
    """ a Hand is a series of Hand.State.Moves until there are no more Moves: either stymied or WON.
    
    aggregates all 3 kinds of Moves for a State and SHIFTS one of them creating a new State.
    three kinds: fndMove, sibMove, kngMove.
       format (moves list) > ([crd, FROM_StkStt, TO_Stk], [],,):
       where [as of "rS.60.0.py module. #VER 111109.0620]
        """
    def __init__(self, mystate=state.State()):
        """ """
        logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN 
        self.state = mystate  #MOD 7.5.7
        self.fndMovesL =  []
        self.sibMovesL = []  
        self.kngMovesL =  []
        
    #----------------------------------------------------------------------
    def PLAY_1_Set(self,  N_hands=50,   logger=None):
        """PLAYS  1 Set: N Hands, and REPORTS and RETURNS setStats: won, foundationCnt, handCnt
        
        One Hand FINDS & EXECUTES Moves until stymied or WON.    
        """
        if not logger: logger = logging.getLogger('MyINFO')
        #  myDEBUG OR myINFO OR myWARN
        setCntr =  Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0, std=0)
        for n in  range(N_hands):
            self.state = state.FullState(True)  #new shuffled state.
            setCntr += self.PLAY_1_Hand(logger=logger)            
            pass
            
        n = nCnt =  setCntr['nCnt']
        f = setCntr['fCnt']
        dt = setCntr['msClk']
        w =  setCntr['winCnt']
        winMean = w / n  # mean
        std = calculate_std2(nCnt, winMean)
        setCntr['std'] =  std  # new
        ret = "  **** {:2} WINS mean/std [{:.1%}/{:1.2}]  in {} HANDS; {} FndCnt @AVG:fnd:{:.1f} & AVG:ms:{:3.1f}.\n".format( w, std, w / n ,  n, f,  f / n,  dt / n )
        if logger: logger.warn(ret)
        return  setCntr
    
    def PLAY_1_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        RETURNS HndStat(won, fCnt)
    
        """        
        if not logger:  logger = logging.getLogger('myWARN')
        #  myDEBUG OR myINFO OR myWARN
        if not state:
            state = self.state    #MOD 7.5.6
        hCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        mCntr = Counter(f=0,  k=0,  s=0)
        startClk =  clock()
        
        # MOD 7.5.8 111230 0640 just beginning, while has_Movs not implemented
        has_fndMov = self.fndMove(state,  logger)  
        has_kng_Mov =  self.kngMove(state,  logger)
        has_sibMov = self.sibMove(state,  logger)
        
        hasMovs = has_fndMov or  has_kng_Mov or has_sibMov
        while hasMovs:           
            while self.fndMove(state,  logger)   :  #MOD 30.1150>and mCntr['k']  <=  52:  #keep this while, rapidly does whole seq
                mCntr['f'] += 1
                self.state.move(self.fndMovesL[-1], logger)
                #has_fndMov = self.fndMove(state,  logger)       
            while self.kngMove(state,  logger):  #MOD 30.1150> and mCntr['k']  <=  24:
                mCntr['k'] +=  1
                self.state.move(self.kngMovesL[-1], logger)
                #has_kng_Mov =  self.kngMove(state,  logger)
            while self.sibMove(state,  logger):  #MOD 30.1150> or mCntr['s']  >  200:
                mCntr['s'] +=  1                   
                self.state.move(self.sibMovesL[-1], logger)
                #has_sibMov = self.sibMove(state,  logger)
                
            has_fndMov = self.fndMove(state,  logger)  
            has_kng_Mov =  self.kngMove(state,  logger)
            has_sibMov = self.sibMove(state,  logger)
            
            hasMovs = has_fndMov or  has_kng_Mov or has_sibMov
                 
        
        hCntr['msClk'] = (clock() - startClk) *  1000
        hCntr['winCnt'] = 1 if state.haveWon else 0
        #assert  mCntr['f'] ==  state.fndCnt
        hCntr['fCnt'] = state.fndCnt
        hCntr['nCnt'] = 1
        if logger: logger.info("  **************** Hand (f,n,w,ms)-({0[fCnt]:>2}, {0[nCnt]}, {0[winCnt]}, {0[msClk]:3.2f}): Moves(f,k,s)-({1[f]:2}, {1[k]:2}, {1[s]:3})\n\n".format(  dict( hCntr) ,  dict(mCntr)))
        return hCntr

    def kngMove(self, state, logger=None):
        """SETS self.kngMovesL  RETURNS True if there are moves.
        
        - king IsFaceUp, in a tableau, and not its first card moves to an empty tableau.
        """
        # tests in hand_testdocs.py testHand.test_kngMove()
        
        del self.kngMovesL[:]
        # FROM RULES: tops
        RULE_stk_IsEmpty =  lambda nme:  state.stkOD[nme].isEmpty
        # TO RULES: Kings
        RULE_crd_Is_in_tbl = lambda new_stt: new_stt.stkNme[0] ==  'T'
        RULE_crd_Is_faceUP =  lambda new_stt: new_stt.fce
        RULE_crd_not_first_crd =  lambda crd,  stt: state.stkOD[stt.stkNme].index(crd) >  0
                
        # TO Stack
        _empty_tbl_stkL = [ (nme)  for nme in  TABLEAUS
                        if RULE_stk_IsEmpty(nme)]
        
        if _empty_tbl_stkL:
            
            # FROM King
            _kng_crdL = [(crd, state.crd2OD[crd])
                         for crd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)]]
            _faceUP_tbl_kngL = [ (stt.stkNme , crd)
                        for crd, stt in  _kng_crdL
                           if stt
                           and RULE_crd_Is_faceUP(stt)
                           and RULE_crd_not_first_crd(crd,  stt)
                           and RULE_crd_Is_in_tbl(stt)]
            _movL =  [(Mov( kng_crd,  mty_nme))
                           for kng_nme, kng_crd in  _faceUP_tbl_kngL
                           for mty_nme in  _empty_tbl_stkL
                           if kng_nme != mty_nme]
            for _mov in  _movL:
                self.kngMovesL.append( _mov) 
            
        return  len(self.kngMovesL ) >  0
           
    def fndMove(self, state, logger=None):
        """SETS self.fndMovesL  RETURNS True if there are moves.
        
        - faceUP, top_crd in tableau moves to  foundation top_crd if tbl_Crd is older sib of fnd_Crd. 
        """# tests in hand_testdocs.py
        
        #NOTE: This and its brothers are easy to understand but they may be costly in processing time: and redundant ODict calls.
        
        #self.fndMovesL 
        RULE_topNotEmpty =  lambda nme:  not state.stkOD[nme].isEmpty
        RULE_tbl_IsAce = lambda tbl_crd: tbl_crd.valu ==  1
        RULE_tbl_fnd_tops_Match =  lambda tbl_crd , fnd_crd  :  tbl_crd == fnd_crd._replace(valu=fnd_crd.valu+1)
        #RULE_fnd_PossibleMoves =  lambda tbl_topL:  tbl_topL  #  empty foundations can exist
        
        del self.fndMovesL[:]
        
        # FROM not empty tableau top
        not_mty_topCrdL = [(state.stkOD[nme].top_item)
                       for nme in  TABLEAUS
                       if RULE_topNotEmpty(nme)]
        # TO foundation
        not_mty_fnd_topCrdL = [(state.stkOD[nme].top_item)
                      for nme in  FOUNDATIONS
                      if RULE_topNotEmpty(nme)]  #excludes empty foundations; but tabl aces will fill them.
        
        if not_mty_topCrdL:  # at least one topCrd
            for tbl_crd in  not_mty_topCrdL:
                if RULE_tbl_IsAce(tbl_crd):  #special case: avoid fnd_crd.ndx==None
                    self.fndMovesL.append(Mov( tbl_crd,  tbl_crd.suit))
                else: 
                    for fnd_crd  in  not_mty_fnd_topCrdL:
                        if RULE_tbl_fnd_tops_Match( tbl_crd,  fnd_crd):
                            self.fndMovesL.append(Mov( tbl_crd,  tbl_crd.suit))
                            
        # assert from is not in foundation 
        return  len(self.fndMovesL ) >  0
        
    def sibMove(self, state, logger=None):
        """ SETS self.sibMovesL: RETURNS True if there are moves.
        
        - faceUP, buried or not, sib_crd in another tableau moves to a tableau top_crd that can't be an ace.
        """# TESTS in hand_testdocs.py
        #makeStk = lambda nme: state.stkOD[nme]
        
        RULE_topNotEmpty =  lambda stk:  not stk.isEmpty
        RULE_sibFaceUp =  lambda stt: stt.fce
        RULE_sib_Not_In_Foundation = lambda stk: stk.name[0] == 'T' 
        RULE_sibDiffTbl =  lambda tbl_stk,  sib_stk : tbl_stk.name !=  sib_stk.name
        
        del self.sibMovesL[:]
        
        # TO not empty or ace tableau top
        not_mty_stkL = [(stk) for nme,  stk in  ((nme, state.stkOD[nme])
                       for nme in  TABLEAUS)
                       if RULE_topNotEmpty(stk)]
        # FROM faceUPsib
        
        for tbl_stk in  not_mty_stkL :
            top_crd =  tbl_stk.top_item
            if top_crd.valu !=  1:  # no sib for an Ace 
                # REFACT: maybe do something if it is an ace
                sib_crd = top_crd._replace(valu=top_crd.valu-1)
                sib_stt = state.crd2OD[sib_crd]
                if sib_stt:  # could be empty stack in TESTING.: 
                    sib_stk =  state.stkOD[sib_stt.stkNme]
                    if (RULE_sibFaceUp(sib_stt)\
                        and RULE_sibDiffTbl(sib_stk, tbl_stk)\
                        and RULE_sib_Not_In_Foundation(sib_stk)):                        
                            mov =  Mov(sib_crd, tbl_stk.name)                    
                            self.sibMovesL.append(mov)  
        return  len(self.sibMovesL )  >  0  
        
  
            
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
        tstCntr += h.PLAY_1_Set(setCnt)
        
    n = tstCntr['nCnt']
    msg = ( "Test - {: .1%}/{:.1%} WINS:AVG: {:<.1f} FndMovs in {:<4.1f}ms  for {} Games of {} Hands ***********\n".format(tstCntr['winCnt']/n, tstCntr['std'] / n, tstCntr['fCnt']/n, tstCntr['msClk'] /n,  gmeCnt, setCnt ))
    
    print(msg)
    f.write(msg)
    f.close()
    
    

      
#----------------------------------------------------------------------
if __name__ == "__main__":
    logging.config.fileConfig('myConfig.conf')        
    import doctest
    doctest.testmod(verbose=False)
    #doctest.testfile("hand_testdocs.py"
    
    



