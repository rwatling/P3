'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"
    # hand = who's hand it is
    # cards = the cards they have in their possesion
    
    returnList = []
    tempList = []
    for c in cards:
        tempList = Cluedo.getIdentifierFromNames(hand, c)
        returnList.append([tempList])
        tempList = []

    return returnList

def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """

    "*** YOUR CODE HERE ***"
    cards = Cluedo.cards
    hands = Cluedo.hands
    retList = []
    tempList = []

    for c in cards:
        for hand in hands:
            identifier = Cluedo.getIdentifierFromNames(hand, c)
            tempList.append(identifier)

        retList.append(tempList)
        tempList = []
    
    return retList

def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    cards = Cluedo.cards
    hands = Cluedo.hands
    retList = []
   
    for c in range(len(cards)):
        for i in range(len(hands)):
            for j in range((i+1), len(hands)):
                id_i = Cluedo.getIdentifierFromIndicies(i, c)
                id_j = Cluedo.getIdentifierFromIndicies(j, c)
                
                retList.append([-1 * id_i, -1 * id_j])
    
    return retList

def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    weapons = Cluedo.weapons
    suspects = Cluedo.suspects
    rooms = Cluedo.rooms
    weaponLoc = []
    suspectLoc = []
    roomLoc = []
    retList = []
    casefile = Cluedo.casefile

    for w in weapons:
        weaponLoc.append(Cluedo.getIdentifierFromNames(casefile, w))

    for s in suspects:
        suspectLoc.append(Cluedo.getIdentifierFromNames(casefile, s))

    for r in rooms:
        roomLoc.append(Cluedo.getIdentifierFromNames(casefile,r))

    retList.append(weaponLoc)
    retList.append(suspectLoc)
    retList.append(roomLoc)

    return retList

def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    weapons = Cluedo.weapons
    suspects = Cluedo.suspects
    rooms = Cluedo.rooms
    caseIndex = len(Cluedo.hands) - 1
    retList = []

    for w in range(len(weapons)):
        for w2 in range(w+1, len(weapons)):
            id_w = Cluedo.getIdentifierFromIndicies(caseIndex, w)
            id_w2 = Cluedo.getIdentifierFromIndicies(caseIndex, w2)
            retList.append([-1 * id_w, -1 * id_w2])
    
    for s in range(len(suspects)):
        for s2 in range(s+1, len(suspects)):
            id_s = Cluedo.getIdentifierFromIndicies(caseIndex, s)
            id_s2 = Cluedo.getIdentifierFromIndicies(caseIndex, s2)
            retList.append([-1 * id_s, -1 * id_s2])

    for r in range(len(rooms)):
        for r2 in range(r+1, len(rooms)):
            id_r = Cluedo.getIdentifierFromIndicies(caseIndex, r)
            id_r2 = Cluedo.getIdentifierFromIndicies(caseIndex, r2)
            retList.append([-1 * id_r, -1 * id_r2])
    
    return retList

def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    suspects = Cluedo.suspects
    cards = Cluedo.cards

    print(suggester)
    print(card1)
    print(card2)
    print(card3)
    print(refuter)
    print(cardShown)

    # Case 3: No Refuter
    if ((refuter == None) and (cardShown == None)):
        print("case 3")
    
    # Case 2: A card is hidden
    elif (cardShown == None):
        print("case 2")
    
    # Case 1: There is a refuter and they show their card
    else:
        i = suspects.index(suggester)
        j = suspects.index(refuter)
        infoList = []

        while (i != j):
            
            # Cycle through suspect list
            i += 1
            if (i == len(suspects)):
                i = 0
            
            # Card indices
            c1 = cards.index(card1)
            c2 = cards.index(card2)
            c3 = cards.index(card3)

            # Gather information
            # Not the refuters turn
            if (i != j):
                infoList.append([-1 * Cluedo.getIdentifierFromIndicies(i, c1)])
                infoList.append([-1 * Cluedo.getIdentifierFromIndicies(i, c2)])
                infoList.append([-1 * Cluedo.getIdentifierFromIndicies(i, c3)])
            # The refuter's turn
            elif (i == j):
                infoList.append([Cluedo.getIdentifierFromNames(refuter, cardShown)])

        return infoList
    
    return None

def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    return []
