#hand.7.5.5     
#MOD 7.5.5 
# #implementing fnd, kng and sib moves.  111225-

from rS import *
import state
#import  hand
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
    def __init__(self, mystate):
        """ """
        logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN 
        self.state = mystate
        self.fndMovesL =  []
        self.sibMovesL = []  
        self.kngMovesL =  []      
    #----------------------------------------------------------------------
    def PLAY_N_Hands(self,  N_hands=50,   logger=None):
        """PLAYS N Hands, which is 1 Set, and REPORTS and RETURNS setStats: won, foundationCnt, handCnt
        
        One Hand FINDS & EXECUTES Moves until stymied or WON.
        """
        if not logger: 
            logger = logging.getLogger('MyINFO')  #  myDEBUG OR myINFO OR myWARN
            
        #if logger: logger.debug("***  IN  PLAY_N_Hands")

        won =  0
        for n in  range(N_hands):
            self.state = state.State(logger)  #new shuffled state.
            hnd = self.PLAY_1_Hand(self.state, logger)
            
            setStat = SetStat(hnd.won, hnd.fCnt, N_hands)
     
        ret = "  **[{1:.1%}]** {0.won:2} WINS in {0.nCnt} HANDS; AVG:fnd:{2:.1f}.\n".format(setStat,  setStat.won/setStat.nCnt, setStat.fCnt/setStat.nCnt)
        
        if logger: logger.warning(ret)
        #if logger: logger.debug("***  OUT PLAY_hand")
        return  setStat
    
    def PLAY_1_Hand(self,  state,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        RETURNS HndStat(won, fCnt)
        
        """
        are_Moves = self.GET_moves(state,  logger)
        while are_Moves:  #returns areMoves
            self.SHIFT_a_Move(state, logger)  #  at least one move available
            are_Moves = self.GET_moves(state,  logger)
         
        _count = self.state.fnd_Count
        _won = True if _count == 52 else False           
        
        if logger: logger.info("  ** Hand COUNT:fnd:{}".format(_count))
        return HndStat(_won,  _count)
      
    def GET_moves(self, state,  logger=None):             
        """ SETS new state.fnd, kng, sibMoves and RETURNS areMoves.        
        """    
##        if not logger:  # and not logger.level: 
##            logger = logging.getLogger('myWARN')  #  myDEBUG OR myINFO OR myWARN
            
        are_Moves =  False
        
        self.fndMove(state, logger)
##        REFACT don't use these until SHIFT_a _Move implements kng and sib    
##        self.kngMove(state, logger)
##        self.sibMove(state, logger)
        
        if len(self.fndMovesL):
            are_Moves = True
            if logger: logger.info("\nfndMovesL:{0}".format(self.fndMovesL))            
##        if len(self.sibMovesL):
##            are_Moves = True            
##            if logger: logger.info("sibMovesL:{0}\n".format(self.sibMovesL))            
##        if len(self.kngMovesL):
##            are_Moves = True
##            if logger: logger.info("kngMovesL:{0}\n".format(self.kngMovesL))
        
        return are_Moves



    def SHIFT_a_Move(self,  state,  logger=None):
        """tactically SELECTS & SHIFTS one of > 0 moves. RETURNS state.fnd_Count.
        """
        # move order of preference: fnd, kng, sib
        if len(self.fndMovesL): self.state.moveCrd2Nme(self.fndMovesL[0])
        elif len(self.kngMovesL): self.state.moveCrd2Nme(self.kngMovesL[0])
        elif len(self.sibMovesL): self.state.moveCrd2Nme(self.sibMovesL[0])
            
        return  state.fnd_Count
    
    def kngMove(self, state, logger=None):
        """SETS self.kngMovesL  - king IsFaceUp_NotFirstRULE in tableau moves to a tableau topCrd.
        """
        # tests in hand_testdocs.py testHand.test_kngMove()
        
        self.kngMovesL = []
        RULE_topIsEmpty =  lambda nme:  not len(state.stkOD[nme]) 
        RULE_crdIsFaceUp_nd_NotFirst = lambda crd: state.crd2OD[crd].fce and state.crd2OD[crd].loc.ndx >  0
        
        # FROM King
        faceUP_kngL = [(crd) for crd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)] if RULE_crdIsFaceUp_nd_NotFirst(crd)]
        # TO Stack
        mty_StkL = [ (nme)  for nme in  TABLEAUS if RULE_topIsEmpty(nme)]
        
        # generator move[s] output: could be empty []
        self.kngMovesL += (Mov2Nme( kng_crd,  mty_nme)
                           for kng_crd in  faceUP_kngL
                           for mty_nme in  mty_StkL)
        pass
           
    def fndMove(self, state, logger=None):
        """SETS self.fndMovesL  - faceUP, topCrd in tableau moves to  foundation topCrd if f_Crd is younger sib of t_Crd 
        """# tests in hand_testdocs.py
        
        #NOTE: This and its brothers are easy to understand but they may be costly in processing time: Generators instead of list; and redundant ODict calls.
        RULE_topNotEmpty =  lambda nme:  len(state.stkOD[nme]) > 0
        RULE_tbl_fnd_tops_Match =  lambda f_crd,  t_crd:  t_crd == f_crd._replace(valu=f.crd.valu+1)
        
        # FROM not empty tableau top
        not_mty_topCrdG = ((nme,  state.stkOD[nme].top_item.crd)
                       for nme in  TABLEAUS
                       if RULE_topNotEmpty(nme))
        # TO foundation
        fnd_topCrdG = ( (nme,  state.stkOD[nme].top_item.crd)
                      for nme in  FOUNDATIONS)
        # generator move[s] output: could be empty []
        self.fndMovesL += (Mov2Nme( t_crd,  f_nme)
                        for f_nme, f_crd in  fnd_topCrdG
                        for t_nme,  t_crd in  not_mty_topCrdG
                        if RULE_tbl_fnd_tops_Match())
        pass
        
    def sibMove(self, state, logger=None):
        """ SETS self.sibMovesL - faceUP, buried or not, sibCrd in another tableau moves to a tableau topCrd that can't be an ace.   """# TESTS in hand_testdocs.py
        self.sibMovesL = []
        makeStk = lambda nme: state.stkOD[nme]        
        RULE_topNotEmptyorAce =  lambda nme:  len(state.stkOD[nme]) > 1
        RULE_sttFaceUp =  lambda stt: stt.fce
        RULE_sibDiffTbl =  lambda topStt,  sibStt : topStt.loc.stk.nme !=  sibStt.loc.stk.nme
        
        # TO not empty or ace tableau top
        not_mty_nmeG = ((nme,  state.stkOD[nme].top_item)
                       for nme in  TABLEAUS
                       if RULE_topNotEmptyorAce(nme))
        # FROM faceUPsib
        
        for topStkNme,  topCrd in  not_mty_nmeG :
            topStt = state.crd2OD[topCrd]
            sibCrd = topCrd._replace(valu=topCrd.valu-1)
            sibStt = state.crd2OD[sibCrd]
            if RULE_sttFaceUp(sibStt) and RULE_sibDiffTbl(sibStt, topStt):
                mov =  Mov2Nme(sibCrd, topStkNme)
                self.sibMovesL.append(mov)  # THIS WORKS: gives [Mov2Nme(...)]
                #self.sibMovesL += (mov)  #THIS DOESN'T WORK: gives [Crd(...), nme]. The other two nMove use a generator:  self.sibMovesL += gen yield
        pass    
        
  
            
    #----------------------------------------------------------------------
    def main():
        """ Run: PLAYS n Games of m sets of Hands & prints stats.
        PRINTS summary stats.
        """
        s =  state.State()
        h =  hand.Hand(s)
        
        setCnt = 5
        gmeCnt = 2
        
        tstCnt =  setCnt * gmeCnt
        gme_wins =  gme_fndCnt = tst_wins =  tst_fndCnt =  0
        for i in range(gmeCnt):
            setStat = h.PLAY_N_Hands(setCnt)
            gme_wins +=  setStat.won
            gme_fndCnt +=  setStat.fCnt
        tst_wins +=  gme_wins
        tst_fndCnt +=  gme_fndCnt
        print( "**** WIN:{: .1%}  AvgFnd:{:.1f}  in {} Games of {} Hands ***********".format(tst_wins / tstCnt,  tst_fndCnt / tstCnt,  gmeCnt,  setCnt))
        

    
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    logging.config.fileConfig('myConfig.conf')        
    import doctest
    doctest.testmod(verbose=False)
    doctest.testfile("hand_testdocs.py")
    #main()
    
    



