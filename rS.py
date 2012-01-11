#! /usr/bin/env python3.2
#rS.7.7.2.py

#120107.10.00  in git created seeTops and produced state.sttTops() to return a string of formated tops ( or I'm beginning to think of them as heads): T1:C05, T2:--, T3,H13

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
