""" state.7.7.1.py 
"""
# MOD 7.7.1
# 120110 # next is State.move(). assure logging is effective.
##  crippled hand_testdocs.py till ready for it. All test now OK.
## overlaid State.move in newState
## State.move REFACTed
## State.move logging improved.
## Stack.moveMyItems() trimmed

# MOD 7.7 enhanced State
# 120109
# introduce namedtuple h.Status to replace newStt
# introduced new namedtuple h.Move(Crd, fce, StkNme) :NEW ORDER.
# introduce namedtuple newState.crdOD to replace Hand's crd2OD.
# override populate() to not force face = True.
# added another dictionary: movesD
# reversed tuple output of getTopsL(), now called getHeadsL
#  add State.findMoves(): move this functionality from hand to here where it belongs.
