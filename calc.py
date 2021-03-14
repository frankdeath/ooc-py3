#!/usr/bin/env python3

from enum import IntEnum
from collections import Counter
from itertools import product, combinations, zip_longest, groupby, filterfalse
from functools import total_ordering

class HandRank(IntEnum):
  def __new__(cls, string):
    value = len(cls.__members__)
    member = int.__new__(cls, value)
    member._value_ = value
    member.string = string
    return member
  
  HIGH_CARD       = 'High Card'
  ONE_PAIR        = 'One Pair'
  TWO_PAIR        = 'Two Pair'
  THREE_OF_A_KIND = 'Three of a Kind'
  STRAIGHT        = 'Straight'
  FLUSH           = 'Flush'
  FULL_HOUSE      = 'Full House'
  FOUR_OF_A_KIND  = 'Four of a Kind'
  STRAIGHT_FLUSH  = 'Straight Flush'
  ROYAL_FLUSH     = 'Royal Flush'

#for hr in HandRank:
#  print(hr, hr.name, hr.value, hr.string)

class Rank(IntEnum):
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

class Suit(IntEnum):
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
  
  def __len__(self):
    return(len(self.deck))
  
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
    #!print(cards)
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
      if self.sCards[1].rank == Rank.KING:
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

@total_ordering
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
  
  def __gt__(self, other):
    return self.bestHand.__gt__(other.bestHand)
  
  def __eq__(self, other):
    return self.bestHand.__eq__(other.bestHand)
  
  def debugPrint(self):
    print()
    print("{} | {} - {}".format(Hand.to_string(self.hand), Hand.to_string(self.board), self.bestHand.rank.string))
    print()
    #for i, h in enumerate(self.handList):
    #  if i == self.bestHandIdx:
    #    print("{} *".format(h))
    #  else:
    #    #print(h)
    #    pass
  
  
def cardsToList(h):
  # This clones the iterator
  args = [iter(h)] * 2
  # Zipping the iterator with its clone takes 2-char slices
  return [''.join(x) for x in zip_longest(*args)]

def countBetterHands(oh, deck):
  '''
  Enumerate the number of 5-hard hands that can be made with the
  existing board that are better than the given hand.  Assume that
  deck already has oh.hand removed to avoid recreating deck.
  '''
  bhc = Counter({r : 0 for r in HandRank})
  total = 0
  
  for h1, h2 in combinations(deck, 2):
    h = OmahaHand([h1, h2], oh.board)
    if h > oh:
      bhc[h.rank] += 1
    total += 1
  
  return (bhc, total)
    
def printStats(name, ctr, bhc, bht):
  total = sum(ctr.values())
  
  print(name)
  print()
  header = "{:<16}{:<16}{:<16}{:<16}{:<16}".format("Hand", "out of {}".format(total), "Odds 1:", "Probability", "# Better / {}".format(bht))
  print(header)
  
  for r in sorted(HandRank, reverse=True):
    if ctr[r] != 0:
      odds = total / ctr[r] - 1.0
    else:
      odds = 0.0
    percent = ctr[r] / total * 100.0
    print("{:<16}{:<16}{:<16.2f}{:<16.2f}{:<16}".format(r.string, ctr[r], odds, percent, bhc[r]))
  print()

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
    bhc, bht = countBetterHands(oh, d.deck)
    #!print(bhc)
    oh.debugPrint()
    
    if args.turn == None:
      ### calc turn stats
      tc = Counter({r : 0 for r in HandRank})
      
      for turn in d.deck:
        th = OmahaHand(hc, bc+[turn,])
        tc[th.rank] += 1
        #th.debugPrint()
      
      ### calc river stats
      rc = Counter({r : 0 for r in HandRank})
      
      for turn, river in combinations(d.deck, 2):
        rh = OmahaHand(hc, bc+[turn, river])
        rc[rh.rank] += 1
      
      #!print(tc)
      printStats("TURN", tc, bhc, bht)
      
      #print(rc)
      printStats("RIVER", rc, bhc, bht)
    
    elif args.river == None:
      ### calc river stats
      rc = Counter({r : 0 for r in HandRank})
      
      for river in d.deck:
        rh = OmahaHand(hc, bc+[river,])
        rc[rh.rank] += 1
      
      #print(rc)
      printStats("RIVER", rc, bhc, bht)
    
    else:
      ### calc showdown stats
      sc = Counter({r : 0 for r in HandRank})
      sc[oh.rank] += 1
      
      printStats("SHOWDOWN", sc, bhc, bht)
    
    # When calculating better hands...
    #for bc in d.deck:
    #  print(bc)
    #  print(*filterfalse(lambda x : x == bc, d.deck))


if __name__ == '__main__':
  import argparse as ap
  import sys
  
  parser = ap.ArgumentParser("calc.py")
  
  parser.add_argument("hole_cards", action="store")
  #parser.add_argument("flop", nargs='?', action="store")
  # Require flop until hutchison point calc is implemented
  parser.add_argument("flop", action="store")
  parser.add_argument("turn", nargs='?', action="store")
  parser.add_argument("river", nargs='?', action="store")
  
  args = parser.parse_args(sys.argv[1:])
  
  #print(args)
  main(args)
  
  # Ad7dAs4d 4sAhAc
  
