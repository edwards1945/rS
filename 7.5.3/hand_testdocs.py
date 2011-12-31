#hand.testdocs.7.5.3.py
#MOD 7.3.1 

class Hand:
    def fndMove(self, state,  loggerNone):
        """ SETS SETS self.fndMovesL
        for not empty fnd_tops crd.valu CHECK4 tbl_tops[crd.suit] for loc.lng+1
        
        #>>> import  state, hand
        #>>> from rS import *
        #>>> st = state.State()
        
        #>>> # **** populate a test state. 
        #>>> pop0 = Pop( 'T3', True, Crd('H', 7))  
        #>>> pop1 = Pop('T3', True, Crd('D', 4))   # T3.top_item
        #>>> pop2 = Pop('T6', True, Crd('D', 3))   # sib
        #>>> st.populate(pop0,  pop1, pop2)
        #>>> # ********* state setup done
        #>>> h = hand.Hand(st)
        #>>> h.sibMove(st)
        #>>> movL = h.sibMovesL
        #>>> len(movL) #==  1
        #1
        #>>> st.moveCrd(movL[0])  # OBJECT UNDER TEST
        #>>> st.stkOD['T6'].top_item  # >>  empty
        #>>> st.stkOD['T3'].top_item  # sib
        #Crd(suit='D', valu=3)
        
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
        >>> len(h.sibMovesL) ==  0  #don't movCrd !!  REFACT 
        True
        >>> st.moveCrd(h.sibMovesL)
        Traceback (most recent call last):
        ...
        AssertionError: WARNING: Don't call moveCrd with empty move list.
        >>> # ********** try again but with faceUP sib
        >>> new_Stt = st.crdOD[sibCrd]._replace(fce=True)
        >>> st.crdOD[sibCrd] = new_Stt
        >>> h.sibMove(st) # OBJECT UNDER TEST
        >>> st.moveCrd(h.sibMovesL[0])
        >>> st.stkOD['T6'].top_item  # >>  empty
        >>> st.stkOD['T3'].top_item  # sib
        Crd(suit='D', valu=3)

        """ 
         
