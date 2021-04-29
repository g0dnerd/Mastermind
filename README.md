# Mastermind

Based on VILLE, KNUTH and others, this will attempt to implement a solution tree for MM(p,c)  
with tight upper bounds, dynamic lower bound evaluation and case equivalence detection.  
  
My code is most likely ugly, but still works.

## Changes

* implemented KNUTH's algorithm with W = 5 for MM(4,6)

## TODOs

* comment the damn code
* optimize performance
* look into why solution of (6,3,4,6) takes longer (repeating on identical remaining codes)
* look into pruning