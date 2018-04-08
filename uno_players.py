from uno_objs import Hand

class Player():

    def __init__(self, name):
        self.name = name
        self.id = -1
        self.type = 'human'
        self.hand = Hand()
        self.forceDraw = 0
        self.points = 0

    def addCard(self, card):
        if self.forceDraw > 0:
            self.forceDraw -= 1
        self.hand.addCard(card)

    def addPoints(self, amount):
        if (self.points + amount) <= 999999999999999999999:
            self.points += amount

    def assignID(self, identity):
        self.id = identity

    def checkCard(self, index):
        return self.hand.getCard(int(index))

    def discardHand(self):
        self.hand.discard()

    def removeCard(self, index):
        return self.hand.removeCard(index)

    def getAllLegalCards(self, color, value):
        out = {'all': [],
               'wild': [],
               'values' : [],
               'special' : [],
               'canDrawTwo' : False,
               'canReverse': False,
               'canSkip': False,
               'canValueChange' : False
               }
        for i, card in enumerate(self.hand):
            if card.value == value or card.color == color:
                out['all'].append(i)
                if card.color != color:
                    out['values'].append(i)
                    out['canValueChange'] = True
                if card.value in ('+2', 'R', 'X'):
                    out['special'].append(i)
                    if card.value == 'R':
                        out['canReverse'] = True
                    elif card.value == 'X':
                        out['canSkip'] = True
                    elif card.value == '+2':
                        out['canDrawTwo'] = True
            elif card.value in ('W','+4'):
                out['wild'].append(i)
        canPlusFour = len(out['all']) == 0
        for index in out['wild']:
            card = self.hand[index]
            if card.value == '+4':
                if canPlusFour:
                    out['all'].append(index)
            else:
                out['all'].append(index)
        return out

class ComputerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.type = 'computer'
        self.colorsInHand = {
            'blue' : 0,
            'red' : 0,
            'green' : 0,
            'yellow' : 0,
        }

    def addCard(self, card):
        super().addCard(card)
        if card.color in ('red','blue','green','yellow'):
            self.colorsInHand[card.color] += 1

    def removeCard(self, index):
        card = super().removeCard(index)
        if card.color in ('red', 'blue', 'green', 'yellow'):
            self.colorsInHand[card.color] -= 1
        return card

    def think(self, match):
        legalCards = self.getAllLegalCards(match.currentColor, match.currentValue)

        if len(legalCards['all']) == 0:
            if len(match.deck) == 0:
                pass