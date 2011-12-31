""" state.7.3.1.py 
#MOD 7.3.13
# 111213.1040
# Loc.lng begins at lng==0. New rules for SHIFT()
"""

import random
import rS
from rS import *
#import lookup

import logging
import logging.config
####################################################

class State:
    """
    """
    def __init__(self, shuffle=True,  logger=None):
        """ rS deal of 52 states: stt @ (crd, loc, fce)>(('C', 3), ('T4', 4), True)
        """
        self.crdD =  OrderedDict()
        self.stkD =  OrderedDict()
        self.DEAL_LENGTHS = []  #Loc
        
        #BUILD RUSSIAN ROULETTE INIT STATE
        STACK_FACE_DICT = OrderedDict(sorted({'T0':[UP]
                                      , 'T1': 1 * [False] + 5 * [True]
                                      , 'T2': 2 * [False] + 5 * [True]
                                      , 'T3': 3 * [False] + 5 * [True]
                                      , 'T4': 4 * [False] + 5 * [True]
                                      , 'T5': 5 * [False] + 5 * [True]
                                      , 'T6': 6 * [False] + 5 * [UP]
                                      ,  'S': [],  'H': [], 'D': [], 'C': []
                                      }.items(), key=lambda t: t[0])) #{'T0':[True], 'T1':[False, True, True, True, True, True], ,,,}
        
        DEAL_LENGTHS =  [(s_nme, len(STACK_FACE_DICT[s_nme])) for s_nme in STACKS]
        #[('T0', 1), ('T1', 6), ('T2', 7), ('T3', 8), ('T4', 9), ('T5', 10), ('T6', 11), ('S', 0), ('H', 0), ('D', 0), ('C', 0)]

        CARDS = [Crd(s, v) for s in  SUITS for  v in  VALUES ]              
        if shuffle: random.shuffle(CARDS)
        CARDS_52_LIST = [CARDS.pop() for nme, nlen in  DEAL_LENGTHS for  i in  range(nlen)]
        #[('C', 13), ('C', 12), ('C', 11), ('C', 10), ('C', 9), ('C', 8), ('C', 7), ('C', 6),
        
        LOCS_52_LIST = [Loc(nme, i) for nme, nlen in  DEAL_LENGTHS for  i in  range(nlen)]
        #[('T0', 0), ('T1', 0), ('T1', 1), ('T1', 2), ('T1', 3), ('T1', 4), ('T1', 5), ('T2', 0), 
        
        FACES_52_LIST = [ fceL for nme, nlen in  DEAL_LENGTHS for fceL in STACK_FACE_DICT[nme]]  
        #[True, False, True, True, True, True, True, False,
        
        TOPS =  lambda i, n: True if i ==  n - 1 else False
        TOPS_52_LIST = [TOPS(i, nlen) for nme, nlen in  DEAL_LENGTHS for  i in  range(nlen)]
        #[True, False, False, False, False, False, True, False,
        
        zipped =  list(zip(CARDS_52_LIST, LOCS_52_LIST,  FACES_52_LIST,  TOPS_52_LIST))
        STATE_52_LIST = list(Stt(c, l, f, t) for c, l, f, t in zipped)
        
        ## BUILD cardD
        zipped =  list(zip(CARDS_52_LIST, STATE_52_LIST))   # HAND FORMED HERE.
        self.crdD = OrderedDict(zipped)  # NO foundations in crdD yet!!
        
        #BUILD stkD
        stksL =  [(Loc(stt.loc.nme,  stt.loc.lng), stt) for stt in STATE_52_LIST]
        fndsL = [(Loc(nme,  -1), Stt(Crd_EMPTY,  Loc(nme, -1), 1, 1)) for nme in  FOUNDATIONS]
        stksL += fndsL
        self.stkD =  OrderedDict(stksL)
        #MOD7.2.1: ADD empty stack Loc to foundations.
        
        del(CARDS, DEAL_LENGTHS, shuffle,  CARDS_52_LIST, LOCS_52_LIST,  FACES_52_LIST,  TOPS_52_LIST,  STATE_52_LIST, zipped,  stksL,  fndsL)
               
        pass
    
    @property
    def fnd_Count(self):
        ret = len([(key) for key, stt in self.stkD.items() if key.nme in FOUNDATIONS and stt.crd.valu != -1])
        return  ret

    @property
    def topD(self):
        return OrderedDict(sorted([(loc.nme, stt) for loc, stt in self.stkD.items() if stt.top]))
    
    @property
    def tbl_topD(self) :
        return OrderedDict(sorted([(nme,  stt) for nme, stt in self.topD.items() if  nme in TABLEAUS]))
    @property
    def fnd_topD(self):
        return OrderedDict(sorted([(nme,  stt) for nme, stt in self.topD.items() if  nme in FOUNDATIONS]))
        
    
    def SHIFT(self,  frm_Stt,  to_stk_nme,  logger=None,  boolPRINT_Tops = False):
        """ SHIFT one or more STATES to a STACK. UPDATE crdD and stkD."""
        # APPEND FROM ( frm_Stt)  TO ( _to_top_Stt)
       
       # TAGS & INIT******
        stkD = self.stkD
        crdD =  self.crdD
        msg = ''
        
        frm_crd,  frm_loc,  frm_fce,  frm_top = frm_Stt
        RULE_EMPTY_STATE =  lambda stt:  stt.crd == Crd_EMPTY
        
        # ***** TO: 
        _cur_top_Stt = self.get_Top_Stt(to_stk_nme)  #BUILD _to_Stt from _cur_top_Stt
        _cur_top_Loc = _cur_top_Stt.loc  # RESET old top
        _to_Loc = _cur_top_Stt.loc._replace(lng=_cur_top_Stt.loc.lng +1)  # Now, equiv 'APPEND'
        _to_Stt = _cur_top_Stt._replace(crd=frm_crd, loc=_to_Loc,  fce=True,  top=True)
        
        msg = "Before  Tops:frm:"+Tmplt_Stt.format(self.get_Top_Stt(frm_Stt.loc.nme)) + "   to:" + Tmplt_Stt.format(self.get_Top_Stt(to_stk_nme))
        
        if RULE_EMPTY_STATE(_cur_top_Stt):  #REPLACE an empty state@ lng=-1 with new state @ loc.lng=0.
            del(stkD[_cur_top_Loc])  #del empty state.
            #_to_Stt = _cur_top_Stt._replace(crd=frm_crd, loc=_to_Loc,  fce=True,  top=True)
##            stkD[_to_Loc] =  _to_Stt
##            crdD[frm_crd] =  _to_Stt
        else: # ''appending' to a loaded stack @ lng=cur top +1:UPDATE lower stt.
            _cur_top_Stt =  _cur_top_Stt._replace(top=False)  
            stkD[_cur_top_Loc] =  _cur_top_Stt
            #_to_Stt = _cur_top_Stt._replace(crd=frm_crd, loc=_to_Loc,  fce=True,  top=True) 
        stkD[_to_Loc] =  _to_Stt
        crdD[frm_crd] =  _to_Stt
        pass
    
        if RULE_EMPTY_STATE(frm_Stt):  # Crd==Crd_EMPTY; 
            # FRM:Loc0,Crd_EMPTY+  SHIFT() is prohibited.
            if logger: logger.error(" Cannot switch({}). It is Crd_EMPTY.".format(frm_Stt))
            pass
        elif frm_loc.lng == 0:  # only one in stk, REPLACE it with empty stt.
            del(stkD[frm_loc])   # lng=0         
            frm_Loc = frm_loc._replace(lng=-1)
            frm_Stt = Stt(Crd_EMPTY,  frm_Loc,  True, True)
            crdD[frm_Stt.crd] =  frm_Stt     #UPDATE crdD              
            stkD[frm_Stt.loc] = frm_Stt
            pass
        else:  # more than one stt in stack;
            del(stkD[frm_loc])
            # there is stt under frm_Stt; it is now top
            _new_top =  stkD[frm_loc._replace(lng=frm_loc.lng - 1)]  #
            _new_top = _new_top._replace(top=True)  #old state is NOW top.
            crdD[_new_top.crd] =  _new_top                   
            stkD[_new_top.loc] = _new_top
            
        ##### CLEAN UP ###########   
        self.stkD =  stkD
        self.crdD = crdD
        msg += "\n  After  Tops:frm:"+Tmplt_Stt.format(self.get_Top_Stt(frm_Stt.loc.nme)) + "   &  " + Tmplt_Stt.format(self.get_Top_Stt(to_stk_nme))
        if boolPRINT_Tops: print(msg)
        if logger: logger.info("\n"+msg)    
        return self.get_Top_Stts()
    
    def get_Top_Stts(self):
        """ <list> Stt@(crd, loc, fce, top)."""
        # 11 stacks: only return filled stacks.            
        ret = [(stt) for stt in self.stkD.values() if stt.top]
        return ret
    
    
    def get_Top_Stt(self,  stk_nme):
        """ """
        _topD =  dict([(loc.nme, stt) for loc, stt in self.stkD.items() if stt.top])
        ret =  _topD[stk_nme]
        return ret
        
    
    def PRINT_Tops(self):
        print('Tops:') 
        for stt in self.stkD.values():
            if stt.top: print(Tmplt_StkD.format(stt))
           
    def PRINT_Stk(self,  stk_str):
        print('Stk '+stk_str + ':') 
        for stt in self.stkD.values():
            if stt.loc.nme == stk_str:
                print(Tmplt_StkD.format(stt))
        
    def PRINT_Stts(self):
        """ """
        for stk_nme in  STACKS:
            self.PRINT_Stk(stk_nme)
        print("\n**********************")       

if __name__ == "__main__":
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    #doctest.testmod(verbose=False)
    doctest.testfile("deal.print.txt")
    doctest.testfile("state_testdocs.txt")
