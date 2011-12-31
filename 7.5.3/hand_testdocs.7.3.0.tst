 #hand_testdocs.7.3.0   module.
#MOD 7.3.0 #Stack was Loc(nme, ndx) now Loc(nme, lng) for length; allowing lng==0
 >>> from rS import  * 
 >>> import state,  hand
 >>> import logging
 >>> import logging.config
 
 #>>> logger = logging.getLogger('myINFO') #  myDEBUG OR myWARN
 #>>> #logger.debug("debug msg 1.")
 #>>> logger.info("info msg 1.")
 #>>> logger.warning("warning msg 1.")
 >>>  #### now PLAY_hands()
 #>>> s =  state.State()
 #>>> h =  hand.Hand(s)
 #>>> logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN
 #>>> count = h.PLAY_N_hands(50,  logger)
 #>>> del(h)
 #>>> del(s)
 >>>  #### now shuffled ########
 #>>>  #### now PLAY_hands()
 #>>> s =  state.State()
 #>>> h =  hand.Hand(s)
 #>>> logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN
 #>>> count = h.PLAY_N_hands(500,  logger)
 #>>> del(h)
 #>>> del(s)
 #>>>  #### now shuffled ########
 #>>> s =  state.State()
 #>>> h =  hand.Hand(s)
 #>>> logger = logging.getLogger('myINFO') #  myDEBUG, myINFO OR myWARN
 #>>> count = h.SHIFT_moves(s,  logger)
 
 >>>  ###### now multiple moves with SHIFT_moves()
 #>>> tS = state.TestState()
 #>>> h =  hand.Hand(tS) 
 #>>> logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN
 #>>> h.SHIFT_moves(tS, logger)   # count (tbl / fnd). no debug param - level is WARN
 #(0, 52)
 

 >>>  ### AS INITIZED#######
 >>> tS = state.State(TEST_FALSE)
 >>> h =  hand.Hand(tS)
 >>> logger = logging.getLogger('myWARN') #  myDEBUG, myINFO OR myWARN 
 >>> h.GET_moves(tS)  # UNDER TEST: no logger so expect default: myWARN 
 >>> h.sibMovesL 
 []
 >>> h.kngMovesL
 []
 >>> h.fndMovesL
 [(Stt(crd=Crd(suit='S', valu=1), loc=Loc(nme='T6', lng=10), fce=True, top=True), 'S')]
 
 >>>  #now SHIFT for TEST ONLY, MAKE fake moves
 >>> x = tS.SHIFT(Stt( Crd('C', 13), Loc('T0', 0), 1, 1), 'C')  # make an empty stack and see 3 kngMoves.
 >>> tCrd, tLoc, tfce,  ttop = tS.crdD[Crd('C', 6)] #Make sib acceptable and see a sibMove.
 >>> tStt = Stt(tCrd,  tLoc,  True,  False)  #fce is now UP but top still False.
 >>> tS.crdD[tCrd] =  tStt
 >>> tS.stkD[tLoc] =  tStt
 >>> h.GET_moves(tS)  # UNDER TEST: 
 >>> h.sibMovesL             
 [(Stt(crd=Crd(suit='C', valu=6), loc=Loc(nme='T2', lng=0), fce=True, top=False), 'T1')]
 >>> h.kngMovesL
 [(Stt(crd=Crd(suit='C', valu=13), loc=Loc(nme='C', lng=0), fce=True, top=True), 'T0'), (Stt(crd=Crd(suit='D', valu=13), loc=Loc(nme='T2', lng=6), fce=True, top=True), 'T0'), (Stt(crd=Crd(suit='H', valu=13), loc=Loc(nme='T4', lng=4), fce=True, top=False), 'T0'), (Stt(crd=Crd(suit='S', valu=13), loc=Loc(nme='T5', lng=8), fce=True, top=False), 'T0')]
 >>> h.fndMovesL
 [(Stt(crd=Crd(suit='S', valu=1), loc=Loc(nme='T6', lng=10), fce=True, top=True), 'S')]

 
 
 
 
