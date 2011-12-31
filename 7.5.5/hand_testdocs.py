#hand.testdocs.7.5.5.py
#MOD 7.5.5

class testHand:
    def test_fndMove(self):
        """SETS self.fndMovesL  - faceUP, topCrd in tableau moves to  foundation topCrd if f_Crd is younger sib of t_Crd 
        >>> import  state, hand
        >>> from rS import *
        >>> st = state.State()
        
        # populate a foundation test to
        # (1) topTbl no match in foundation
        # (2)topTbl has match in foundation
        # (3)topTbl Ace has match in empty foundation
        # (4)buried Tbl has match in foundation: NO MOVE
        
        >>> newSttL = []
        >>> newSttL.append(newStt( 'T0', True, Crd('C', 2))) #(1)      
        >>> newSttL.append(newStt( 'T1', True, Crd('D', 2)))  #(2)       
        >>> newSttL.append(newStt( 'D', True, Crd('D', 1))) #(2)        
        >>> newSttL.append(newStt( 'T2', True, Crd('H', 1))) #(3)
        >>> newSttL.append(newStt( 'T3', False, Crd('S', 1))) #(4)
        >>> newSttL.append(newStt( 'T3', False, Crd('S', 2))) #(4)
        >>> #newSttL
        >>> st.populate(newSttL)
        >>> del st
        >>>
        """
        
    def test_kngMove(self):
        """ SETS self.kngMovesL  - king IsFaceUp_NotFirstRULE in tableau moves to a tableau topCrd.

        >>> import  state, hand
        >>> from rS import *
        >>> st = state.State()
        
        >>> # **** populate a king test state.: three UP kings but one is ndx 0, two empty tbl: T2, T6
        >>> newStt0 = [ newStt( 'T0', True, Crd('D', 13)) ]  # faceUP kng in 0 Ndx.
        >>> newStt0.append( newStt('T1', False, Crd('D', 6)) )
        >>> newStt0.append(newStt('T1', True, Crd('D', 12)))
        >>> newStt0.append(newStt( 'T3', True, Crd('C', 1)))
        >>> newStt0.append(newStt( 'T3', True, Crd('H', 13)))  # buried faceUP king
        >>> newStt0.append(newStt( 'T3', True, Crd('H', 6))  )
        >>> newStt0.append(newStt('T4', True, Crd('D', 4))  )
        >>> newStt0.append(newStt('T5', False, Crd('D', 10)) )
        >>> newStt0.append(newStt('T5', False, Crd('S', 13)))  # faceDOWN kng
        >>> newStt0.append(newStt('T5', True, Crd('C', 13)))  # top faceUP kng
        >>> st.populate(newStt0)
        >>> # ********* state setup done
        >>> h = hand.Hand(st)
        >>> h.kngMove(st)  # OBJECT UNDER TEST
        >>> h.kngMovesL[0]  # the first move will be H-13 in T3 to T2
        Mov2Nme(crd=Crd(suit='H', valu=13), stkNme='T2')
        >>> h.kngMovesL[1]
        Mov2Nme(crd=Crd(suit='H', valu=13), stkNme='T6')
        >>> h.kngMovesL[2]
        Mov2Nme(crd=Crd(suit='C', valu=13), stkNme='T2')
        >>> h.kngMovesL[3]  
        Mov2Nme(crd=Crd(suit='C', valu=13), stkNme='T6')
        >>> len(h.kngMovesL) ==  4
        True
        >>>  # *************  move one to confirm moveCrd2Nme() works
        >>> h.state.moveCrd2Nme(h.kngMovesL[0])  #UNDER TEST METHOD
        >>> st.stkOD['T3'].top_item  # >>  was buried under king
        Crd(suit='C', valu=1)
        >>> st.stkOD['T2'].top_item  # card on top of buried Kng
        Crd(suit='H', valu=6)
        >>> del st
        >>> 
        """
        pass
    
    def test_sibMove(self):
        """ SETS self.sibMovesL - faceUP, sibCrd in another tableau moves to a tableau topCrd.
        
        >>> import  state, hand
        >>> from rS import *
        >>> st = state.State()
        >>> # violations: top is Ace, sib faceDOWN
        >>> # **** populate a test state.
        >>> sibCrd = Crd('D', 3)
        >>> newStt0 = [ newStt('T3', True, Crd('H', 7))]
        >>> newStt0.append(newStt('T3', True, Crd('D', 4)))   # T3.top_item
        >>> newStt0.append(newStt('T6', False, sibCrd))   # faceDOWN sib violates RULE
        >>> st.populate(newStt0)  #state updated
        >>> # ********* state setup done
        >>> h = hand.Hand(st)
        >>> h.sibMove(st) # OBJECT UNDER TEST: 
        >>> len(h.sibMovesL) ==  0
        True
        >>> # OBJECT UNDER TEST #don't call moveCrd2Nme with no moves OR handle it better than assert !!   
        >>>
        #NOTE: The following really tests State.moveCrd2Nme. Should be in State. Figureout what to do with a call of no moves.
        #>>> st.moveCrd2Nme(h.sibMovesL)
        #Traceback (most recent call last):
        #...
        #AssertionError: WARNING: Don't call moveCrd2Nme with empty move list.
        >>> # ********** try again but with faceUP sib
        >>> new_Stt = st.crd2OD[sibCrd]._replace(fce=True)
        >>> st.crd2OD[sibCrd] = new_Stt
        >>> h.sibMove(st) # OBJECT UNDER TEST
        >>> st.moveCrd2Nme(h.sibMovesL[0])  # OBJECT UNDER TEST
        >>> st.stkOD['T6'].top_item  # >>  empty
        >>> st.stkOD['T3'].top_item  # sib
        Crd(suit='D', valu=3)
        >>> del st
        >>>
        """ 
        pass
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
        
