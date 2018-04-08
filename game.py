from ui import UnoInterface
from uno_players import Player, ComputerPlayer
from match import Match
import curses
import time
import random

class Game():

    COLORS = ('blue', 'red', 'green', 'yellow')
    VALUES = ('0','1','2','3','4','5','6','7','8','9','R','X','+2','+4','W')
    BUTTON_PLAYER_REQUIREMENTS = ((1,5),(-1,4),(-1,4),(0,5),(-1,5))
    COMPUTER_NAMES = ('Watson', 'SkyNet', 'Hal 9000', 'Metal Gear')
    SELECT = (ord(' '), ord('\n'))
    SETTINGS_MOVEMENTS = {
        0 : [3,1],
        1 : [0,2],
        2 : [1,3],
        3 : [2,0]
    }
    NEXT_SPEED = {
        'Slow' : 'Normal',
        'Normal' : 'Fast',
        'Fast' : 'Slow'
    }

    def __init__(self, screen):
        self.screen = screen
        self.screen.box()
        self.screen.refresh()
        self.ui = UnoInterface(screen)

        self.buttonPointer = 1
        self.stagePointer = -1
        self.settingsPointer = -1
        self.playerStaging = []
        self.players = []
        self.numPlayers = 0

        self.settings = {
            'effects' : True,
            'showHands' : False,
            'speed' : 'Normal',
            'dummy' : False
        }

    def addPlayer(self, player):
        self.playerStaging.append(player)
        self.ui.updateStage(self.numPlayers, player.name, player.points)
        self.numPlayers += 1

    def removePlayer(self, number):
        del self.playerStaging[number]
        for i in range(4):
            self.ui.clearStage(i)
        for i, player in enumerate(self.playerStaging):
            self.ui.updateStage(i, player.name, player.points)
        self.numPlayers -= 1

    def finalizePlayers(self):
        for player in self.playerStaging:
            self.players.append(player)
        for i, player in enumerate(self.players):
            self.players[i].id = i

    def canMoveToButton(self):
        return self.numPlayers < Game.BUTTON_PLAYER_REQUIREMENTS[self.buttonPointer][1] and self.numPlayers > Game.BUTTON_PLAYER_REQUIREMENTS[self.buttonPointer][0]

    def getComputerName(self):
        complete = False
        index = self.numPlayers
        while not complete:
            name = Game.COMPUTER_NAMES[index]
            complete = True
            for player in self.playerStaging:
                if player.name == name:
                    index += 1
                    if index >= len(Game.COMPUTER_NAMES):
                        index = 0
                        complete = False

        return Game.COMPUTER_NAMES[index]

    def updateSettings(self):
        if self.settingsPointer == 0:
            self.settings['effects'] = not self.settings['effects']
        if self.settingsPointer == 1:
            self.settings['speed'] = Game.NEXT_SPEED[self.settings['speed']]
        if self.settingsPointer == 2:
            self.settings['showHands'] = not self.settings['showHands']
        if self.settingsPointer == 3:
            self.settings['dummy'] = not self.settings['dummy']

    def playMatch(self):
        self.finalizePlayers()
        m = Match(self.players, self.ui, self.settings)
        self.ui.setDirectory('match')
        self.players = m.play()

        self.playerStaging = []
        for player in self.players:
            self.playerStaging.append(player)
        self.players = []
        for i, player in enumerate(self.playerStaging):
            self.ui.updateStage(i, player.name, player.points)
        self.ui.setDirectory('main')

    def start(self):
        self.ui.setDirectory('main')
        self.ui.console("Welcome to Uno! Add Players to Begin.")
        while True:
            self.ui.controls('Navigate with Arrow Keys. Select with SPACE BAR or ENTER')
            self.ui.updateMainButtons(self.numPlayers, self.buttonPointer)
            command = self.ui.getInput()
        
            if command == curses.KEY_DOWN:
                if self.buttonPointer == 4:
                    self.buttonPointer = 0
                else:
                    self.buttonPointer += 1
                while not self.canMoveToButton():
                    if self.buttonPointer == 4:
                        self.buttonPointer = 0
                    else:
                        self.buttonPointer += 1
            elif command == curses.KEY_UP:
                if self.buttonPointer == 0:
                    self.buttonPointer = 4
                else:
                    self.buttonPointer -= 1
                while not self.canMoveToButton():
                    if self.buttonPointer == 0:
                        self.buttonPointer = 4
                    else:
                        self.buttonPointer -= 1

            elif command in Game.SELECT:
                if self.buttonPointer == 0:
                    self.playMatch()
                elif self.buttonPointer == 1:
                    self.ui.controls('Press Enter to Confirm Name')
                    name = self.ui.getPlayerName(self.numPlayers)
                    if name[0]:
                        p = Player(name[1])
                        self.addPlayer(p)
                    if self.numPlayers == 4:
                        self.buttonPointer = 3
                elif self.buttonPointer == 2:
                    name = self.getComputerName()
                    p = ComputerPlayer(name)
                    self.addPlayer(p)
                    if self.numPlayers == 4:
                        self.buttonPointer = 3
                elif self.buttonPointer == 3:
                    self.stagePointer = 0
                    self.ui.setStagePointer(self.stagePointer)
                    while True:
                        command = self.ui.getInput()
                        if command == curses.KEY_DOWN:
                            if self.stagePointer + 2 < self.numPlayers:
                                self.stagePointer += 2
                                self.ui.setStagePointer(self.stagePointer)
                        elif command == curses.KEY_UP:
                            if self.stagePointer - 2 >= 0:
                                self.stagePointer -= 2
                                self.ui.setStagePointer(self.stagePointer)
                        elif command == curses.KEY_RIGHT:
                            if self.stagePointer + 1 < self.numPlayers:
                                self.stagePointer += 1
                                self.ui.setStagePointer(self.stagePointer)
                        elif command == curses.KEY_LEFT:
                            if self.stagePointer - 1 >= 0:
                                self.stagePointer -= 1
                                self.ui.setStagePointer(self.stagePointer)
                        elif command in Game.SELECT:
                            self.ui.setStagePointer(-1)
                            self.removePlayer(self.stagePointer)
                            self.stagePointer = -1
                            break
                    if self.numPlayers == 0:
                        self.buttonPointer = 1
                elif self.buttonPointer == 4:
                    self.ui.controls("Navigate with Arrow Keys. Press ENTER or ESC To Exit.")
                    self.ui.colorWindow('settingsButton','green')
                    self.settingsPointer = 0
                    self.ui.setSettingsPointer(self.settingsPointer)
                    playerInput = self.ui.getInput()
                    while playerInput != ord('\n') and playerInput != 27:
                        if playerInput == curses.KEY_DOWN:
                            self.settingsPointer = Game.SETTINGS_MOVEMENTS[self.settingsPointer][1]
                            self.ui.setSettingsPointer(self.settingsPointer)
                        elif playerInput == curses.KEY_UP:
                            self.settingsPointer = Game.SETTINGS_MOVEMENTS[self.settingsPointer][0]
                            self.ui.setSettingsPointer(self.settingsPointer)
                        elif playerInput in (ord(' '),curses.KEY_LEFT,curses.KEY_RIGHT):
                            self.updateSettings()
                            self.ui.updateSettingsBoard(self.settings)
                        playerInput = self.ui.getInput()
                    self.settingsPointer = -1
                    self.ui.setSettingsPointer(self.settingsPointer)
                    self.ui.colorWindow('settingsButton', 'yellow')

            elif command == ord('q'):
                exit()