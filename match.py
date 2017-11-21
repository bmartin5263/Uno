from uno_objs import Card, Deck, Hand
import curses
import time
import random
import threading
import queue

class Match():

    TURN_INPUT = (ord(' '),)
    HAND_INPUT = (curses.KEY_LEFT, curses.KEY_RIGHT, ord('d'))
    INITIAL_CARD_COUNT = 7
    WILD_CARDS = ('+4', 'W')
    WILD_INPUT = (ord('b'),ord('g'),ord('y'),ord('r'))
    COLOR_ABBREVIATIONS = {
        ord('b'):'blue',
        ord('r'):'red',
        ord('g'):'green',
        ord('y'):'yellow'
    }

    def __init__(self, players, ui):
        self.players = players
        self.ui = ui
        self.complete = False

        self.playerControlled = []
        self.computerControlled = []

        self.deck = Deck(True)
        self.pile = Deck(False)

        self.displayEffects = True
        self.computerSpeed = 0

        self.errorMessage = ''
        self.errorTime = None

        self.turn = None
        self.cardPointer = -1
        self.currentHand = None
        self.turnComplete = False
        self.reverse = False
        self.currentColor = None
        self.currentValue = None

    def eventBegin(self):
        self.ui.console("Beginning Match, Press Enter")
        self.ui.getInput()
        self.ui.console("Dealing Cards...")
        for i, player in enumerate(self.players):
            for j in range(Match.INITIAL_CARD_COUNT):
                card = self.deck.drawCard()
                self.ui.importDeck(self.deck)
                player.addCard(card)
                if i == len(self.players) - 1:
                    self.ui.importHand(player.hand.getUIData(),player.name, True, True)
                self.ui.updateCardCount(i, len(player.hand))
                if self.displayEffects:
                    time.sleep(.1)
        self.turn = random.randrange(0,len(self.players))
        self.ui.console("First Turn will be {}, Press Enter".format(self.players[self.turn].name))
        self.ui.getInput()
        card = self.deck.drawCard()
        #card = Card('blue','R')
        self.pile.addCard(card)
        self.ui.importCard(self.pile[0].getUIData(), False, self.reverse)
        for i in range(12):
            self.ui.expandTopCard(i,self.reverse)
        self.currentColor = card.color
        self.currentValue = card.value

    def eventReverse(self):
        self.ui.error('Reverse Card Played! Reversing Turn Order.')
        time.sleep(1)
        for i in range(10):
            self.ui.eventReverse(i, self.reverse)

    def eventWild(self):
        for i in range(17):
            self.ui.wildColor(i)

    def removeCard(self, player):
        card = player.removeCard(self.cardPointer)
        self.ui.updateCardCount(self.turn, len(player.hand), True)
        self.ui.setCardPointer(-1)

        self.pile.addCard(card)
        self.ui.importCard(self.pile[len(self.pile) - 1].getUIData(), False, self.reverse)
        self.ui.importHand(self.players[self.turn].hand.getUIData(), self.players[self.turn].name,
                           False, False)

        for i in range(12):
            self.ui.expandTopCard(i, self.reverse)
        self.currentColor = card.color
        self.currentValue = card.value

    def getInput(self):
        while not self.complete:
            curses.flushinp()
            k = self.ui.getInput()
            return k

    def getNextTurn(self, forceReverse=False):
        if forceReverse:
            reverse = not self.reverse
        else:
            reverse = self.reverse
        currentIndex = self.turn
        if not reverse:
            if (currentIndex + 1) == len(self.players):
                return 0
            else:
                return currentIndex + 1
        else:
            if currentIndex == 0:
                return len(self.players) - 1
            else:
                return currentIndex - 1

    def nextTurn(self):
        self.cardPointer = 0
        turnType = self.players[self.turn].type
        turnComplete = False
        wild = False
        reverse = False
        self.ui.importHand(self.players[self.turn].hand.getUIData(), self.players[self.turn].name, False, False)
        self.ui.setCardPointer(self.cardPointer)
        self.ui.emphasizePlayer(self.turn)

        while not turnComplete:

            player = self.players[self.turn]

            if turnType == 'human':
                if self.errorTime is None:
                    if len(self.deck) > 0:
                        self.ui.console('Select a card, (D)raw, or (P)ause.')
                    else:
                        self.ui.console('Select a card, (P)ause, or Pas(s).')
                    if player.forceDraw > 0:
                        self.ui.error('Draw Card Played! Draw {} cards.'.format(player.forceDraw))
                else:
                    if time.time() - self.errorTime <= 1:
                        self.ui.error(self.errorMessage)
                    else:
                        self.errorMessage = ''
                        self.errorTime = None

                playerInput = self.ui.getInput()
                if playerInput in Match.HAND_INPUT:
                    if playerInput == curses.KEY_LEFT:
                        if self.cardPointer > 0:
                            self.cardPointer -= 1
                            self.ui.setCardPointer(self.cardPointer)
                    elif playerInput == curses.KEY_RIGHT:
                        if self.cardPointer + 1 < len(player.hand):
                            self.cardPointer += 1
                            self.ui.setCardPointer(self.cardPointer)
                    elif playerInput == ord('d'):
                        if len(self.deck) > 0:
                            card = self.deck.drawCard()
                            self.ui.importDeck(self.deck)
                            player.addCard(card)
                            self.ui.importHand(player.hand.getUIData(), player.name, False, True)
                            self.ui.updateCardCount(self.turn, len(player.hand), True)
                            self.cardPointer = len(player.hand) - 1
                            self.ui.setCardPointer(self.cardPointer)
                        else:
                            self.errorMessage = "Deck is Empty!"
                            self.errorTime = time.time()
                            curses.beep()

                elif playerInput in Match.TURN_INPUT:
                    if playerInput == ord(' '):
                        cardCheck = player.checkCard(self.cardPointer)
                        if cardCheck.value in Match.WILD_CARDS:
                            self.removeCard(player)
                            wild = True
                            turnComplete = True
                        elif cardCheck.color == self.currentColor or cardCheck.value == self.currentValue:
                            if cardCheck.value == 'R':
                                reverse = True
                            self.removeCard(player)
                            turnComplete = True
                        else:
                            self.errorMessage = "Card Does Not Match Color {} or Value {}!".format(self.currentColor.title(), self.currentValue.title())
                            self.errorTime = time.time()
                            curses.beep()

                if reverse:
                    self.eventReverse()
                    self.reverse = not self.reverse
                if wild:
                    self.ui.error("Wild Card! Pick a New Color: (B)lue, (R)ed, (G)reen, or (Y)ellow")
                    playerInput = self.ui.getInput()
                    while playerInput not in Match.WILD_INPUT:
                        playerInput = self.ui.getInput()
                    newColor = Match.COLOR_ABBREVIATIONS[playerInput]
                    self.ui.changeTopCardColor(newColor)
                    self.currentColor = newColor
                    self.eventWild()

            elif turnType == 'computer':
                self.cardPointer = -1



        self.ui.understatePlayer(self.turn)
        self.turn = self.getNextTurn()


    def setupInterface(self):
        for i, player in enumerate(self.players):
            self.ui.importPlayer(i, player.name)
        self.ui.hidePile()
        self.ui.hideCards()
        self.ui.importDeck(self.deck)

    def play(self):
        self.setupInterface()
        self.eventBegin()
        while not self.complete:
            self.nextTurn()
        return self.players