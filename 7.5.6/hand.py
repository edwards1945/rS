#hand.7.5.6     
#MOD 7.5.6
# # Hand.state is now default to basic State()
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
    def __init__(self, mystate=state.State()):
        """ """
        logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN 
        self.state = mystate  #MOD 7.5.6
        self.fndMovesL =  []
        self.sibMovesL = []  
        self.kngMovesL =  []
        self.Cntr =  Counter(['wonCnt',  'fCnt', 'nCnt'])
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
    
    def PLAY_1_Hand(self,  state=None,  logger=None):
        """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.
        RETURNS HndStat(won, fCnt)
        """
        
##        if not logger:  # and not logger.level: 
##            logger = logging.getLogger('myWARN')  #  myDEBUG OR myINFO OR myWARN
        if not state: state = self.state    #MOD 7.5.6
        hCntr =  Cntr
        hCntr['wonCnt']  = hCntr['fCnt'] =  0
        
        while self.fndMove(state,  logger):
            self.state.moveCrd2Nme(self.fndMovesL[0])
            continue       
        #while  self.kngMove(state,  logger):
            #self.state.moveCrd2Nme(self.kngMovesL[0])
            #break
        #while self.sibMove(state,  logger):
            #self.state.moveCrd2Nme(self.sibMovesL[0])
            #break
        
        if state.haveWon: hCntr['wonCnt'] = 1
        hCntr['fCnt'] = state.fndCnt
                   
        #if logger: logger.info("  ** Hand 
        return hCntr

    def kngMove(self, state, logger=None):
        """SETS self.kngMovesL  RETURNS True if there are moves.
        
        - king IsFaceUp_NotFirstRULE in tableau moves to a tableau topCrd.
        """
        # tests in hand_testdocs.py testHand.test_kngMove()
        
        del self.kngMovesL[:]
        
        #RULE_topIsEmpty =  lambda nme:  not len(state.stkOD[nme]) 
        #RULE_crdIsFaceUp_nd_NotFirst = lambda crd: state.crd2OD[crd].fce
        #RULE_tbl_crd = 'fix this'
        #RULE_crd_not_first_crd =  lambda crd: state.crd2OD[crd].crd.ndx >  0
        #RULE_PossibleMoves =  lambda l1,  l2 :  l1 and  l2
        
        ## FROM King
        #faceUP_kng_crdL = [(crd) for crd in  [Crd('S',  13), Crd('H', 13), Crd('D',  13),  Crd('C', 13)] if RULE_crdIsFaceUp_nd_NotFirst(crd)]
        ## TO Stack
        #mty_StkL = [ (nme)  for nme in  TABLEAUS if RULE_topIsEmpty(nme)]
        
        #if RULE_PossibleMoves(faceUP_kng_crdL, mty_StkL ):               
            #self.kngMovesL.append((Mov2Nme( kng_crd,  mty_nme))
                           #for kng_crd in  faceUP_kngL
                           #for mty_nme in  mty_StkL)
            
        return  len(self.kngMovesL ) >  0
           
    def fndMove(self, state, logger=None):
        """SETS self.fndMovesL  RETURNS True if there are moves.
        
        - faceUP, topCrd in tableau moves to  foundation topCrd if tbl_Crd is older sib of fnd_Crd. 
        """# tests in hand_testdocs.py
        
        #NOTE: This and its brothers are easy to understand but they may be costly in processing time: and redundant ODict calls.
        
        #self.fndMovesL 
        RULE_topNotEmpty =  lambda nme:  not state.stkOD[nme].isEmpty
        RULE_tbl_IsAce = lambda tbl_crd: tbl_crd.valu ==  1
        RULE_tbl_fnd_tops_Match =  lambda fnd_crd,  tbl_crd:  tbl_crd == fnd_crd._replace(valu=fnd_crd.valu+1)
        RULE_fnd_PossibleMoves =  lambda tbl_topL:  tbl_topL  #  empty foundations can exist
        
        del self.fndMovesL[:]
        
        # FROM not empty tableau top
        not_mty_topCrdL = [(state.stkOD[nme].top_item)
                       for nme in  TABLEAUS
                       if RULE_topNotEmpty(nme)]
        # TO foundation
        not_mty_fnd_topCrdL = [(state.stkOD[nme].top_item)
                      for nme in  FOUNDATIONS
                      if RULE_topNotEmpty(nme)]  
        
        if RULE_fnd_PossibleMoves(not_mty_topCrdL):
            for tbl_crd in  not_mty_topCrdL:
                if RULE_tbl_IsAce(tbl_crd):  #special case: avoid fnd_crd.ndx==None
                    self.fndMovesL.append(Mov2Nme( tbl_crd,  tbl_crd.suit))
                else: 
                    for fnd_crd  in  not_mty_fnd_topCrdL:
                        if RULE_tbl_fnd_tops_Match(fnd_crd,  tbl_crd):
                            self.fndMovesL.append(Mov2Nme( tbl_crd,  fnd_crd.suit))

        return  len(self.fndMovesL ) >  0
        
    def sibMove(self, state, logger=None):
        """ SETS self.sibMovesL: RETURNS True if there are moves.
        
        - faceUP, buried or not, sib_crd in another tableau moves to a tableau topCrd that can't be an ace.
        """# TESTS in hand_testdocs.py
        makeStk = lambda nme: state.stkOD[nme]
        
        RULE_topNotEmptyorAce =  lambda stk:  len(stk) > 1
        RULE_sibFaceUp =  lambda stt: stt.fce
        RULE_sibDiffTbl =  lambda tbl_stk,  sib_stk : tbl_stk.name !=  sib_stk.name
        
        del self.sibMovesL[:]
        
        # TO not empty or ace tableau top
        not_mty_stkL = [(state.stkOD[nme])
                       for nme in  TABLEAUS
                       if RULE_topNotEmptyorAce(state.stkOD[nme])]
        # FROM faceUPsib
        
        for tbl_stk in  not_mty_stkL :
            topCrd =  tbl_stk.top_item
            #topStt = state.crd2OD[topCrd]
            sib_crd = topCrd._replace(valu=topCrd.valu-1)
            sib_stt = state.crd2OD[sib_crd]
            sib_stk =  state.stkOD[sib_stt.stkNme]
            if RULE_sibFaceUp(sib_stt) and RULE_sibDiffTbl(sib_stk, tbl_stk):
                mov =  Mov2Nme(sib_crd, tbl_stk.name)
                
                self.sibMovesL.append(mov)  # THIS WORKS: gives [Mov2Nme(...)]
                #self.sibMovesL.append(mov)  #THIS DOESN'T WORK: gives [Crd(...), nme]. The other two nMove use a generator:  self.sibMovesL.append   gen yield
        return  len(self.sibMovesL )  >  0  
        
  
            
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
    
    



