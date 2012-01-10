# stack_testdocs.7.7.1
# MOD 7.7 enhanced State

from h import *
import  stack
import logging
import logging.config

class test_Stack(deque):
    """ named deque of 0 to 52 somethings. For rS it's Stt.
    
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()
    >>> len(st.crd2OD) == 52
    True
    >>> len(st.stkOD)  == 11
    True
       
   >>> from h import *
   >>> import stack
   >>> s = stack.Stack('Test')
    
    # ************* TEST class invoke Stack   **********
    >>> tbl_0 = stack.Stack('T0')    
    >>> tbl_0.name == 'T0'
    True
    >>> tbl_0.top_ndx  #None
    >>> tbl_0.top_item  #None
    
    >>> tbl_0.extend(['H0', 'C1'])
    >>> tbl_0.PUSH('anything I want')
    >>> del( tbl_0[-1:])
    >>> tbl_0.pop()
    'C1'
    >>> tbl_0.pop()
    'H0'
    >>> fnd_H = stack.Stack('H')    
    >>> fnd_H.pop()   # use POP() not pop()
    Traceback (most recent call last):
    ...
    IndexError: pop from empty list
    >>> tbl_0.POP()  # no problem popping an mty stack
    
    """
    def test_top_ndx(lst):
        """
        >>> import stack
        >>> stack._top_ndx([1,2,3])==2
        True
        >>> stack._top_ndx([1])== 0
        True
        >>> stack._top_ndx([]) is None
        True
        """
    def test_top_item (lst):
        """ RETURN: top_item item or None.
        >>> stack._top_item(['a', 'b', 'c'])=='c'
        True
        >>> stack._top_item(['d'])== 'd'
        True
        >>> stack._top_item([]) is None
        True
       
        """
        
if __name__ == "__main__":   
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("stack_testdocs.txt")
