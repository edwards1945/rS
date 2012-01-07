#! /usr/bin/env python3.2
#rS.7.6.py
#MOD 7.6  Tested Basic play @ 2.5- 3 %
#MOD 120107.0950
#  tried _do_best_kngMove() spawning new Hands in 1st cut. Worked but really slowed things down.
#  trying _do_best_kngMove just spawning new State but can't figure it out.
## branch: maybe if I could see the top || head cards in a loggger output I could understand better. Should I git branch from here:wip or from master??? Let's try from master to seeTops.

# PURPOSE
#I want to compare win rate of non-recursive play versus recursive play.

#Is 5% normal for stop when no more moves?
#as of 1201 basic play of shift all fundMoves, then a kng move then a sib move nets 2 - 3%.
#Is 8% or better for recursive?
#Recursive means trying every option until a win. Or maybe EVERY option and compare record."""
#Regex VER *[0-9]*\.[0-9]*

import sys,  math
import logging
import logging.config

#################
def main():
    import  hand
    import cProfile,  pstats
    #cProfile.run("test()")  # any change to see it in git
    hand.test()
    


if __name__ == "__main__":
    logging.config.fileConfig('myConfig.conf')        
    import doctest
    #doctest.testmod(verbose=False)
    #doctest.testfile("rS_testdocs.py")
    main()
