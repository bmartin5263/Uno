# Uno
Recreation of the classic Uno card game with modified rules, text-based graphics, and computer-controlled AI players. 
Based on an Uno game I wrote during my Sophomore year at DePaul university, my goals with this project was to expand 
what I had already created by updating the user interface using the Curses module for more interesting effects.

## Getting Started
__Language Version:__ Python 3.5

__Usage:__
```
python3 main.py
```
The Uno Basic repository includes the following python modules:
* game.py
* main.py
* match.py
* ui.py
* uno_objs.py
* uno_players.py

Uno Basic does not require the download of any third-party modules and only uses standard Python library modules.

## How To Play

Uno Basic is a close recreation to the classic Uno Game and includes many of the same rules, however some rules have
been modified to add to a more competitive experience.

### Rules
* 2-4 Players.
* First turn is selected at random.
* Players place cards onto the pile that match either the color or value of the piles topmost card.
* First player to empty hand of all cards wins.
* Winning player gets points based on the values of the remaining cards in the opponents hands
* Draw Four cards may only be used when no other card can be legally placed.
* Reverse Cards act as skips during games with only two players.
* If deck is empty and player has no usuable cards, the player may pass their own turn.

<img src=https://github.com/bmartin5263/Uno/blob/master/images/image1.png width="400" height="400"> <img src=https://github.com/bmartin5263/Uno/blob/master/images/image2.png width="400" height="400">
<img src=https://github.com/bmartin5263/Uno/blob/master/images/image3.png width="400" height="400"> <img src=https://github.com/bmartin5263/Uno/blob/master/images/image4.png width="400" height="400">
<img src=https://github.com/bmartin5263/Uno/blob/master/images/image5.png width="400" height="400">
