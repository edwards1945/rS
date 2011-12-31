# stack_testdocs.7.5.6.py module
# MOD 7.5.6  

from rS import *
import logging
import logging.config

class Stack(deque):
    """ named deque of 0 to 52 somethings. For rS it's Stt.
    
    >>> from rS import *
    >>> import stack
    >>> s = stack.Stack('Test')
    
    # ************* TEST class invoke Stack   **********
    >>> tbl_0 = stack.Stack('T0')    
    >>> tbl_0.nme == 'T0'
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
    
if __name__ == "__main__":   
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("stack_testdocs.txt")
