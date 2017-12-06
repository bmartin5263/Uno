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
               'wild': []}
        for i, card in enumerate(self.hand):
            if card.value == value or card.color == color:
                out['all'].append(i)
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
        self.legalCards = []
        self.wildCards = []
        self.valueChangeCards = []
        self.zeroCards = []
        self.canSkip = False
        self.canReverse = False
        self.canDrawTwo = False
        self.canDrawFour = False
        self.canValueChange = False

    def think(self, match):
        legalCards = self.getAllLegalCards(match.currentColor, match.currentValue)

        if len(legalCards['all']) == 0:
            if len(match.deck) == 0:
                pass