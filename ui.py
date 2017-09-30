import curses
import curses.panel
import time
import random

class UnoInterface():

    TILE_FORMAT = 'p{}Tile'
    CARD_FORMAT = 'card{}'
    HAND_FORMAT = "{}'s Hand"
    STAGE_FORMAT = "player{}Stage"
    COLORS = ('blue','red','green','yellow')
    VALUES = ('0','1','2','3','4','5','6','7','8','9','R','X','+2','+4','W')
    IGNORE_INPUT = (127, 260, 259, 261, 258)

    MATCH_DIRECTORY = ('main', 'hand', 'backCard', 'frontCard', 'unoTitle', 'console', 'deckMeter', 'deckCount', 'p0Tile',
                      'p1Tile', 'p2Tile', 'p3Tile', 'card0', 'card1', 'card2', 'card3', 'card4', 'card5',
                      'card6', 'card7', 'card8', 'card9', 'card10', 'card11', 'card12', 'card13', 'cardLeft',
                      'cardRight')

    MAIN_DIRECTORY = ('main', 'mainMenu', 'unoTitle', 'playerStaging', 'player0Stage', 'player1Stage', 'player2Stage', 'player3Stage',
                      'beginButton', 'addPlayerButton', 'addComputerButton', 'removePlayerButton', 'settingsButton',
                      'highscoresTable', 'console')

    MAIN_BUTTONS = ('beginButton', 'addPlayerButton', 'addComputerButton', 'removePlayerButton', 'settingsButton')

    BIG_NUMBERS = {'0': ["  .d8888b.  ", " d88P  Y88b ", " 888    888 ", " 888    888 ", " 888    888 ", " 888    888 ",
                         " Y88b  d88P ", '  "Y8888P"  '],
                   '1': ['   .d888    ', '  d88888    ', '    8888    ', '    8888    ', '    8888    ', '    8888    ',
                         '    8888    ', '  88888888  '],
                   '2': ['  .d8888b.  ', ' d88P  Y88b ', '        888 ', '      .d88P ', '  .od888P"  ', ' d88P"      ',
                         ' 888"       ', ' 8888888888 '],
                   '3': ['  .d8888b.  ', ' d88P  Y88b ', '      .d88P ', '     8888"  ', '      "Y8b. ', ' 888    888 ',
                         ' Y88b  d88P ', '  "Y8888P"  '],
                   '4': ['     d8888  ', '    d8P888  ', '   d8P 888  ', '  d8P  888  ', ' d88   888  ', ' 8888888888 ',
                         '       888  ', '       888  '],
                   '5': [' 8888888888 ', ' 888        ', ' 888        ', ' 8888888b.  ', '      "Y88b ', '        888 ',
                         ' Y88b  d88P ', '  "Y8888P"  '],
                   '6': ['  .d8888b.  ', ' d88P  Y88b ', ' 888        ', ' 888d888b.  ', ' 888P "Y88b ', ' 888    888 ',
                         ' Y88b  d88P ', '  "Y8888P"  '],
                   '7': [' 8888888888 ', '       d88P ', '      d88P  ', '     d88P   ', '  88888888  ', '   d88P     ',
                         '  d88P      ', ' d88P       '],
                   '8': ['  .d8888b.  ', ' d88P  Y88b ', ' Y88b. d88P ', '  "Y88888"  ', ' .d8P""Y8b. ', ' 888    888 ',
                         ' Y88b  d88P ', '  "Y8888P"  '],
                   '9': ['  .d8888b.  ', ' d88P  Y88b ', ' 888    888 ', ' Y88b. d888 ', '  "Y888P888 ', '        888 ',
                         ' Y88b  d88P ', '  "Y8888P"  '],
                   'X': [' Y8b    d8P ', '  Y8b  d8P  ', '   Y8888P   ', '    Y88P    ', '    d88b    ', '   d8888b   ',
                         '  d8P  Y8b  ', ' d8P    Y8b '],
                   'R': ['   Y88b     ', '    Y88b    ', '     Y88b   ', '      Y88b  ', '      d88P  ', '     d88P   ',
                         '    d88P    ', '   d88P     '],
                   'W': [' 88      88 ', ' 88      88 ', ' 88  db  88 ', ' 88 d88b 88 ', ' 88d8888b88 ', ' 88P    Y88 ',
                         ' 8P      Y8 ', ' P        Y ']
                   }

    WINDOW_TYPES = {
        'frontCard': {'border': 'box', 'color': 'white', 'h': 12, 'l': 14, 'y': 10, 'x': 29},
        'backCard': {'border': 'box', 'color': 'white', 'h': 12, 'l': 14, 'y': 8, 'x': 27},
        'unoTitle': {'border': None, 'color': 'white', 'h': 3, 'l': 68, 'y': 1, 'x': 1},
        'console': {'border' : 'border', 'color': 'white', 'h': 3, 'l': 70, 'y': 4, 'x': 0},
        'controls': {'border': None, 'color': 'white', 'h': 1, 'l': 70, 'y': 32, 'x': 0},
        'hand': {'border': 'border', 'color': 'white', 'h': 9, 'l': 70, 'y': 23, 'x': 0},
        'deckMeter': {'border': 'box', 'color': 'white', 'h': 11, 'l': 5, 'y': 11, 'x': 2},
        'deckCount': {'border': None, 'color': 'white', 'h': 2, 'l': 9, 'y': 8, 'x': 1},
        'p0Tile': {'border': 'box', 'color': 'blue', 'h': 4, 'l': 14, 'y': 7, 'x': 55},
        'p1Tile': {'border': 'box', 'color': 'red', 'h': 4, 'l': 14, 'y': 11, 'x': 55},
        'p2Tile': {'border': 'box', 'color': 'green', 'h': 4, 'l': 14, 'y': 15, 'x': 55},
        'p3Tile': {'border': 'box', 'color': 'yellow', 'h': 4, 'l': 14, 'y': 19, 'x': 55},
        'card0': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 7},
        'card1': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 11},
        'card2': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 15},
        'card3': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 19},
        'card4': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 23},
        'card5': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 27},
        'card6': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 31},
        'card7': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 35},
        'card8': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 39},
        'card9': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 43},
        'card10': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 47},
        'card11': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 51},
        'card12': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 55},
        'card13': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 59},
        'cardLeft': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 2},
        'cardRight': {'border': 'box', 'color': 'white', 'h': 4, 'l': 4, 'y': 27, 'x': 64},
        'mainMenu' : {'border' : 'box', 'color': 'white', 'h': 28, 'l': 70, 'y': 4, 'x': 0},
        'playerStaging': {'border': 'border', 'color': 'white', 'h': 10, 'l': 70, 'y': 6, 'x': 0},
        'player0Stage': {'border': 'box', 'color': 'gray', 'h': 4, 'l': 34, 'y': 7, 'x': 1},
        'player1Stage': {'border': 'box', 'color': 'gray', 'h': 4, 'l': 34, 'y': 7, 'x': 35},
        'player2Stage': {'border': 'box', 'color': 'gray', 'h': 4, 'l': 34, 'y': 11, 'x': 1},
        'player3Stage': {'border': 'box', 'color': 'gray', 'h': 4, 'l': 34, 'y': 11, 'x': 35},
        'beginButton': {'border': 'box', 'color': 'gray', 'h': 3, 'l': 34, 'y': 16, 'x': 1},
        'addPlayerButton': {'border': 'box', 'color': 'white', 'h': 3, 'l': 34, 'y': 19, 'x': 1},
        'addComputerButton': {'border': 'box', 'color': 'white', 'h': 3, 'l': 34, 'y': 22, 'x': 1},
        'removePlayerButton': {'border': 'box', 'color': 'gray', 'h': 3, 'l': 34, 'y': 25, 'x': 1},
        'settingsButton': {'border': 'box', 'color': 'white', 'h': 3, 'l': 34, 'y': 28, 'x': 1},
        'highscoresTable': {'border': 'box', 'color': 'white', 'h': 15, 'l': 34, 'y': 16, 'x': 35},
    }

    def __init__(self, screen):
        self.windows = {
            'main':{'window': screen, 'panel': None, 'location': None},
            'frontCard':{'window': None, 'panel': None, 'location': None},
            'backCard': {'window': None, 'panel': None, 'location': None},
            'unoTitle': {'window': None, 'panel': None, 'location': None},
            'console': {'window': None, 'panel': None, 'location': None},
            'deckMeter': {'window': None, 'panel': None, 'location': None},
            'deckCount': {'window': None, 'panel': None, 'location': None},
            'hand': {'window': None, 'panel': None, 'location': None},
            'p0Tile': {'window': None, 'panel': None, 'location': None},
            'p1Tile': {'window': None, 'panel': None, 'location': None},
            'p2Tile': {'window': None, 'panel': None, 'location': None},
            'p3Tile': {'window': None, 'panel': None, 'location': None},
            'card0': {'window': None, 'panel': None, 'location': None},
            'card1': {'window': None, 'panel': None, 'location': None},
            'card2': {'window': None, 'panel': None, 'location': None},
            'card3': {'window': None, 'panel': None, 'location': None},
            'card4': {'window': None, 'panel': None, 'location': None},
            'card5': {'window': None, 'panel': None, 'location': None},
            'card6': {'window': None, 'panel': None, 'location': None},
            'card7': {'window': None, 'panel': None, 'location': None},
            'card8': {'window': None, 'panel': None, 'location': None},
            'card9': {'window': None, 'panel': None, 'location': None},
            'card10': {'window': None, 'panel': None, 'location': None},
            'card11': {'window': None, 'panel': None, 'location': None},
            'card12': {'window': None, 'panel': None, 'location': None},
            'card13': {'window': None, 'panel': None, 'location': None},
            'cardRight': {'window': None, 'panel': None, 'location': None},
            'cardLeft': {'window': None, 'panel': None, 'location': None},
            'controls': {'window': None, 'panel': None, 'location': None},
            'mainMenu': {'window': None, 'panel': None, 'location': None},
            'playerStaging': {'window': None, 'panel': None, 'location': None},
            'player0Stage' : {'window': None, 'panel': None, 'location': None},
            'player1Stage': {'window': None, 'panel': None, 'location': None},
            'player2Stage': {'window': None, 'panel': None, 'location': None},
            'player3Stage': {'window': None, 'panel': None, 'location': None},
            'beginButton' : {'window': None, 'panel': None, 'location': None},
            'addPlayerButton': {'window': None, 'panel': None, 'location': None},
            'addComputerButton': {'window': None, 'panel': None, 'location': None},
            'removePlayerButton': {'window': None, 'panel': None, 'location': None},
            'settingsButton': {'window': None, 'panel': None, 'location': None},
            'highscoresTable': {'window': None, 'panel': None, 'location': None}
            }

        self.TEXT_COLORS = {
            'white': curses.color_pair(1),
            'blue': curses.color_pair(2),
            'red': curses.color_pair(3),
            'green': curses.color_pair(4),
            'yellow': curses.color_pair(5),
            'invert': curses.color_pair(6),
            'gray': curses.color_pair(11),
        }

        self.BACK_COLORS = {
            'blue' : curses.color_pair(7),
            'red' : curses.color_pair(8),
            'green' : curses.color_pair(9),
            'yellow' : curses.color_pair(10),
        }

        self.cardPointer = -1
        self.playerPointer = -1
        self.stagePointer = -1
        self.hand = []
        self.playerNames = []
        self.topCard = []
        self.bottomCard = ()
        self.handName = ''

        # Initialize Curses
        curses.curs_set(0)
        curses.init_pair(1, 15, curses.COLOR_BLACK)
        curses.init_pair(2, 39, curses.COLOR_BLACK)
        curses.init_pair(3, 199, curses.COLOR_BLACK)
        curses.init_pair(4, 82, curses.COLOR_BLACK)
        curses.init_pair(5, 226, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, 15)
        curses.init_pair(7, 39, 17)
        curses.init_pair(8, 199, 52)
        curses.init_pair(9, 82, 22)
        curses.init_pair(10, 226, 58)
        curses.init_pair(11, 8, curses.COLOR_BLACK)

        self.windows['main']['window'].attrset(self.TEXT_COLORS["white"])
        self.windows['main']['window'].box()
        self.windows['main']['window'].refresh()

        # Create Windows
        self.createTypeWindow('unoTitle')
        self.createTypeWindow('backCard')
        self.createTypeWindow('frontCard')
        self.createTypeWindow('hand')
        for i in range(4):
            self.createTypeWindow('p{}Tile'.format(i))
        for i in range(14):
            self.createTypeWindow('card{}'.format(i))
        self.createTypeWindow('cardLeft')
        self.createTypeWindow('cardRight')
        self.createTypeWindow('controls')
        self.createTypeWindow('deckMeter')
        self.createTypeWindow('deckCount')
        self.createTypeWindow('mainMenu')
        self.createTypeWindow('console')
        self.createTypeWindow('playerStaging')
        for i in range(4):
            self.createTypeWindow('player{}Stage'.format(i))
        self.createTypeWindow('beginButton')
        self.createTypeWindow('addPlayerButton')
        self.createTypeWindow('addComputerButton')
        self.createTypeWindow('removePlayerButton')
        self.createTypeWindow('settingsButton')
        self.createTypeWindow('highscoresTable')

        self.setPlayerPointer(-1)
        self.setCardPointer(-1)
        self.refreshPanels()
        self.setDirectory('none')

    def createTypeWindow(self, type):
        window = curses.newwin(UnoInterface.WINDOW_TYPES[type]['h'], UnoInterface.WINDOW_TYPES[type]['l'], #height, length
                               UnoInterface.WINDOW_TYPES[type]['y'], UnoInterface.WINDOW_TYPES[type]['x']) #y, x coordinates
        if type == 'controls':
            window.bkgd(ord(' ') | curses.color_pair(6))
            window.attrset(self.TEXT_COLORS['invert'])
        else:
            window.bkgd(ord(' ') | curses.color_pair(1))
        window.attrset(self.TEXT_COLORS[UnoInterface.WINDOW_TYPES[type]['color']])
        if UnoInterface.WINDOW_TYPES[type]['border'] is not None:
            if UnoInterface.WINDOW_TYPES[type]['border'] == 'box':
                window.box()
            else:
                if type in ['console', 'playerStaging']:
                    window.border(curses.ACS_VLINE, curses.ACS_VLINE, "=", "=", curses.ACS_VLINE,
                    curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_VLINE)
                elif type == 'hand':
                    window.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LTEE,
                               curses.ACS_RTEE, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
        panel = curses.panel.new_panel(window)
        self.windows[type]['window'] = window
        if type == 'unoTitle':
            self.putText('unoTitle', 0, 25, "|| ||", 'blue')
            self.putText('unoTitle', 0, 31, "||\\ ||", 'green')
            self.putText('unoTitle', 0, 39, "// \\\\", 'red')
            self.putText('unoTitle', 1, 25, "|| ||", 'blue')
            self.putText('unoTitle', 1, 31, "||\\\\||", 'green')
            self.putText('unoTitle', 1, 38, "((   ))", 'red')
            self.putText('unoTitle', 2, 25, "\\\\ //", 'blue')
            self.putText('unoTitle', 2, 31, "|| \\||", 'green')
            self.putText('unoTitle', 2, 39, "\\\\ //", 'red')
        elif type == 'hand':
            self.putText('hand', 2, 1, '--------------------------------------------------------------------', 'white')
        elif type == 'highscoresTable':
            self.putText('highscoresTable', 1, 11, 'High Scores', 'white')
            self.putText('highscoresTable', 2, 1, '--------------------------------', 'white')
        elif type == 'cardRight':
            self.putText('cardRight', 1, 1, "->", 'white')
            self.putText('cardRight', 2, 1, "->", 'white')
        elif type == 'cardLeft':
            self.putText('cardLeft', 1, 1, "<-", 'white')
            self.putText('cardLeft', 2, 1, "<-", 'white')
        elif type == 'deckCount':
            self.putText('deckCount', 0, 0, "Deck:", 'white')
            self.putText('deckCount', 1, 0, "0 Cards", 'white')
        elif type == 'beginButton':
            self.putText('beginButton', 1, 11, "Begin Match", 'gray')
        elif type == 'addPlayerButton':
            self.putText('addPlayerButton', 1, 12, "Add Player", 'white')
        elif type == 'addComputerButton':
            self.putText('addComputerButton', 1, 11, "Add Computer", 'white')
        elif type == 'removePlayerButton':
            self.putText('removePlayerButton', 1, 10, "Remove Player", 'gray')
        elif type == 'settingsButton':
            self.putText('settingsButton', 1, 13, "Settings", 'white')
        elif type in ('player0Stage','player1Stage','player2Stage','player3Stage'):
            self.putText(type, 1, 1, "No Player")

        window.refresh()
        self.windows[type]['panel'] = panel
        self.windows[type]['location'] = (UnoInterface.WINDOW_TYPES[type]['y'],UnoInterface.WINDOW_TYPES[type]['x'])

    def refreshPanels(self):
        curses.panel.update_panels();
        self.windows['main']['window'].refresh()

    def putText(self, windowName, y, x, text, color=None):
        if color:
            try:
                self.windows[windowName]['window'].addstr(y, x, text, self.TEXT_COLORS[color])
            except:
                pass
        else:
            try:
                self.windows[windowName]['window'].addstr(y, x, text)
            except:
                pass
        self.windows[windowName]['window'].refresh()

    def console(self, text):
        self.windows['console']['window'].addstr(1,1,'                                                                    ')
        try:
            self.windows['console']['window'].addstr(1, 1, text, self.TEXT_COLORS['yellow'])
        except:
            pass
        self.windows['console']['window'].refresh()

    def error(self, text):
        self.windows['console']['window'].addstr(1,1,'                                                                    ')
        try:
            self.windows['console']['window'].addstr(1, 1, text, self.TEXT_COLORS['red'])
        except:
            pass
        self.windows['console']['window'].refresh()

    def controls(self, text):
        self.windows['controls']['window'].erase()
        try:
            self.windows['controls']['window'].addstr(0, 0, text, self.TEXT_COLORS['invert'])
        except:
            pass
        self.windows['controls']['window'].refresh()

    def drawHand(self):
        for i in range(14):
            windowName = UnoInterface.CARD_FORMAT.format(i)
            self.windows[windowName]['panel'].hide()
        for i in range(len(self.hand)):
            windowName = UnoInterface.CARD_FORMAT.format(i)
            window = self.windows[windowName]['window']
            color = self.hand[i][0]
            value = self.hand[i][1]
            window.attrset(self.TEXT_COLORS[color])
            if value not in ('+2','+4'):
                self.putText(windowName, 1, 2, value, color)
                self.putText(windowName, 2, 1, value, color)
            else:
                self.putText(windowName, 1, 1, value, color)
                self.putText(windowName, 2, 1, value, color)
            self.windows[windowName]['panel'].show()
            curses.panel.update_panels()
            window.box()
            window.noutrefresh()
        handName = UnoInterface.HAND_FORMAT.format(self.handName)
        self.windows['hand']['window'].addstr(1, 1, '                          ')
        self.windows['hand']['window'].addstr(1,1,handName)
        self.windows['hand']['window'].noutrefresh()
        curses.doupdate()


    def drawCard(self, bottom=False):
        if bottom and self.bottomCard != ():
            color = self.bottomCard[0]
            value = self.bottomCard[1]
            window = self.windows['backCard']['window']
            self.windows['frontCard']['window'].erase()
            self.windows['frontCard']['window'].noutrefresh()
        else:
            color = self.topCard[0]
            value = self.topCard[1]
            window = self.windows['frontCard']['window']
        window.resize(12, 14)
        window.erase()
        window.bkgd(ord(' ') | self.TEXT_COLORS[color])
        window.attrset(self.TEXT_COLORS[color])
        window.box()
        for i, num in enumerate(UnoInterface.BIG_NUMBERS[value]):
            window.addstr(2 + i, 1, num, self.TEXT_COLORS[color])
        window.noutrefresh()

    def importCard(self, card, draw=True):
        self.bottomCard = tuple(self.topCard)
        self.topCard = list(card)
        self.drawCard(True)
        if draw:
            self.drawCard()
        curses.doupdate()

    def importCardToHand(self, card):
        windowName = UnoInterface.CARD_FORMAT.format(len(self.hand))
        window = self.windows[windowName]['window']
        self.hand.append(card)
        color = card[0]
        value = card[1]
        window.attrset(self.TEXT_COLORS[color])
        if value not in ('+2', '+4'):
            self.putText(windowName, 1, 2, value, color)
            self.putText(windowName, 2, 1, value, color)
        else:
            self.putText(windowName, 1, 1, value, color)
            self.putText(windowName, 2, 1, value, color)
        self.windows[windowName]['panel'].show()
        curses.panel.update_panels()
        window.box()
        window.refresh()

    def expandTopCard(self, amount):
        window = self.windows['frontCard']['window']
        if amount == 11:
            self.drawCard()
            curses.doupdate()
        else:
            window.erase()
            window.resize(2+amount, 4+amount)
            window.bkgd(ord(' ') | self.TEXT_COLORS[self.topCard[0]])
            window.attrset(self.TEXT_COLORS[self.topCard[0]])
            window.box()
            window.refresh()
            time.sleep(.06)

    def changeTopCardColor(self, color):
        self.topCard[0] = color
        value = self.topCard[1]
        window = self.windows['frontCard']['window']
        window.attrset(self.TEXT_COLORS[color])
        window.box()
        for i, num in enumerate(UnoInterface.BIG_NUMBERS[value]):
            window.addstr(2 + i, 1, num)
        window.refresh()

    def wildColor(self, seed):
        seed += 1
        if seed == 1:
            self.console("Wild Card! Changing Color...")
        elif seed == 17:
            self.console("")
        window = self.windows['frontCard']['window']
        if seed in (16, 12, 8, 4):
            window.attrset(self.TEXT_COLORS['red'])
        elif seed in (15, 11, 7, 3):
            window.attrset(self.TEXT_COLORS['yellow'])
        elif seed in (14, 10, 6, 2):
            window.attrset(self.TEXT_COLORS['green'])
        elif seed in (13, 9, 5, 1):
            window.attrset(self.TEXT_COLORS['blue'])
        else:
            window.attrset(self.TEXT_COLORS[self.topCard[0]])
        for i, num in enumerate(UnoInterface.BIG_NUMBERS[self.topCard[1]]):
            window.addstr(2 + i, 1, num)
        window.box()
        window.refresh()
        time.sleep(.07)

    def elevateCard(self, cardNum):
        cardName = UnoInterface.CARD_FORMAT.format(cardNum)
        window = self.windows[cardName]['window']
        newLocation = (self.windows[cardName]['location'][0]-1,self.windows[cardName]['location'][1])
        self.windows[cardName]['panel'].move(newLocation[0],newLocation[1])
        self.windows[cardName]['location'] = newLocation
        window.attrset(self.TEXT_COLORS['white'])
        window.box()
        window.noutrefresh()
        self.refreshPanels()

    def lowerCard(self, cardNum):
        cardName = UnoInterface.CARD_FORMAT.format(cardNum)
        window = self.windows[cardName]['window']
        newLocation = (self.windows[cardName]['location'][0]+1,self.windows[cardName]['location'][1])
        self.windows[cardName]['panel'].move(newLocation[0],newLocation[1])
        self.windows[cardName]['location'] = newLocation
        window.attrset(self.TEXT_COLORS[self.hand[cardNum][0]])
        window.box()
        window.noutrefresh()
        self.refreshPanels()

    def emphasizePlayer(self, num):
        playerName = UnoInterface.TILE_FORMAT.format(num)
        window = self.windows[playerName]['window']
        if num == 0:
            color = self.BACK_COLORS['blue']
            frontColor = self.TEXT_COLORS['blue']
        elif num == 1:
            color = self.BACK_COLORS['red']
            frontColor = self.TEXT_COLORS['red']
        elif num == 2:
            color = self.BACK_COLORS['green']
            frontColor = self.TEXT_COLORS['green']
        elif num == 3:
            color = self.BACK_COLORS['yellow']
            frontColor = self.TEXT_COLORS['yellow']
        window.bkgd(ord(' ') | color)
        window.attrset(frontColor)
        window.box()
        window.refresh()
        self.windows[playerName]['window'] = window

    def understatePlayer(self, num):
        playerName = UnoInterface.TILE_FORMAT.format(num)
        window = self.windows[playerName]['window']
        if num == 0:
            color = self.TEXT_COLORS['blue']
        elif num == 1:
            color = self.TEXT_COLORS['red']
        elif num == 2:
            color = self.TEXT_COLORS['green']
        elif num == 3:
            color = self.TEXT_COLORS['yellow']
        window.bkgd(ord(' ') | color)
        window.attrset(color)
        window.refresh()
        self.windows[playerName]['window'] = window

    def setCardPointer(self, num):
        if self.cardPointer != -1:
            self.lowerCard(self.cardPointer)
        self.cardPointer = num
        if num >= 0:
            self.elevateCard(num)

    def moveCardPointer(self, num):
        if 0 <= self.cardPointer + num < len(self.hand):
            current = int(self.cardPointer)
            self.lowerCard(current)
            self.cardPointer += num
            self.elevateCard(self.cardPointer)
            curses.doupdate()

    def setPlayerPointer(self, num):
        if self.playerPointer != -1:
            self.understatePlayer(self.playerPointer)
        self.playerPointer = num
        if num >= 0:
            self.emphasizePlayer(num)

    def movePlayerPointer(self, num):
        if 0 <= self.playerPointer + num < 4:
            current = int(self.playerPointer)
            self.understatePlayer(current)
            self.playerPointer += num
            self.emphasizePlayer(self.playerPointer)
            curses.doupdate()

    def importHand(self, hand, owner, offset=0):
        self.setCardPointer(0)
        self.hand = hand
        self.handName = owner
        self.drawHand()
        self.setCardPointer(0)

    def setDirectory(self, directory):
        for window in self.windows:
            if window != 'main':
                self.windows[window]['panel'].hide()
        if directory == 'match':
            for window in self.MATCH_DIRECTORY:
                if window != 'main':
                    self.windows[window]['panel'].show()
            self.putText('controls', 0, 0, 'Controls: (P)ause, Pas(s), (D)raw, Space Bar - Select Card', 'invert')
        elif directory == 'main':
            for window in self.MAIN_DIRECTORY:
                if window != 'main':
                    self.windows[window]['panel'].show()
        self.refreshPanels()

    def updateMainButtons(self, numPlayers, pointer):

        for button in UnoInterface.MAIN_BUTTONS:
            if button in ('beginButton', 'removePlayerButton'):
                self.windows[button]['window'].attrset(self.TEXT_COLORS['gray'])
            else:
                self.windows[button]['window'].attrset(self.TEXT_COLORS['white'])

        if numPlayers > 0:
            self.windows['removePlayerButton']['window'].attrset(self.TEXT_COLORS['white'])
        if numPlayers > 1:
            self.windows['beginButton']['window'].attrset(self.TEXT_COLORS['blue'])
            self.windows['removePlayerButton']['window'].attrset(self.TEXT_COLORS['white'])
        if numPlayers > 3:
            self.windows['addPlayerButton']['window'].attrset(self.TEXT_COLORS['gray'])
            self.windows['addComputerButton']['window'].attrset(self.TEXT_COLORS['gray'])
        self.windows[UnoInterface.MAIN_BUTTONS[pointer]]['window'].attrset(self.TEXT_COLORS['yellow'])
        self.putText('beginButton', 1, 11, "Begin Match")
        self.windows['beginButton']['window'].box()
        self.windows['beginButton']['window'].noutrefresh()
        self.putText('addPlayerButton', 1, 12, "Add Player")
        self.windows['addPlayerButton']['window'].box()
        self.windows['addPlayerButton']['window'].noutrefresh()
        self.putText('addComputerButton', 1, 11, "Add Computer")
        self.windows['addComputerButton']['window'].box()
        self.windows['addComputerButton']['window'].noutrefresh()
        self.putText('removePlayerButton', 1, 10, "Remove Player")
        self.windows['removePlayerButton']['window'].box()
        self.windows['removePlayerButton']['window'].noutrefresh()
        self.putText('settingsButton', 1, 13, "Settings")
        self.windows['settingsButton']['window'].box()
        self.windows['settingsButton']['window'].noutrefresh()
        curses.doupdate()

    def updateStage(self, num, playerName, points):
        windowName = UnoInterface.STAGE_FORMAT.format(num)
        window = self.windows[windowName]['window']
        window.erase()
        window.attrset(self.TEXT_COLORS[UnoInterface.COLORS[num]])
        window.box()
        self.putText(windowName, 1, 1, playerName)
        self.putText(windowName, 2, 1, "Points: {}".format(points))
        window.refresh()

    def readyStage(self, num):
        windowName = UnoInterface.STAGE_FORMAT.format(num)
        window = self.windows[windowName]['window']
        window.erase()
        window.attrset(self.TEXT_COLORS[UnoInterface.COLORS[num]])
        window.addstr(1,1,'            ')
        window.box()
        window.move(1,1)
        curses.curs_set(1)
        window.refresh()

    def clearStage(self, num):
        windowName = UnoInterface.STAGE_FORMAT.format(num)
        window = self.windows[windowName]['window']
        window.erase()
        window.attrset(self.TEXT_COLORS['gray'])
        window.box()
        self.putText(windowName, 1, 1, 'No Player')
        window.refresh()

    def getPlayerName(self, num):
        windowName = UnoInterface.STAGE_FORMAT.format(num)
        window = self.windows[windowName]['window']
        self.readyStage(num)
        name = []
        c = self.getInput()
        while chr(c) != '\n':
            if c not in UnoInterface.IGNORE_INPUT and len(name) < 12:
                name.append(chr(c))
            elif c == 127 and len(name) > 0:
                name.pop()
            for i, character in enumerate(name):
                window.addstr(1, 1 + i, character)
            window.move(1, len(name)+1)
            window.refresh()
            c = self.getInput()
            window.addstr(1, 1, '            ')
        curses.curs_set(0)
        if name == []:
            self.clearStage(num)
            return False, ''
        return True, ''.join(name)

    def colorWindow(self, name, color):
        self.windows[name]['window'].bkgd(0, self.TEXT_COLORS[color])
        self.windows[name]['window'].refresh()

    def emphasizePlayer(self, num):
        playerName = UnoInterface.TILE_FORMAT.format(num)
        window = self.windows[playerName]['window']
        if num == 0:
            color = self.BACK_COLORS['blue']
            frontColor = self.TEXT_COLORS['blue']
        elif num == 1:
            color = self.BACK_COLORS['red']
            frontColor = self.TEXT_COLORS['red']
        elif num == 2:
            color = self.BACK_COLORS['green']
            frontColor = self.TEXT_COLORS['green']
        elif num == 3:
            color = self.BACK_COLORS['yellow']
            frontColor = self.TEXT_COLORS['yellow']
        window.bkgd(ord(' ') | color)
        window.attrset(frontColor)
        window.box()
        window.refresh()
        self.windows[playerName]['window'] = window

    def understatePlayer(self, num):
        playerName = UnoInterface.TILE_FORMAT.format(num)
        window = self.windows[playerName]['window']
        if num == 0:
            color = self.TEXT_COLORS['blue']
        elif num == 1:
            color = self.TEXT_COLORS['red']
        elif num == 2:
            color = self.TEXT_COLORS['green']
        elif num == 3:
            color = self.TEXT_COLORS['yellow']
        window.bkgd(ord(' ') | color)
        window.attrset(color)
        window.refresh()
        self.windows[playerName]['window'] = window

    def setStagePointer(self, num):
        if self.stagePointer != -1:
            self.colorWindow(UnoInterface.STAGE_FORMAT.format(self.stagePointer), self.COLORS[self.stagePointer])
        self.stagePointer = num
        if num >= 0:
            self.colorWindow(UnoInterface.STAGE_FORMAT.format(num), 'white')

    def getInput(self):
        curses.flushinp()
        k = self.windows['main']['window'].getch()
        return k