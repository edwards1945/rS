#hand.7.3.1     module.
#MOD 7.3.1 #Stack was Loc(nme, ndx) now Loc(nme, lng) for length; allowing lng==0

from rS import *
import state
import  hand
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
        if len(self.fndMovesL): self.state.moveCrd(self.fndMovesL[0])
        elif len(self.kngMovesL): self.state.moveCrd(self.kngMovesL[0])
        elif len(self.sibMovesL): self.state.moveCrd(self.sibMovesL[0])
            
        return  state.fnd_Count
    
    def kngMove(self, state, logger=None):
        """ SETS self.kngMovesL
        
        empty_tbl_tops CHECK4 available king cards"""
        emt_tblL = [(nme,  stt) for nme, stt in state.tbl_topD.items() if stt.crd ==  Crd_EMPTY]
        kng_sttL =  [(stt) for crd,  stt in  state.crdD.items() if crd.valu ==  13 and  stt.fce]
        mov =  [(kng_stt,  emt_nme) for emt_nme,  stt in  emt_tblL for kng_stt in kng_sttL ]
        self.kngMovesL = mov
    
    def fndMove(self, state, logger=None):
        """SETS self.fndMovesL  - faceUP, kngCrd in tableau moves to a tableau topCrd.
        """
        #tblRULE nme in TABLEAUS
        topIsEmptyRULE =  lambda nme:  not len(state.stkOD[nme]) 
        crdIsFaceUpRULE = lambda crd: state.crd2OD[crd].fce
        
        # FROM King
        faceUP_kngL = [(crd) for crd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)] if crdIsFaceUpRULE(crd)]
        # TO Stack
        mty_StkL = [ (nme)  for nme in  TABLEAUS if topIsEmptyRULE(nme)]
        
        self.fndMovesL += (Mov2Nme( f_crd,  t_nme) for f_crd in  faceUP_kngL for t_nme in  mty_StkL)
        pass
        
    def sibMove(self, state, logger=None):
        """ SETS self.sibMovesL
        - faceUP, sibCrd in another tableau moves to a tableau topCrd. 
        
        TESTS in hand_testdocs.py
        """
        #tblRULE nme in TABLEAUS
        #topNotEmptyorAceRULE: len(crd2OD[crd].loc.nme)  > 1
        #topNotEmptyorAceRULE: len(stkOD[nme])  > 1
        #crdFaceUpRULE : crd2OD[crd].fce (== True)
        #sttFaceUpRULE: lambda stt: stt.fce
        #sibDiffTblRULE needs crdStt.loc.nme != sibStt.loc.nme
        
        makeStk = lambda nme: state.stkOD[nme]        
        topNotEmptyorAceRULE =  lambda nme:  len(state.stkOD[nme]) > 1
        sttFaceUpRULE =  lambda stt: stt.fce
        sibDiffTblRULE =  lambda topStt,  sibStt : topStt.loc.stk.nme !=  sibStt.loc.stk.nme
        
        not_mty_nme = ((nme,  state.stkOD[nme].top_item) for nme in  TABLEAUS if topNotEmptyorAceRULE(nme))
        
        for topStkNme,  topCrd in  not_mty_nme :
            topStt = state.crd2OD[topCrd]
            sibCrd = topCrd._replace(valu=topCrd.valu-1)
            sibStt = state.crd2OD[sibCrd]
            if sttFaceUpRULE(sibStt) and sibDiffTblRULE(sibStt, topStt):
                mov =  Mov2Nme(sibCrd, topStkNme)
                self.sibMovesL.append(mov)
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
    #doctest.testmod(verbose=False)
    # USING rS_testdocs w/ ACCEPTS 
    doctest.testfile("hand_testdocs.py")
    #main()
    
    



