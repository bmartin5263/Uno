from uno_objs import Card, Deck, Hand
import time
import random
import threading

class Match():

    def __init__(self, players, ui):
        self.players = players
        self.ui = ui
        self.complete = False
        self.threads = None

        self.playerControlled = []
        self.computerControlled = []

        self.deck = Deck(True)
        self.pile = Deck(False)

        self.displayEffects = True
        self.computerSpeed = 0

        self.turn = None
        self.turnComplete = False
        self.reverse = False
        self.currentColor = None
        self.currentValue = None

    def eventBegin(self):
        self.ui.console("Beginning Match, Press Enter")
        self.ui.getInput()
        self.ui.console("Dealing Cards...")
        for i, player in enumerate(self.players):
            for j in range(7):
                card = self.deck.drawCard()
                player.addCard(card.getUIData())
                if self.displayEffects:
                    if i == len(self.players) - 1:
                        self.ui.importHand(player.hand,player.name, True)
                    self.ui.updateCardCount(i, len(player.hand))
                    time.sleep(.1)
        self.turn = random.randrange(0,len(self.players))
        self.ui.console("First Turn will be {}, Press Enter".format(self.players[self.turn].name))
        self.ui.getInput()
        self.ui.emphasizePlayer(self.turn)
        time.sleep(2)

    def getInput(self, playerType):
        if playerType == 0:
            while not self.complete:
                if self.turn in self.playerControlled:
                    pass

        elif playerType == 1:
            while not self.complete:
                pass

        else:
            while not self.complete:
                pass

    def setupInterface(self):
        for i, player in enumerate(self.players):
            self.ui.importPlayer(i, player.name)
        self.ui.hidePile()
        self.ui.hideCards()

    def setupThreads(self):
        self.threads = []
        for i, player in enumerate(self.players):
            if player.type == 'human':
                self.playerControlled.append(i)
            else:
                self.computerControlled.append(i)
        if len(self.playerControlled) > 0:
            thread = threading.Thread(target=self.getInput, args=(0,))
            self.threads.append(thread)
        if len(self.computerControlled) > 0:
            thread = threading.Thread(target=self.getInput, args=(1,))
            self.threads.append(thread)
        thread = threading.Thread(target=self.getInput, args=(2,))
        self.threads.append(thread)

    def start(self):
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()

    def play(self):
        self.setupInterface()
        self.eventBegin()
        self.setupThreads()
        self.start()
        return self.players