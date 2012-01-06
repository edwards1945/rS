# stack.7.6.py module
# MOD 7.6  Tested Basic play @ 2.5- 3 %
# #  

#from h import *
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
    def name(self):
        return self._nme
    @property
    def isEmpty(self):
        return not  len(self) > 0
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

    #----------------------------------------------------------------------
    def moveMyItems(self,  item, to_stk, updateItem_function):
        """ moves one or more items -  in  rS items are cards - to the new stack.
        The updateItem_function() updates the card dictionary with new state in rS.
        
        Self can be empty.        
        """
        if item not in self:  # special case: populating an empty stk.
            # MOD 7.5.7 111229.1130 DEL> and  item.ndx is None:  
            to_stk.PUSH(item) 
            updateItem_function(item,  to_stk)        
        else:           
            _slice = self[self.index(item):] 
            for _itm in  _slice:
                self.remove(_itm)   # won't error if empty
                to_stk.PUSH(_itm)
                updateItem_function(_itm,  to_stk)        
            if not self.isEmpty:  # uncovered a card, make it faceUP
                crd = self.top_item
                updateItem_function(crd, self)
        
        
        
#----------------------------------------------------------------------
def _top_ndx(lst):
    """
    """
    lng =  len(lst)
    return lng -1 if  lng > 0 else None

def _top_item (lst):
    """ RETURN: top_item item or None.
    """
    ndx = _top_ndx(lst)
    return lst[ndx] if ndx is not None else None    

if __name__ == "__main__":   
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    doctest.testfile("stack_testdocs.py")
