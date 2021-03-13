#!/usr/bin/env python3

import enum
from itertools import product, combinations, zip_longest, groupby
from functools import total_ordering

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

@total_ordering
class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
  
  def __gt__(self, other):
    return (self.rank, self.suit) > (other.rank, other.suit)
  
  def __eq__(self, other):
    return (self.rank, self.suit) == (other.rank, other.suit)
  
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

@total_ordering
class Hand:
  '''
  A five-card poker hand
  '''
  def __init__(self, *cards):
    self.cards = cards
    self.sCards = sorted(cards, reverse=True)
    self.rank = self._handEval()

  def __gt__(self, other):
    if self.rank == other.rank:
      if self.rank in (HandRank.STRAIGHT, HandRank.STRAIGHT_FLUSH):
        # Omit the highest card in the straight so that low-A straights are handled properly
        return self.rankList[1:] > other.rankList[1:]
      else:
        return self.rankList > other.rankList
    else:
      return self.rank > other.rank
  
  def __eq__(self, other):
    if self.rank == other.rank:
      return self.rankList == other.rankList
    else:
      return False

  def __repr__(self):
    return "<Hand: {}>".format(" ".join([c.__repr__() for c in self.cards]))
  
  def __str__(self):
    return self.to_string(self.cards)
  
  @staticmethod
  def to_string(cList):
    return " ".join([c.__str__() for c in cList])
  
  def _flushCheck(self):
    '''
    Returns True if all cards have same suit, False otherwise
    '''
    flush = True
    lastSuit = None
    for c in self.sCards:
      if lastSuit == None:
        lastSuit = c.suit
        continue
      else:
        if c.suit != lastSuit:
          # Can't have a flush
          flush = False
          break
    return flush

  def _handEval(self):
    # Group the cards by rank and count how many of each there are
    # Note: this works because the hand is sorted by rank
    self.rankList = sorted([(len([*g]), k) for k, g in groupby(self.sCards, lambda x : x.rank)], reverse=True)
    #!print(rankList)
    numRanks = len(self.rankList)
    
    # A straight is possible if there are 5 ranks and...
    # (the highest and lowest cards are 4 apart or ...
    #  the highest and 2nd highest cards are 9 apart, which can only happen with A & 5)
    if (numRanks == 5) and ((self.sCards[0].rank - self.sCards[4].rank == 4) or (self.sCards[0].rank - self.sCards[1].rank == 9)):
      straight = True
    else:
      straight = False
    #!print("Straight = {}".format(straight))
    
    # A flush is only possible if every suit is the same as the previous one
    flush = self._flushCheck()
    #!print("Flush = {}".format(flush))
    
    # This step wouldn't be necessary if the k were _ when creating RankList
    multi = [x[0] for x in self.rankList]
    # [4, 1] = four of a kind
    # [3, 2] = full house
    # [3, 1, 1] = three of a kind
    # [2, 2, 1] = two pair
    # [2, 1, 1, 1] = one pair
    # [1, 1, 1, 1, 1] = high card
    #!print(multi)
    
    # If the 2nd highest card in a straight flush is a King ==> Royal!
    if straight and flush:
      if hs[1].rank == Rank.KING:
        hr = HandRank.ROYAL_FLUSH
      else:
        hr = HandRank.STRAIGHT_FLUSH
    elif multi == [4, 1]:
      hr = HandRank.FOUR_OF_A_KIND
    elif multi == [3, 2]:
      hr = HandRank.FULL_HOUSE
    elif flush:
      hr = HandRank.FLUSH
    elif straight:
      hr = HandRank.STRAIGHT
    elif multi == [3, 1, 1]:
      hr = HandRank.THREE_OF_A_KIND
    elif multi == [2, 2, 1]:
      hr = HandRank.TWO_PAIR
    elif multi == [2, 1, 1, 1]:
      hr = HandRank.ONE_PAIR
    else:
      hr = HandRank.HIGH_CARD
    #!print(hr)
    #!print()
    
    return hr

class OmahaHand:
  '''
  '''
  def __init__(self, hand, board):
    self.hand = hand
    self.board = board
    # Warning: hCombos is an iterator
    self.hCombos = product(combinations(hand,2),combinations(board,3))
    self.handList = [Hand(*(h+b)) for h, b in self.hCombos]
    self.rank, self.bestHand, self.bestHandIdx = max([(x.rank, x, i) for (i, x) in enumerate(self.handList)])
  
  def debugPrint(self):
    print("{} | {} - {}".format(Hand.to_string(self.hand), Hand.to_string(self.board), self.bestHand.rank.string))
    print()
    for i, h in enumerate(self.handList):
      if i == self.bestHandIdx:
        print("{} *".format(h))
      else:
        #print(h)
        pass

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
    
    oh = OmahaHand(hc, bc)
    oh.debugPrint()

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
  
  # Ad7dAs4d 4sAhAc
  
