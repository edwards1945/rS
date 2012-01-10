""" state.7.7.py 
"""
# 100109
# MOD 7.7 enhanced State
# introduce namedtuple h.Status to replace newStt
# introduced new namedtuple h.Move(Crd, fce, StkNme) :NEW ORDER.
# introduce namedtuple newState.crdOD to replace Hand's crd2OD.
# override populate() to not force face = True.
# added another dictionary: movesD
# reversed tuple output of getTopsL(), now called getHeadsL
#  add State.findMoves(): move this functionality from hand to here where it belongs.
