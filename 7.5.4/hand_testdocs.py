#hand.testdocs.7.5.4.py
#MOD 7.3.1 

class testHand:
    def fndMove(self, state,  loggerNone):
        """ SETS SETS self.fndMovesL
        for not empty fnd_tops crd.valu CHECK4 tbl_tops[crd.suit] for loc.lng+1
        
        >>> import  state, hand
        >>> from rS import *
        >>> st = state.State()
        
        >>> # **** populate a test state.: two UP kings, two empty tbl: T2, T6
        >>> pop0 = Pop( 'T0', True, Crd('H', 5))  
        >>> pop1 = Pop('T1', False, Crd('D', 6))  
        >>> pop2 = Pop('T1', False, Crd('D', 13))  # faceDOWN kng
        >>> pop3 = Pop('T1', True, Crd('D', 12))
        >>> pop4_0 = Pop( 'T3', True, Crd('C', 1))
        >>> pop4 = Pop( 'T3', True, Crd('H', 13))  # buried king
        >>> pop5 = Pop( 'T3', True, Crd('H', 6))  
        >>> pop6 = Pop('T4', True, Crd('D', 4))  
        >>> pop7 = Pop('T5', False, Crd('D', 10)) 
        >>> pop8 = Pop('T5', False, Crd('S', 13))  # faceDOWN kng
        >>> pop9 = Pop('T5', True, Crd('C', 13))  # top kng
        >>> st.populate(pop0,  pop1, pop2, pop3, pop4_0, pop4, pop5, pop6, pop7, pop8, pop9)
        >>> # ********* state setup done
        >>> h = hand.Hand(st)
        >>> h.fndMove(st)  # OBJECT UNDER TEST
        >>> movL = h.fndMovesL  # the first move will be H-13 in T3 to T2
        >>> len(movL) ==  4
        True
        
        #>>> st.stkOD['T3'].top_item  # >>  under card
        #Crd(suit='C', valu=1)
        #>>> st.stkOD['T2'].top_item  # card on top of buried Kng
        #Crd(suit='H', valu=6)
        #>>> del st
        >>> 
        """    
        pass
         
    def sibMove(self, state, logger=None):
        """ SETS self.sibMovesL - faceUP, sibCrd in another tableau moves to a tableau topCrd.
        
        >>> import  state, hand
        >>> from rS import *
        >>> st = state.State()
        
        >>> # **** populate a test state.
        >>> sibCrd = Crd('D', 3)
        >>> pop0 = Pop( 'T3', True, Crd('H', 7))  
        >>> pop1 = Pop('T3', True, Crd('D', 4))   # T3.top_item
        >>> pop2 = Pop('T6', False, sibCrd)   # faceDOWN sib violates RULE
        >>> st.populate(pop0,  pop1, pop2)  #state updated
        >>> # ********* state setup done
        >>> h = hand.Hand(st)
        >>> h.sibMove(st) # OBJECT UNDER TEST
        >>> movL= h.sibMovesL
        >>> len(h.sibMovesL) ==  0  # OBJECT UNDER TEST #don't call moveCrd2Nme with no moves OR handle it better than assert !!   
        True
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

        """ 
         
