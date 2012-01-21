""" state_7.7.5.py 
"""
# MOD 7.7.5
# 1120121
## now need move count passed thru to branches.
## worked out hand branching for kngMoves()
# MOD 7.7.6 - moving bulk of play_Hand() to state.
# 120119
## move move decision making to state. With hopes to ease king branching.
#MOD 7.7.5
## working on logging to figure out what kingmoves() is doing.
#MOD 7.7.4
# 120118
## modife State.getTS() to accept folder name.
## developing Hand.branch_kngMoves() method.
## add State.pickleMyState() method to pickle and return current state
## changed Hand.fndMoves() to while / continue
#MOD _7.7.3
# 120117
## hand module test() working; about same results.
## Hand.play_Set() is working with corrected logging displays
## Hand.play_Hand() is working with improved logging
## State.move() improved logging.
# 120116
## changed logging: + easier to change; - ??
## sibMoves() looks ok.
## added stop counter while testing to prevent infinite loop in play_Hand while loop.
## mod State properties ref moves and foundations.
## using state.hasMoves property in Hand.play_Hand()
#MOD _7.7.2
# 120116 
##- now have class getTS() method constant states.
## and a module getTS() function.
## think I understand pickling a little better. really need makeTS since getTS calls it.
# 120114 - rework  Hand, State, Stack fo State handling moves.
## add @propery:isFull to Stack; @property:isWin to State
# 120113 - bypass run or create static TestStates for now; 
# #get back to Hand and multiple kngHands.
# 120112 - worked on TestStates to get constant States
## trouble with makeTS() and getTS()
# 120111 - work on multiple state branching in Hand.
## but first reimplement FullState in newState with fastef full rS deck of cards and stacks.
## newFullState done with short test.
## changed Stack and stack_testdocs attribute get_tops => .head & headsL.
## emoves all the original class State and not used stuff.
## some problems with IDE tests. don't work
# MOD 7.7.1
# 120111 # newState.move() full implement; simple tests run and in state_testdocs.py. Really improved logging: all in one place in move().
## added use of 'hand' instead of 'top' as it is in State: mostly in Stack too.
## NO checking in Move(); except assert ''can't move faceDOWN'.
## improved move() logging and testing
##Stack new property: head
# 120110 # next is State.move(). assure logging is effective.
##  crippled hand_testdocs.py till ready for it. All test now OK.
## overlaid State.move in newState
## State.move REFACTed
## State.move logging improved.
## Stack.moveMyItems() trimmed


# 120109
# introduce namedtuple h.Status to replace newStt
# introduced new namedtuple h.Move(Crd, fce, StkNme) :NEW ORDER.
# introduce namedtuple newState.crdOD to replace Hand's crd2OD.
# override populate() to not force face = True.
# added another dictionary: movesD
# reversed tuple output of getTopsL(), now called getHeadsL
#  add State.find_Moves(): move this functionality from hand to here where it belongs.
