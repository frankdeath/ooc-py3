#!/usr/bin/env python3

from enum import IntEnum
from collections import Counter, deque
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
    self.rank, self.name = self._handEval()

  def __gt__(self, other):
    if self.rank == other.rank:
      if self.rank in (HandRank.STRAIGHT, HandRank.STRAIGHT_FLUSH):
        # Use the highest card in the straight for the comparison
        # 5 is the highest card in the wheel, even though it has an ace
        
        if self.rankList[0][1] - self.rankList[1][1] == 9:
          sRank = self.rankList[1][1]
        else:
          sRank = self.rankList[0][1]
        
        if other.rankList[0][1] - other.rankList[1][1] == 9:
          oRank = self.rankList[1][1]
        else:
          oRank = self.rankList[0][1]
        
        return sRank > oRank
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
    # Group the cards by rank and count how many of each there are. [(#, Rank), ...]
    # NOTE: this works because the hand is sorted by rank
    self.rankList = sorted([(len([*g]), k) for k, g in groupby(self.sCards, lambda x : x.rank)], reverse=True)
    highestRank = self.rankList[0][1]
    secondHighestRank = self.rankList[1][1]
    numRanks = len(self.rankList)
    
    # Assume there isn't a straight (wheel = A2345)
    straight = wheel = False
    #wheel = False
    # A straight is possible if there are 5 ranks and...
    # (the highest and lowest cards are 4 apart--a normal straight--or ...
    #  the highest and 2nd highest cards are 9 apart, which can only happen with A & 5)
    if (numRanks == 5):
      if (self.sCards[0].rank - self.sCards[4].rank == 4):
        straight = True
      if (self.sCards[0].rank - self.sCards[1].rank == 9):
        straight = True
        wheel = True
    
    # A flush is only possible if every suit is the same as the previous one
    flush = self._flushCheck()
    
    # This step wouldn't be necessary if the k were _ when creating RankList
    multi = [x[0] for x in self.rankList]
    # [4, 1] = four of a kind
    # [3, 2] = full house
    # [3, 1, 1] = three of a kind
    # [2, 2, 1] = two pair
    # [2, 1, 1, 1] = one pair
    # [1, 1, 1, 1, 1] = high card (also straight / flush / straight flush)
    
    # If the 2nd highest card in a straight flush is a King ==> Royal!
    if straight and flush:
      if self.sCards[1].rank == Rank.KING:
        hr = HandRank.ROYAL_FLUSH
        hn = hr.string
      else:
        hr = HandRank.STRAIGHT_FLUSH
        if wheel:
          hn = "{}-high {}".format(secondHighestRank.char, hr.string)
        else:
          hn = "{}-high {}".format(highestRank.char, hr.string)
    elif multi == [4, 1]:
      hr = HandRank.FOUR_OF_A_KIND
      hn = "Four {}'s".format(highestRank.char)
    elif multi == [3, 2]:
      hr = HandRank.FULL_HOUSE
      hn = "{}'s over {}'s".format(highestRank.char, secondHighestRank.char)
    elif flush:
      hr = HandRank.FLUSH
      hn = "{}-high {}".format(highestRank.char, hr.string)
    elif straight:
      hr = HandRank.STRAIGHT
      if wheel:
        hn = "{}-high {}".format(secondHighestRank.char, hr.string)
      else:
        hn = "{}-high {}".format(highestRank.char, hr.string)
    elif multi == [3, 1, 1]:
      hr = HandRank.THREE_OF_A_KIND
      hn = "Three {}'s".format(highestRank.char)
    elif multi == [2, 2, 1]:
      hr = HandRank.TWO_PAIR
      hn = "{}'s and {}'s".format(highestRank.char, secondHighestRank.char)
    elif multi == [2, 1, 1, 1]:
      hr = HandRank.ONE_PAIR
      hn = "Pair of {}'s".format(highestRank.char)
    else:
      hr = HandRank.HIGH_CARD
      hn = "{}-high".format(highestRank.char)
    
    return (hr, hn)


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
  
  def __repr__(self):
    return "<OmahaHand: {} {}>".format("".join([x.__str__() for x in self.hand]), "".join([x.__str__() for x in self.board]))
  
  def pprint(self):
    print()
    if self.bestHand.rank == HandRank.ROYAL_FLUSH:
      print("{} | {} - {}".format(Hand.to_string(self.hand), Hand.to_string(self.board), self.bestHand.rank.string))
    else:
      print("{} | {} - {}: {}".format(Hand.to_string(self.hand), Hand.to_string(self.board), self.bestHand.rank.string ,self.bestHand.name))
    print()


def cardsToList(h):
  # This clones the iterator
  args = [iter(h)] * 2
  # Zipping the iterator with its clone takes 2-char slices
  return [''.join(x) for x in zip_longest(*args)]


def countBetterHands(oh, deck, saveHands):
  '''
  Enumerate the number of 5-hard hands that can be made with the
  existing board that are better than the given hand.  Assume that
  deck already has oh.hand removed to avoid recreating deck.
  '''
  bhc = Counter({r : 0 for r in HandRank})
  total = 0
  handList = []
  
  for h1, h2 in combinations(deck, 2):
    h = OmahaHand([h1, h2], oh.board)
    if h > oh:
      bhc[h.rank] += 1
      if saveHands:
        handList.append(h)
    total += 1
  
  return (bhc, total, sorted(handList, reverse=True))


def hutchison(hole):
  hr = sorted(hole, reverse=True)
  # rankGroups element: ( # of rank, rank )
  rankGroups = [(len([*g]),k) for k, g in groupby(hr, lambda x: x.rank)]
  #!print(rankGroups)
  numRanks = len(rankGroups)
  #!print(f'{numRanks = }')
  hs = sorted(hole, reverse=True, key=lambda y: (y.suit, y.rank))
  # suitGroups element: ( [ list of ranks ], suit )
  suitGroups = [([c.rank for c in g], k) for k, g in groupby(hs, lambda z: z.suit)]
  #!print(suitGroups)
  score = 0
  
  # Phase 1 - Contribution from suited cards
  bonus1 = {Rank.ACE : 8, Rank.KING : 6, Rank.QUEEN : 5, Rank.JACK : 4, Rank.TEN : 3, Rank.NINE : 3, Rank.EIGHT : 2,
            Rank.SEVEN : 1, Rank.SIX : 1, Rank.FIVE : 1, Rank.FOUR : 1, Rank.THREE : 1, Rank.TWO : 1}
  penalty1 = -2
  phase1 = 0
  
  for s in suitGroups:
    # If there are at least two cards with the same suit
    if len(s[0]) > 1:
      # The bonus is based on the highest rank
      phase1 += bonus1[s[0][0]]
      
      # There is a penalty for more than two cards of the same suit (only applies once)
      if len(s[0]) > 2:
        phase1 += penalty1
  
  #!print(f'{phase1 = }')
  score += phase1
  
  # Phase 2 - Contribution from pairs
  bonus2 = {Rank.ACE : 18, Rank.KING : 16, Rank.QUEEN : 14, Rank.JACK : 13, Rank.TEN : 12, Rank.NINE : 10, Rank.EIGHT : 8,
            Rank.SEVEN : 7, Rank.SIX : 7, Rank.FIVE : 7, Rank.FOUR : 7, Rank.THREE : 7, Rank.TWO : 7}
  phase2 = 0
  
  for r in rankGroups:
    # Bonuses only apply to pairs
    if r[0] == 2:
      phase2 += bonus2[r[1]]
  
  #!print(f'{phase2 = }')
  score += phase2
  
  # Phase 3 - Contribution from straight cards
  bonus3 = {4 : 25, 3 : 18, 2 : 8}
  gapPenalty = -2
  acePenalty = -4
  aceLowBonus = {1 : 6, 2 : 12}
  phase3 = 0
  
  # Helper function from stack overflow
  def _nwise_slice(it, n):
      deq = deque((), n)
      for x in it:
          deq.append(x)
          if len(deq)==n: yield deq
  
  # Recursive function that does all the phase-3 work
  def _calcStraightBonus(_rankGroupList):
    '''
    A recursive function that checks whether groups of cards can make straights, using smaller groups with each level of recursion.
    '''
    _points = 0
    _numRanks = len(_rankGroupList)
    #!print(f'Start: {_numRanks = } {_rankGroupList = }')
    if _numRanks > 1:
      _maxRankDiff = _rankGroupList[0][1] - _rankGroupList[-1][1]
      if _maxRankDiff < 5: 
        # _numRanks cards can make a straight
        # _gaps = _maxRankDiff - 1 - (_numRanks - 2)
        _gaps = _maxRankDiff - _numRanks + 1
        _points += bonus3[_numRanks] + (_gaps * gapPenalty)
        
        if _rankGroupList[0][1] == Rank.ACE:
          _points += acePenalty
        
      else:
        # See if (_numRanks-1) slices can make a straight
        for _rankGroupSlice in _nwise_slice(_rankGroupList, _numRanks-1):
          #!print(f'Recursing: {_rankGroupSlice = }')
          _points += _calcStraightBonus(_rankGroupSlice)
    #!print(f'Done: {_numRanks = }, {_points = }')
    return _points
  
  def _calcAceModifier(_rankGroupList):
    '''
    '''  
  
  # Hands with Aces are special
  if rankGroups[0][1] == Rank.ACE:
    # Count how many low cards there are
    numLow = [x[1] < Rank.SIX for x in rankGroups].count(True)
    
    if numLow == 3:
      # Ace + 3 low cards
      phase3 += aceLowBonus[2]
    elif numLow == 2:
      # Ace + 2 low cards
      phase3 += aceLowBonus[2]
      phase3 += _calcStraightBonus(rankGroups[:-numLow])
    elif numLow == 1:
      # Ace + 1 low card
      phase3 += aceLowBonus[1]
      phase3 += _calcStraightBonus(rankGroups[:-numLow])
    else:
      # Ace + no low cards
      phase3 += _calcStraightBonus(rankGroups)
  else:
    phase3 += _calcStraightBonus(rankGroups)
  
  #!print(f'{phase3 = }')
  score += phase3
  
  #!print(f'{score = }')
  return score


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
    
    if args.flop == None:
      s = hutchison(hc)
      print("Hutchison score: {}".format(s))
      print("Approximate win: {:.1f}%".format(s/2.0)) 
    else:
      oh = OmahaHand(hc, bc)
      bhc, bht, bhl = countBetterHands(oh, d.deck, saveHands=args.better_hands)
      
      if args.turn == None:
        ### calc turn stats
        tc = Counter({r : 0 for r in HandRank})
        
        for turn in d.deck:
          th = OmahaHand(hc, bc+[turn,])
          tc[th.rank] += 1
        
        ### calc river stats
        rc = Counter({r : 0 for r in HandRank})
        
        for turn, river in combinations(d.deck, 2):
          rh = OmahaHand(hc, bc+[turn, river])
          rc[rh.rank] += 1
        
        oh.pprint()
        printStats("TURN", tc, bhc, bht)
        printStats("RIVER", rc, bhc, bht)
      
      elif args.river == None:
        ### calc river stats
        rc = Counter({r : 0 for r in HandRank})
        
        for river in d.deck:
          rh = OmahaHand(hc, bc+[river,])
          rc[rh.rank] += 1
        
        oh.pprint()
        printStats("RIVER", rc, bhc, bht)
      
      else:
        ### calc showdown stats
        sc = Counter({r : 0 for r in HandRank})
        sc[oh.rank] += 1
        
        oh.pprint()
        printStats("SHOWDOWN", sc, bhc, bht)
      
      if args.better_hands:
        print("BETTER HANDS")
        print()
        print("{:>3}   {:<20}".format("#", "HAND"))
        
        for n, h in [(len([*g]), k) for k, g in groupby(bhl, lambda x : x.bestHand.name)]:
          print("{:>3} | {:<20}".format(n, h))
        print("{:>3}   {:<20}".format(sum(bhc.values()), "TOTAL"))


if __name__ == '__main__':
  import argparse as ap
  import sys
  
  parser = ap.ArgumentParser("calc.py")
  
  parser.add_argument("hole_cards", action="store")
  parser.add_argument("flop", nargs='?', action="store")
  parser.add_argument("turn", nargs='?', action="store")
  parser.add_argument("river", nargs='?', action="store")
  parser.add_argument("-b", action="store_true", dest="better_hands", help="Show better hands")
  
  args = parser.parse_args(sys.argv[1:])
  
  main(args)
