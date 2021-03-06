#hand.testdocs_7.7.5.py

import logging
import logging.config


def test_play_Set(self,  state=None,  logger=None):
    """ EXECUTES foundation, king and sibling Moves until no more moves: stymied or Won.  RETURNS hCntr(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
    >>> from h import *    
    >>> import logging
    >>> import pickle
    >>> import state
    >>> import hand
    >>> tCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0, std=0)
    >>> logW = logging.getLogger('myW')
    >>> logI = logging.getLogger('myI')
    >>> logI.info("#### now on play_Set ###############")
    >>> th = hand.Hand('set')
    >>> tCntr = th.play_Set(5, logW)
    >>> #
    """
    pass

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
    >>> logI.info("#### now add sibMoves() that Stymied")
    >>> ts2 = state.getTS('t_sibOnly')  # stymies
    >>> th = hand.Hand(mystate = ts2, tag='1')
    >>> tCntr = th.play_Hand(logger=logW)
    >>> 
    >>> logW.warn( " #### first pure fndMoves() with sequenced TestState.")
    >>> ts1 = state.getTS('t_52fnd', False)
    >>> th = hand.Hand(mystate = ts1, tag='1')
    >>> tCntr = th.play_Hand(logger=logW)
    >>> tCntr['winCnt'] == 1 and tCntr['fCnt'] == 52
    True

    """
    pass
class testHand:
    def test_1_kngBranching():
        """ the begining of maxHands: picking the highest return.
        >>> import logging
        >>> import logging.config
        >>> from h import *      
        >>> import hand, state
        >>> tCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        >>> hnd = hand.Hand(tag='1')
        >>> hnd.state = state.FullState()  # shuffled
        >>> logger = logging.getLogger('myI')
        >>> tCntr.clear()

        >>> #tCntr += hnd.play_Hand(logger=logger)  #TEST OBJECT
        asdfghjk
        >>>          
        """
        pass
        
if __name__ == "__main__":
    logging.config.fileConfig('myConfig.conf')            
    import doctest
    doctest.testmod(verbose=False)

    #def test_0_kngBranching():
        #""" the begining of maxHands: picking the highest return.
        #>>> import  state, hand
        #>>> import logging
        #>>> import logging.config
        #>>> from h import *      
        #>>> #logger = logging.getLogger('myW')        
        #>>> tCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        #>>> h = hand.Hand(tag='1')
        #>>> h.state = state.FullFoundations()
        #>>> # MAKE 4 kngMovs: 2Kngs x 2 empty tbls.
        #>>> h.state.move(Mov(Crd('C', 12),  'T0'))  # is 13, 12
        #>>> h.state.move(Mov(Crd('D', 12),  'T1'))  # is 13, 12
        #>>> h.state.move(Mov(Crd('D', 11),  'T2'))  # is11
        #>>> h.state.move(Mov(Crd('D', 10),  'T3'))  # is 10
        #>>> h.state.move(Mov(Crd('D', 7),  'T4'))  # is7,8,9
        #>>> #                                                T5 & T6 are empty.
        #>>> logger = logging.getLogger('myW')
        #>>> tCntr.clear()
        #>>> tCntr += h.play_Hand(logger=logger)  #TEST OBJECT
        
         #"""
    
        
    #def test_play_1_Set(self):
        #"""      
        #>>> from h import *
        #>>> import  state, hand
        #>>> import logging
        #>>> import logging.config
        #>>> #import cProfile
        
        #>>> testSetCntr = Counter( fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        #>>> h = hand.Hand()
        #>>>
        #>>> #  ****** TESTS # (1) state already WON: fndCnt == 52
        #>>> h.state = state.FullState(True)  #shuffled
        #>>> logger = logging.getLogger('myI')
        #>>> testSetCntr.clear()
        #>>> #REFACT testSetCntr = h.play_Set(5, logger=logger)  #TEST OBJECT
        #>>> testSetCntr['nCnt'] == 5
        #True
        #>>>
        #"""
        
    #def test_play_Hand(self):
        #"""      
        #>>> import  state, hand
        #>>> from h import *
        #>>> testSetCntr = Counter(['winCnt', 'fCnt', 'nCnt'])
        #>>>
        #>>> #  ****** TESTS # (1) state is aleady WON: fndCnt == 52
        #>>> h = hand.Hand()
        #>>> h.state = state.FullFoundations()  # already at the end
        #>>> testSetCntr.clear()
        #>>> testSetCntr += h.play_Hand()  #TEST OBJECT
        #>>> #testSetCntr
        #>>> testSetCntr['nCnt'] == 1 and testSetCntr['fCnt'] == 0
        #True
        #>>> # *******TESTS # (2) state STYMID: no moves available
        #>>> h.state = state.State()
        #>>> s0 = newStt('T1', True, Crd('H', 1 ))
        #>>> s1 = newStt('T1', True, Crd( 'H', 2))  # BLOCKS ACE MOVE
        #>>> h.state.populate([ s0, s1])
        #>>> testSetCntr.clear()
        #>>> testSetCntr += h.play_Hand()  #TEST OBJECT
        #>>> testSetCntr['winCnt'] == 0 and testSetCntr['nCnt'] == 1
        #True
        #>>> # ********* # (3) testdata sequenced for all fndMove
        #>>> h = hand.Hand()        
        #>>> h.state = state.FullState(False)
        #>>> testSetCntr.clear()
        #>>> testSetCntr += h.play_Hand()  #TEST OBJECT 
        #>>> testSetCntr['nCnt'] == 1 and testSetCntr['fCnt'] == 52  # 1 pass thre play_Hand using 'while fndMove()
        #True
        #>>>
        #>>> import  state, hand
        #>>> import logging
        #>>> import logging.config
        #>>> from h import *      
        #>>> logger = logging.getLogger('myW')        
        #>>> testSetCntr = Counter(fCnt=0,  nCnt=0,  winCnt=0, msClk=0)
        #>>>
        #>>> # ********* # (4) testdata shuffled
        #>>> h = hand.Hand()        
        #>>> h.state = state.FullState()  # default is shuffle: True
        #>>> logger = logging.getLogger('myW')
        #>>> testSetCntr.clear()
        #>>> testSetCntr += h.play_Hand(logger=logger)  #TEST OBJECT
        #>>> #testSetCntr
        #>>>                

        #>>> # ********* # (1) test new tag
        #>>> h = hand.Hand(tag='0')
        #>>> h.tag == '0'
        #True
        #>>> h.tag = 'h.5.6'
        #>>> h.tag
        #'h.5.6'
        #"""        
        #pass
    
    
    #def test_fndMove(self):
        #"""SETS self.fndMovesL  - faceUP, topCrd in tableau moves to  foundation topCrd if f_Crd is younger sib of t_Crd 
        #>>> import  state, hand
        #>>> from h import *
        #>>> st = state.State()
        #>>> h = hand.Hand(st)
        
        ## populate a foundation test to
        ## (1) topTbl no match in foundation
        ## (2)topTbl has match in foundation
        ## (3)topTbl Ace has match in empty foundation
        ## (4)buried Tbl has match in foundation: NO MOVE
        ## (5) faceDown Ace: No MOVE
        #>>> newSttL = []
        #>>> newSttL.append(newStt( 'T0', True, Crd('C', 2))) #(1)      
        #>>> newSttL.append(newStt( 'T1', True, Crd('D', 2)))  #(2)       
        #>>> newSttL.append(newStt( 'D', True, Crd('D', 1))) #(2)   MOVE  
        #>>> newSttL.append(newStt( 'T2', True, Crd('H', 1))) #(3)  MOVE
        #>>> newSttL.append(newStt( 'T3', True, Crd('S', 1))) #(4)  
        #>>> newSttL.append(newStt( 'T3', True, Crd('S', 2))) #(4)
        #>>> newSttL.append(newStt( 'T4', False, Crd('C', 1))) #(5)  MOVE 
        #>>> #newSttL
        #>>> st.populate(newSttL)
        #>>> h.fndMove(st)  #  UNDER TEST ITEM
        #True
        #>>> len( h.fndMovesL)   # expect 
        #3
        #>>> #del st
        #>>>
        #"""
        
    #def test_kngMove(self):
        #""" SETS self.kngMovesL  - king IsFaceUp_NotFirstRULE in tableau moves to a tableau topCrd.

        #>>> import  state, hand
        #>>> from h import *
        #>>> st = state.State()
        
        #>>> # **** populate a king test state.: three UP kings but one is ndx 0, two empty tbl: T2, T6
        #>>> newStt0 = [ newStt( 'T0', True, Crd('D', 13)) ]  # MOVE faceUP kng in 0 Ndx.
        #>>> newStt0.append( newStt('T1', False, Crd('D', 6)) )
        #>>> newStt0.append(newStt('T1', True, Crd('D', 12)))
        #>>> newStt0.append(newStt( 'T3', True, Crd('C', 1)))
        #>>> newStt0.append(newStt( 'T3', True, Crd('H', 13)))  # MOVE buried faceUP king
        #>>> newStt0.append(newStt( 'T3', True, Crd('H', 6))  )
        #>>> newStt0.append(newStt('T4', True, Crd('D', 4))  )
        #>>> newStt0.append(newStt('T5', False, Crd('D', 10)) )
        #>>> newStt0.append(newStt('T5', False, Crd('S', 13)))  # faceDOWN kng
        #>>> st.populate(newStt0)
        #>>> # ********* state setup done
        #>>> h = hand.Hand(st)
        
        ##>>> h.kngMove(st)  # OBJECT UNDER TEST
        ##True
        ##>>> h.kngMovesL[0]  # the first move will be H-13 in T3 to T2
        ##Mov(crd=Crd(suit='H', valu=13), stkNme='T2')
        ##>>> h.kngMovesL[1]
        ##Mov(crd=Crd(suit='H', valu=13), stkNme='T6')
        ##>>> h.kngMovesL[2]
        ##Mov(crd=Crd(suit='C', valu=13), stkNme='T2')
        ##>>> h.kngMovesL[3]  
        ##Mov(crd=Crd(suit='C', valu=13), stkNme='T6')
        ##>>> len(h.kngMovesL) ==  4
        ##True
        ##>>>  # *************  move one to confirm move() works
        ##>>> h.state.move(h.kngMovesL[0])  #UNDER TEST METHOD
        ##>>> st.stkOD['T3'].head  # >>  was buried under king
        ##Crd(suit='C', valu=1)
        ##>>> st.stkOD['T2'].head  # card on top of buried Kng
        ##Crd(suit='H', valu=6)
        ##>>> del st
        #>>> 
        #"""
        #pass
    
    #def test_sibMove(self):
        #""" SETS self.sibMovesL - faceUP, sib_crd in another tableau moves to a tableau topCrd.
        
        #>>> import  state, hand
        #>>> from h import *
        #>>> st = state.State()
        #>>> # violations: top is Ace, sib faceDOWN
        #>>> # **** populate a test state.
        #>>> sib_crd = Crd('D', 3)
        #>>> newStt0 = [ newStt('T3', True, Crd('H', 7))]
        #>>> newStt0.append(newStt('T3', True, Crd('D', 4)))   # T3.head
        #>>> newStt0.append(newStt('T6', False, Crd('D', 3)))   # faceDOWN sib violates RULE
        #>>> newStt0.append(newStt('T6', True, Crd('D', 2)))   # 
        #>>> st.populate(newStt0)  #state updated
        #>>> st.crd2OD[Crd('D', 3)] = newStt('T6', False, Crd('D', 3)) # have to beat the automatic faceUP on append.
        #>>> # ********* state setup done
        #>>> h = hand.Hand(st)
        #>>> h.sibMove(st) # OBJECT UNDER TEST:
        #False
        #>>> len(h.sibMovesL) ==  0
        #True
        #>>> # OBJECT UNDER TEST #don't call move with no moves OR handle it better than assert !!   
        #>>>
        ##NOTE: The following really tests State.move. Should be in State. Figureout what to do with a call of no moves.
        ##>>> st.move(h.sibMovesL)
        ##Traceback (most recent call last):
        ##...
        ##AssertionError: WARNING: Don't call move with empty move list.
        #>>> # ********** try again but with faceUP sib
        #>>> new_Stt = st.crd2OD[sib_crd]._replace(fce=True)
        #>>> st.crd2OD[sib_crd] = new_Stt
        #>>> h.sibMove(st) # OBJECT UNDER TEST
        #True
        #>>> st.move(h.sibMovesL[0])  # OBJECT UNDER TEST
        #>>> st.stkOD['T6'].head  # >>  empty
        #>>> st.stkOD['T3'].head  # sib
        #Crd(suit='D', valu=2)
        #>>> del st
        #>>>
        #""" 
        #pass
    

        
