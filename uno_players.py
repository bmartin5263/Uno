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