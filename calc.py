#!/usr/bin/env python3

import enum
import itertools as it

class Rank(enum.IntEnum):
  def __new__(cls, char):
    value = len(cls.__members__) + 1
    member = int.__new__(cls, value)
    member._value_ = value
    member.char = char
    return member
  
  TWO   = '2'
  THREE = '3'
  FOUR  = '4'
  FIVE  = '5'
  SIX   = '6'
  SEVEN = '7'
  EIGHT = '8'
  NINE  = '9'
  TEN   = 'T'
  JACK  = 'J'
  QUEEN = 'Q'
  KING  = 'K'
  ACE   = 'A'

#for r in Rank:
#  print(r, r.name, r.value, r.char)

class Suit(enum.IntEnum):
  def __new__(cls, char):
    value = len(cls.__members__) + 1
    member = int.__new__(cls, value)
    member._value_ = value
    member.char = char
    return member
  
  SPADE   = 's'
  HEART   = 'h'
  DIAMOND = 'd'
  CLUB    = 'c'

#print
#for s in Suit:
#  print(s, s.name, s.value, s.char)

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
  
  def __repr__(self):
    return "<Card: {}>".format(self.__str__())
  
  def __str__(self):
    return "{}{}".format(self.rank.char, self.suit.char)

class Deck:
  def __init__(self):
    self.deck = [Card(r, s) for (r, s) in it.product(Rank, Suit)]
    self.card_dict = {c.__str__():c for c in self.deck}
  
  def getCard(self, s):
    return self.card_dict[s]

def hole2list(h):
  # This clones the iterator
  args = [iter(h)] * 2
  # Zipping the iterator with its clone takes 2-char slices
  return [''.join(x) for x in it.zip_longest(*args)]
  
def main(args):
  d = Deck()
  hc = [d.getCard(c) for c in hole2list(args.hole_cards)]
  print(hc)
  
if __name__ == '__main__':
  import argparse as ap
  import sys
  
  parser = ap.ArgumentParser("calc.py")
  
  parser.add_argument("hole_cards", action="store")
  parser.add_argument("flop", nargs='?', action="store")
  parser.add_argument("turn", nargs='?', action="store")
  parser.add_argument("river", nargs='?', action="store")
  
  args = parser.parse_args(sys.argv[1:])
  
  #print(args)
  main(args)
