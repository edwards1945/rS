# stack_testdocs_7.7.5


from h import *
import  stack
import logging
import logging.config

class test_Stack(deque):
    """ named deque of 0 to 52 somethings. For rS it's Stt.
    
    >>> from h import *
    >>> import state, stack
    >>> st = state.State()
    >>> len(st.crdOD) == 52
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
    >>> tbl_0.head is None
    True
    >>> tbl_0.extend(['H0', 'C1'])
    >>> tbl_0.PUSH('anything I want')
    >>> tbl_0.head == 'anything I want'
    True
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
    >>>
    """
        
if __name__ == "__main__":   
    import doctest
    logging.config.fileConfig('myConfig.conf') 
    doctest.testmod(verbose=False)
    #doctest.testfile("stack_testdocs.txt")
