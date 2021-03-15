# Omaha Odds Calculator

This is a re-implementation in python 3 of an old [Omaha Odds Calculator](https://github.com/frankdeath/ooc) that I wrote in 2004 using python 2.

# Background

[Omaha](https://www.wsop.com/poker-games/omaha/rules/) (Omaha Hi) is a poker game that is similar to Texas Hold'em.

# Usage

## Pre-flop

The [Hutchison Omaha Point System](http://erh.homestead.com/omaha.html) is used to give an indication of hand strength before the flop:

```shell
$ ./calc.py AsTd6c4h
Hutchison score: 6
Approximate win: 3.0%
```

## Flop

The probabilities of making a hand on the turn & river are calculated after the flop:

```
$ ./calc.py AsTd6c4h Kd8h2s

As Td 6c 4h | Kd 8h 2s - High Card: A-high

TURN

Hand            out of 45       Odds 1:         Probability     # Better / 990  
Royal Flush     0               0.00            0.00            0               
Straight Flush  0               0.00            0.00            0               
Four of a Kind  0               0.00            0.00            0               
Full House      0               0.00            0.00            0               
Flush           0               0.00            0.00            0               
Straight        0               0.00            0.00            0               
Three of a Kind 0               0.00            0.00            9               
Two Pair        0               0.00            0.00            27              
One Pair        21              1.14            46.67           372             
High Card       24              0.88            53.33           24              

RIVER

Hand            out of 990      Odds 1:         Probability     # Better / 990  
Royal Flush     0               0.00            0.00            0               
Straight Flush  0               0.00            0.00            0               
Four of a Kind  0               0.00            0.00            0               
Full House      0               0.00            0.00            0               
Flush           0               0.00            0.00            0               
Straight        64              14.47           6.46            0               
Three of a Kind 21              46.14           2.12            9               
Two Pair        162             5.11            16.36           27              
One Pair        567             0.75            57.27           372             
High Card       176             4.62            17.78           24              
```

## Turn

The probabilities of making a hand on the river are calculated after the flop:

```
$ ./calc.py AsTd6c4h Kd8h2s Jh

As Td 6c 4h | Kd 8h 2s Jh - High Card: A-high

RIVER

Hand            out of 44       Odds 1:         Probability     # Better / 946  
Royal Flush     0               0.00            0.00            0               
Straight Flush  0               0.00            0.00            0               
Four of a Kind  0               0.00            0.00            0               
Full House      0               0.00            0.00            0               
Flush           0               0.00            0.00            0               
Straight        4               10.00           9.09            0               
Three of a Kind 0               0.00            0.00            12              
Two Pair        0               0.00            0.00            54              
One Pair        24              0.83            54.55           426             
High Card       16              1.75            36.36           12              
```

## River

The number of better hands are most useful after all the cards are out:

```
$ ./calc.py AsTd6c4h Kd8h2s Jh 5c

As Td 6c 4h | Kd 8h 2s Jh 5c - High Card: A-high

SHOWDOWN

Hand            out of 1        Odds 1:         Probability     # Better / 903  
Royal Flush     0               0.00            0.00            0               
Straight Flush  0               0.00            0.00            0               
Four of a Kind  0               0.00            0.00            0               
Full House      0               0.00            0.00            0               
Flush           0               0.00            0.00            0               
Straight        0               0.00            0.00            0               
Three of a Kind 0               0.00            0.00            15              
Two Pair        0               0.00            0.00            90              
One Pair        0               0.00            0.00            456             
High Card       1               0.00            100.00          12              
```

Details about the number of hands that are better than your can be displayed at any point after the flop:

```
$ ./calc.py -b AsTd6c4h Kd8h2s Jh 5c

As Td 6c 4h | Kd 8h 2s Jh 5c - High Card: A-high

SHOWDOWN

Hand            out of 1        Odds 1:         Probability     # Better / 903  
Royal Flush     0               0.00            0.00            0               
Straight Flush  0               0.00            0.00            0               
Four of a Kind  0               0.00            0.00            0               
Full House      0               0.00            0.00            0               
Flush           0               0.00            0.00            0               
Straight        0               0.00            0.00            0               
Three of a Kind 0               0.00            0.00            15              
Two Pair        0               0.00            0.00            90              
One Pair        0               0.00            0.00            456             
High Card       1               0.00            100.00          12              

BETTER HANDS

  #   HAND                
  3 | Three K's           
  3 | Three J's           
  3 | Three 8's           
  3 | Three 5's           
  3 | Three 2's           
  9 | K's and J's         
  9 | K's and 8's         
  9 | K's and 5's         
  9 | K's and 2's         
  9 | J's and 8's         
  9 | J's and 5's         
  9 | J's and 2's         
  9 | 8's and 5's         
  9 | 8's and 2's         
  9 | 5's and 2's         
  3 | Pair of A's         
 84 | Pair of K's         
  6 | Pair of Q's         
 84 | Pair of J's         
  3 | Pair of T's         
  6 | Pair of 9's         
 84 | Pair of 8's         
  6 | Pair of 7's         
  3 | Pair of 6's         
 84 | Pair of 5's         
  3 | Pair of 4's         
  6 | Pair of 3's         
 84 | Pair of 2's         
 12 | A-high              
573   TOTAL               
```
