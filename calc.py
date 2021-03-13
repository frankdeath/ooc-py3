#!/usr/bin/env python3

import enum
from itertools import product, combinations, zip_longest

class HandRank(enum.IntEnum):
  def __new__(cls, string):
    value = len(cls.__members__)
    member = int.__new__(cls, value)
    member._value_ = value
    member.string = string
    return member
  
  HIGH_CARD       = 'high card'
  ONE_PAIR        = '1 pair'
  TWO_PAIR        = '2 pair'
  THREE_OF_A_KIND = '3 of a kind'
  STRAIGHT        = 'straight'
  FLUSH           = 'flush'
  FULL_HOUSE      = 'full house'
  FOUR_OF_A_KIND  = '4 of a kind'
  STRAIGHT_FLUSH  = 'straight flush'
  ROYAL_FLUSH     = 'royal flush'

#for hr in HandRank:
#  print(hr, hr.name, hr.value, hr.string)

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
    self.deck = [Card(r, s) for (r, s) in product(Rank, Suit)]
    self.card_dict = {c.__str__():c for c in self.deck}
  
  def lookupCard(self, s):
    return self.card_dict[s]
  
  def takeCard(self, s):
    card = self.card_dict[s]
    self.deck.remove(card)
    return card

def cardsToList(h):
  # This clones the iterator
  args = [iter(h)] * 2
  # Zipping the iterator with its clone takes 2-char slices
  return [''.join(x) for x in zip_longest(*args)]
  
def main(args):
  try:
    d = Deck()
    hc = [d.takeCard(c) for c in cardsToList(args.hole_cards)]
    bcs = "".join([x for x in (args.flop, args.turn, args.river) if x != None])
    bc = [d.takeCard(c) for c in cardsToList(bcs)]
  except ValueError:
    print("Error: card specified multiple times")
  else:
    #!print(hc)
    #!print(bc)
    handCombos = product(combinations(hc,2),combinations(bc,3))
    i = 0
    for h, b in handCombos:
      print(h+b)
      i += 1
    #!print(i)

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
