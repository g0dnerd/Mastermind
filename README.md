# Mastermind

Based on VILLE, KNUTH and others, this will attempt to implement a solution tree for MM(p,c)  
with tight upper bounds, dynamic lower bound evaluation and case equivalence detection.  
  
My code is most likely ugly, but still works.

## Changes

* optimizing for MM(4,6) with optimal first guesses and lexical ordering

## TODOs

* generate next possible code at each node instead of storing entire set of possible solutions