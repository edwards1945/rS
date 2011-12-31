# stack.7.5.0.py module
# MOD 7.5.0  first stack as deque, still using std que; top_item is length

from rS import *
import logging
import logging.config
    
class Stack(list):
    """ named deque of 0 to 52 somethings. For rS it's Stt.

    """
    def __init__(self, stk_name, maxlen=52):
        """  used a stack: right handed FILO        """
        self._nme = stk_name
    #----------------------------------------------------------------------         
    @property
    def nme(self):
        return self._nme
    @property
    def top_ndx(self):
        """      """
        return _top_ndx(self)
    @property
    def top_item (self):
        return _top_item(self)
    #----------------------------------------------------------------------
    def PUSH(self, item):
        """ right push.
        """
        self.append(item)        
    #----------------------------------------------------------------------
    def POP(self):
        """ right pop()  ; allows pops past dek length       
         """
        try:
            return self.pop()
        except IndexError:
            return  None
    #----------------------------------------------------------------------
    def moveItem(self,  mov,  updateItem_function,  logger=None):
        """
        >>> from rS import *
        >>> import stack
        >>> s = stack.Stack('Test')
        
        # ************* TEST a top to top Mov  **********
        >>> fnd_H =stack.Stack('H')
        >>> tbl_1 = stack.Stack('T1')  #new stack
        >>> tbl_1.PUSH('H0') 
        >>> frm_Loc =Loc(tbl_1, tbl_1.top_ndx)
        >>> frm_Loc
        Loc(stk=['H0'], ndx=0)
        >>> # ********  setup complete
        >>> mov = Mov(frm_Loc, fnd_H, 'H0')
        >>> s.moveItem(mov, lambda c: c+'.updated')
        >>> tbl_1.top_item
        >>> fnd_H.top_item
        'H0.updated'
        
        # ************** TEST a NOT top  to top  Mov *****
        >>> tbl_2 = stack.Stack('T2')
        >>> tbl_2.extend(['S13','C7', 'C6'])
        >>> tbl_3 = stack.Stack('T3')
        >>> tbl_3.PUSH('C8')
        >>> # ********  setup complete
        >>> mov = Mov(Loc(tbl_2, 1), tbl_3, 'C7')
        >>> s.moveItem(mov, lambda c: c+'.updated' )
        >>> tbl_3
        ['C8', 'C7.updated', 'C6.updated']
        """
        #self.moveItem_s(mov, updateItem_function)
        frm_loc,  to_stk,  item =  mov
        frm_stk,  frm_stk_ndx = frm_loc
        _slice = frm_loc.stk[frm_loc.ndx:]
        for _itm in  _slice:
            new_item = updateItem_function(_itm)
            frm_loc.stk.remove(_itm) 
            to_stk.PUSH(new_item)  #PUSH new
            

    def moveItem_s(self, mov, updateItem_function):
        """ moves item[or items] frm_loc > to_stk, updating each item.
        """
        frm_loc,  to_stk,  item =  mov
        frm_top_item = frm_loc.stk.top_item 
        while frm_top_item  != item:  #mov items above frm item.
            assert frm_top_item is not None, ("Hey, in Stack.moveItem() for mov:{}"
                      " the while  loop encountered frm_top_item as None.").format(mov)
                    
            new_item = updateItem_function(frm_top_item)
            to_stk.PUSH(new_item)  #PUSH new
            frm_loc.stk.POP() # POP top
            frm_top_item = frm_loc.stk.top_item
            if frm_top_item == item: break  # finished top_items above. 
            #REFACT there has to be a terser way to accomplish this.    
        item = updateItem_function(item)
        to_stk.PUSH(item)  #PUSH new
        frm_loc.stk.POP() # POP frm
        #----------------------------------------------------------------------

def _top_ndx(lst):
    """
    >>> _top_ndx([1,2,3])==2
    True
    >>> _top_ndx([1])== 0
    True
    >>> _top_ndx([]) is None
    True
    """
    lng =  len(lst)
    return lng -1 if  lng > 0 else None

def _top_item (lst):
    """ RETURN: top_item item or None.
    >>> _top_item(['a', 'b', 'c'])=='c'
    True
    >>> _top_item(['d'])== 'd'
    True
    >>> _top_item([]) is None
    True
   
    """
    ndx = _top_ndx(lst)
    return lst[ndx] if ndx is not None else None    

if __name__ == "__main__":   
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    doctest.testfile("stack_testdocs.py")
