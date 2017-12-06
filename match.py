from uno_objs import Card, Deck, Hand
import curses
import time
import random

class Match():

    TURN_INPUT = (ord(' '),ord('p'))
    HAND_INPUT = (curses.KEY_LEFT, curses.KEY_RIGHT, ord('d'), ord('f'), ord('q'))
    INITIAL_CARD_COUNT = 7
    WILD_CARDS = ('+4', 'W')
    WILD_INPUT = (ord('b'),ord('g'),ord('y'),ord('r'))
    COLOR_ABBREVIATIONS = {
        ord('b'):'blue',
        ord('r'):'red',
        ord('g'):'green',
        ord('y'):'yellow'
    }
    SPEEDS = {
        'Slow' : 2,
        'Normal' : 1,
        'Fast' : 0
    }

    def __init__(self, players, ui, settings):
        self.players = players
        self.ui = ui

        self.complete = False
        self.abort = False

        self.playerControlled = []
        self.computerControlled = []

        self.deck = Deck(True)
        self.pile = Deck(False)

        self.displayEffects = settings['effects']
        self.computerSpeed = Match.SPEEDS[settings['speed']]
        self.hideComputerHands = settings['hideHands']

        self.errorMessage = ''
        self.errorTime = None

        self.turn = None
        self.winner = None
        self.cardPointer = -1
        self.currentHand = None
        self.turnComplete = False
        self.reverse = False
        self.currentColor = None
        self.currentValue = None
        self.viewingTop = True

        self.forceDraw = 0
        self.consecutivePasses = 0
        self.maxPasses = len(self.players)

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
        #card = Card('blue','X')
        self.pile.addCard(card)
        self.ui.importCard(self.pile[0].getUIData(), False, self.reverse)
        for i in range(12):
            self.ui.expandTopCard(i,self.reverse)
        self.currentColor = card.color
        self.currentValue = card.value

        if self.currentValue in Match.WILD_CARDS:
            self.ui.importHand(self.players[self.turn].hand.getUIData(), self.players[self.turn].name, False, False)
            self.ui.emphasizePlayer(self.turn)
            self.eventWild()
        elif self.currentValue == 'X' or (self.currentValue == 'R' and len(self.players) == 2):
            self.eventSkip(True)
            self.turn = self.getNextTurn()
        elif self.currentValue == 'R':
            self.eventReverse()

    def eventEnd(self):
        if not self.abort:
            name = self.players[self.winner].name
            self.ui.console('{} Wins!'.format(name))
            for j in range(1):
                for i in range(17):
                    self.ui.wildColor(i, self.winner, name)
                    time.sleep(.1)

            self.ui.emphasizePlayer(self.winner)
            self.ui.console('Press Enter to Begin Point Tally'.format(name))
            self.ui.getInput()
            points = 0
            for i, player in enumerate(self.players):
                if i != self.winner:
                    while len(player.hand) > 0:
                        self.ui.console('{} Won {} Points!'.format(name, points))
                        self.ui.updateCardCount(i, len(player.hand))
                        self.ui.importHand(player.hand.getUIData(), player.name, False, True)
                        card = player.removeCard(0)
                        points += card.points
                        time.sleep(.1)
                    self.ui.updateCardCount(i, len(player.hand))
                    self.ui.importHand(player.hand.getUIData(), player.name, False, True)
                    self.ui.console('{} Won {} Points!'.format(name, points))
                    time.sleep(.1)

            self.ui.console('{} Won {} Points! Press Enter'.format(name, points))
            self.players[self.winner].addPoints(points)
            self.ui.getInput()


        for player in self.players:
            player.discardHand()

        return self.players


    def eventReverse(self):
        self.ui.error('Reverse Card Played! Reversing Turn Order.')
        if self.displayEffects:
            time.sleep(1.5)
        for i in range(10):
            self.ui.eventReverse(i, self.reverse)
            if self.displayEffects:
                time.sleep(.07)
        self.reverse = not self.reverse

    def eventSkip(self, selfSkip):
        if not selfSkip:
            self.turn = self.getNextTurn()
        self.ui.error('Skip Card Played! Skipping {}\'s Turn.'.format(self.players[self.turn].name))
        if self.displayEffects:
            time.sleep(1.5)
        for i in range(4):
            self.ui.skipEvent(i,self.turn)
            if self.displayEffects:
                time.sleep(.3)

    def eventWild(self, color=None):
        if color is None:
            self.ui.error("Wild Card! Pick a New Color: (B)lue, (R)ed, (G)reen, or (Y)ellow")
            playerInput = self.ui.getInput()
            while playerInput not in Match.WILD_INPUT:
                playerInput = self.ui.getInput()
            newColor = Match.COLOR_ABBREVIATIONS[playerInput]
        else:
            newColor = random.choice(self.ui.COLORS)
        self.ui.changeTopCardColor(newColor)
        self.currentColor = newColor
        self.ui.error('Wild Card! Changing Color...')
        for i in range(17):
            self.ui.wildColor(i)
            if self.displayEffects:
                time.sleep(.07)

    def eventPass(self):
        self.ui.setCardPointer(-1, False)
        self.consecutivePasses += 1
        if self.consecutivePasses == self.maxPasses:
            wildColorChange = random.choice(self.ui.COLORS)
            self.eventWild(wildColorChange)
            self.consecutivePasses = 0

    def removeCard(self, player):
        card = player.removeCard(self.cardPointer)
        hide = False
        if player.type != 'human':
            hide = True
        self.ui.updateCardCount(self.turn, len(player.hand), True)
        self.ui.setCardPointer(-1)
        self.consecutivePasses = 0
        self.pile.addCard(card)
        self.ui.importCard(self.pile[len(self.pile) - 1].getUIData(), False, self.reverse)
        self.ui.importHand(self.players[self.turn].hand.getUIData(), self.players[self.turn].name,
                           hide, False)

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

    def drawCard(self, player):
        card = self.deck.drawCard()
        hide = player.type == 'computer'
        self.ui.importDeck(self.deck)
        player.addCard(card)
        self.ui.importHand(player.hand.getUIData(), player.name, hide, True)
        self.ui.updateCardCount(self.turn, len(player.hand), True)
        self.cardPointer = len(player.hand) - 1
        self.ui.setCardPointer(self.cardPointer, hide)
        if self.forceDraw > 0:
            self.forceDraw -= 1

    def nextTurn(self):
        player = self.players[self.turn]
        self.cardPointer = 0
        turnType = player.type
        cardCheck = None
        if turnType == 'human':
            self.ui.importHand(self.players[self.turn].hand.getUIData(), player.name, False, False)
            self.ui.setCardPointer(self.cardPointer)
        else:
            self.ui.importHand(self.players[self.turn].hand.getUIData(), player.name, True, False)
            self.ui.setCardPointer(-1)
        self.ui.emphasizePlayer(self.turn)
        self.viewingTop = True
        turnComplete = False
        wildColorChange = None
        legalCards = player.getAllLegalCards(self.currentColor, self.currentValue)

        if turnType == 'human':
            while not turnComplete:
                if self.errorTime is None:
                    if self.forceDraw > 0 and len(self.deck) > 0:
                        self.ui.error('Draw Card Played! Draw {} cards.'.format(self.forceDraw))
                    else:
                        if len(self.deck) > 0:
                            self.ui.console('Select a card or (D)raw.')
                        else:
                            self.forceDraw = 0
                            self.ui.console('Select a card or (P)ass.')
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
                            self.drawCard(player)
                            legalCards = player.getAllLegalCards(self.currentColor, self.currentValue)
                        else:
                            self.errorMessage = "Deck is Empty!"
                            self.errorTime = time.time()
                            curses.beep()
                    elif playerInput == ord('f') and len(self.pile) > 1:
                        self.ui.exchangePile(self.viewingTop)
                        self.viewingTop = not self.viewingTop
                    elif playerInput == ord('q'):
                        self.ui.setCardPointer(-1)
                        turnComplete = True
                        self.complete = True
                        self.abort = True
                        self.winner = 0

                elif playerInput in Match.TURN_INPUT:
                    if playerInput == ord(' ') and self.forceDraw == 0:
                        if self.cardPointer in legalCards['all']:
                            cardCheck = player.checkCard(self.cardPointer)
                            self.removeCard(player)
                            turnComplete = True
                        else:
                            if self.cardPointer in legalCards['wild']:
                                self.errorMessage = "Cannot Use +4 Cards When You Have Cards Matching the Color or Value!"
                            else:
                                self.errorMessage = "Card Does Not Match Color {} or Value {}!".format(self.currentColor.title(), self.currentValue.title())
                            self.errorTime = time.time()
                            curses.beep()
                    elif playerInput == ord('p'):
                        if len(self.deck) == 0 and len(legalCards['all']) == 0:
                            turnComplete = True
                            self.eventPass()
                        else:
                            if len(self.deck) > 0:
                                self.errorMessage = "Cannot Pass Until Deck is Empty!"
                                self.errorTime = time.time()
                                curses.beep()
                            else:
                                self.errorMessage = "Cannot Pass With Playable Cards!"
                                self.errorTime = time.time()
                                curses.beep()
                    else:
                        curses.beep()

        elif turnType == 'computer':
            self.ui.console("{}'s Turn".format(player.name))
            if self.displayEffects:
                time.sleep(self.computerSpeed)
            drewCards = False

            while not turnComplete:

                player.think(self)

                if len(self.deck) == 0 and len(legalCards['all']) == 0:
                    turnComplete = True
                    self.eventPass()

                while len(legalCards['all']) == 0 or self.forceDraw > 0:
                    drewCards = True
                    self.drawCard(player)
                    legalCards = player.getAllLegalCards(self.currentColor, self.currentValue)
                    if self.displayEffects:
                        time.sleep(.3)

                chosenCard = random.choice(legalCards['all'])

                if not drewCards:
                    self.cardPointer = 0
                    try:
                        moves = random.randrange(1,min(len(player.hand),7))
                    except ValueError:
                        moves = 1
                    for i in range(moves):
                        self.cardPointer = i
                        self.ui.setCardPointer(self.cardPointer, True)
                        if self.displayEffects:
                            time.sleep(.2)

                self.cardPointer = chosenCard
                cardCheck = player.checkCard(self.cardPointer)
                self.removeCard(player)
                turnComplete = True

        oldTurn = self.turn

        if cardCheck is not None:

            if cardCheck.value == 'R':
                if len(self.players) > 2:
                    self.eventReverse()
                else:
                    self.eventSkip(False)
            elif cardCheck.value == 'X':
                self.eventSkip(False)
            elif cardCheck.value in Match.WILD_CARDS:
                if player.type != 'human':
                    wildColorChange = random.choice(self.ui.COLORS)
                self.eventWild(wildColorChange)
                if cardCheck.value == '+4':
                    self.forceDraw = min(4, len(self.deck))
            elif cardCheck.value == '+2':
                self.forceDraw = min(2, len(self.deck))

        if len(player.hand) == 0:
            self.complete = True
            self.winner = oldTurn
        else:
            self.ui.understatePlayer(oldTurn)
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
        return self.eventEnd()