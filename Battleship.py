import keyboard
import os
import random
import re
import sys
import pygame

#Constant

UPPER_FRAME =        "╔═══════════════════════════════════════════╗"
TITLE_TABLE1 =       "║                 Your ships                ║"
TITLE_TABLE2 =       "║                 Your shots                ║"
MIDDLE_LINES_TITLE = "╠═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╣"
CHARACTERS =         "║   ║ A ║ B ║ C ║ D ║ E ║ F ║ G ║ H ║ I ║ J ║"
MIDDLE_LINES =       "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣"
LOW_FRAME =          "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝"
VALID_LETTERS = ['A','B','C','D','E','F','G','H','I','J']
SHIPS_NAMES_HOLES = ['Destroyer (2 holes)','Submarine (3 holes)','Cruiser (3 holes)','Battleship (4 holes)','Carrier (5 holes)']
PLAYER1_BATTLESHIP_TABLE = []
PLAYER2_BATTLESHIP_TABLE = []
SHOOTS_PLAYER = []
SHIPS_PLAYER = {}
SHIPS_COMPUTER = {}
DIRECTIONS = {'W':'W', 'A':'A', 'S':'S', 'D':'D'}
LIVES_PLAYER = 5
LIVES_COMPUTER = 5
messages = []

#This class creates and prints game boards
class Boards:

    def createBoards(self):#This method fills the list of player boards in the game
        for lista in range(0,10):
            PLAYER1_BATTLESHIP_TABLE.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])
            PLAYER2_BATTLESHIP_TABLE.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])
            SHOOTS_PLAYER.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])

    def printBoards(self,tablero1, tablero2):#This method prints the game boards of the player
        global LIVES_PLAYER
        global LIVES_COMPUTER
        print(f"{UPPER_FRAME}     {UPPER_FRAME}")
        print(f"{TITLE_TABLE1}     {TITLE_TABLE2}       Your ships: {LIVES_PLAYER}      Enemy ships: {LIVES_COMPUTER}")
        print(f"{MIDDLE_LINES_TITLE}     {MIDDLE_LINES_TITLE}")
        print(f"{CHARACTERS}     {CHARACTERS}")
        print(f"{MIDDLE_LINES}     {MIDDLE_LINES}")
        rowCount = 0
        for fila1, fila2 in zip(tablero1,tablero2):
            columnCount = 0
            for caracter in fila1:
                if(columnCount>0):
                    print(" "+caracter, end=" ║")
                else:
                    if(rowCount<9):
                        print("║ "+caracter, end=" ║")
                    else:
                        print("║"+caracter, end=" ║")
                columnCount+=1
            for caracter in fila2:
                if(columnCount>11):
                    print(" "+caracter, end=" ║")
                else:
                    if(rowCount<9):
                        print("     ║ "+caracter, end=" ║")
                    else:
                        print("     ║"+caracter, end=" ║")
                columnCount+=1
            print()
            if(rowCount<9):
                print(f"{MIDDLE_LINES}     {MIDDLE_LINES}")
            else:
                print(f"{LOW_FRAME}     {LOW_FRAME}")
            rowCount+=1

#This class creates ships for the players and destroy
class Ships:

    def giveMePositionOfShips(self,player):#This method requests the position of ships
        if player == True:
            for ship in SHIPS_NAMES_HOLES:
                coordinate = playerPerson.correctCoordinateAddShip(ship)
                validationCoordinate.validationCoordinateAddShip(coordinate, player, ship)
                clearConsole()
                boards.printBoards(PLAYER1_BATTLESHIP_TABLE,PLAYER2_BATTLESHIP_TABLE)
            self.giveMePositionOfShips(False)
        else:
            for ship in SHIPS_NAMES_HOLES:
                computerPlayer.randomPosition(ship)
            play_audio(convertMusic('battle-time'))
            clearConsole()
            boards.printBoards(PLAYER1_BATTLESHIP_TABLE,PLAYER2_BATTLESHIP_TABLE)  
            playerPerson.correctCoordinateShoot()

    def createShip(self,coordinate, direction, holeNumbers, player, positionX, positionY, ship):
        #This method creates a ship on the game tables for players
        shipCoordinates = []
        lives = 0
            
        if(direction == DIRECTIONS['W']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)-index
                shipCoordinates.append([positionX, piceOfShip])
                self.addShip(player,positionX, piceOfShip)
                lives += 1
        elif(direction == DIRECTIONS['S']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                shipCoordinates.append([positionX, piceOfShip])
                self.addShip(player,positionX, piceOfShip)
                lives += 1
        elif(direction == DIRECTIONS['D']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                shipCoordinates.append([piceOfShip,positionY-1])
                self.addShip(player, piceOfShip, positionY-1)
                lives += 1
        elif(direction == DIRECTIONS['A']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                shipCoordinates.append([piceOfShip,positionY-1])
                self.addShip(player, piceOfShip, positionY-1)
                lives += 1
        if player == True:
            SHIPS_PLAYER[ship.split()[0]] = [lives, shipCoordinates]
        else:
            SHIPS_COMPUTER[ship.split()[0]] = [lives, shipCoordinates]

    def addShip(self,player, positionX, positionY):
        if player == True:
            PLAYER1_BATTLESHIP_TABLE[positionY][positionX] = 'o'
        else:
            PLAYER2_BATTLESHIP_TABLE[positionY][positionX] = 'o'

    def shotShip(self, player,coordinate):
        translatedCoordinate = validationCoordinate.translateCoordinate(coordinate)
        positionX = translatedCoordinate[0]
        positionY = translatedCoordinate[1]-1
        simbolBoard = ''
        
        if player == True:
            simbolBoard = PLAYER2_BATTLESHIP_TABLE[positionY][positionX]
        else:
            simbolBoard = PLAYER1_BATTLESHIP_TABLE[positionY][positionX]

        if  simbolBoard== 'x' or simbolBoard == 'ø':
            if player == True:
                messages.append("Seems like we've already shot at that coordinate")
                printMessage()
                playerPerson.correctCoordinateShoot()
            else:
                computerPlayer.randomShot()
        else:
            if player == True:
                self.hitShip(PLAYER2_BATTLESHIP_TABLE,player, positionX, positionY, simbolBoard)
            else:
                self.hitShip(PLAYER1_BATTLESHIP_TABLE,player, positionX, positionY, simbolBoard)

    def hitShip(self,board, player, positionX, positionY, simbolBoard):
        if simbolBoard == 'o':
            board[positionY][positionX] = 'ø'
            if player == True:
                SHOOTS_PLAYER[positionY][positionX] = 'ø'
            self.destroyShip(player, positionX, positionY)
        else:
            board[positionY][positionX] = 'x'
            if player == True:
                SHOOTS_PLAYER[positionY][positionX] = 'x'
                messages.append('We miss')
            else:
                messages.append('The enemy has missed')
                printMessage()

        if player == True:
            computerPlayer.randomShot()
        else:
            playerPerson.correctCoordinateShoot()

    def destroyShip(self, player, positionX, positionY):
        global LIVES_COMPUTER
        global LIVES_PLAYER
        global messages
        if player == True:
            for ship, valor in SHIPS_COMPUTER.items():
                for coordinateShip in valor[1]:
                    if coordinateShip[0] == positionX and coordinateShip[1] == positionY:
                        valor[0] -= 1
                        if valor[0] == 0:
                            messages.append(f'Captain! We destroyed the {ship}')
                            LIVES_COMPUTER -= 1
                        else:
                            messages.append('Captain! We hit a ship')
            if LIVES_COMPUTER == 0:
                gameOver(player)
        else:
            for ship, valor in SHIPS_PLAYER.items():
                for coordinateShip in valor[1]:
                    if coordinateShip[0] == positionX and coordinateShip[1] == positionY:
                        valor[0] -= 1
                        if valor[0] ==0:
                            messages.append(f'Captain! The enemy destroyed our "{ship}"')
                            LIVES_PLAYER -= 1
                        else:
                            messages.append('Captain! One of our ships has been hit')
            printMessage()
            if LIVES_PLAYER == 0:
                gameOver(player)

class ValidationCoordinate:

    def translateCoordinate(self, coordinate):#This method translates the player input coordinate
        positionX = None
        positionY = int(re.findall(r'\d+', coordinate)[0])
        for index, character in enumerate(VALID_LETTERS):
            if character == re.findall(r'[a-zA-Z]+', coordinate)[0].upper():
                positionX = index+1
        result = [positionX, positionY]
        return result

    def directionShip(self, player, ship):#This method takes the expansion direction of the ships
        tecla_pulsada = None
        print(f'En que direccion se extiende el barco {ship}?')
        print('W(Arriba), S(Abajo), D(Derecha), A(Izquierda)')

        if player == True:
            while True:
                evento = keyboard.read_event(suppress=True)
                tecla_pulsada = evento.name.upper()
                print(f"Presionaste la tecla: {tecla_pulsada}")
                if tecla_pulsada == 'W':
                    break
                if tecla_pulsada == 'S':
                    break
                if tecla_pulsada == 'A':
                    break
                if tecla_pulsada == 'D':
                    break
        else:
            tecla_pulsada = random.choice("WSAD")
        return tecla_pulsada

    def availablePosible(self, holeNumbers, positionX, positionY):
        #This method checks if it´s possibles to create a ship at this position, provided it´s whithin the game board
        directionPosible = []
        holeSubtraction = int(holeNumbers)-1

        if(1 <= positionY+holeSubtraction <= 10):
            directionPosible.append(True)
        else:
            directionPosible.append(False)

        if(1 <= positionY-holeSubtraction <= 10):
            directionPosible.append(True)
        else:
            directionPosible.append(False)

        if(1 <= positionX+holeSubtraction <= 10):
            
            directionPosible.append(True)
        else:
            directionPosible.append(False)

        if(1 <= positionX-holeSubtraction <= 10):
            directionPosible.append(True)
        else:
            directionPosible.append(False)

        return directionPosible

    def emptySpace(self,availablePosible, holeNumbers,player, positionX, positionY):
        #This method checks if exist there is a ship in any direction where you want to place your ship
        initialPositionX = None
        initialPositionY = None
        isPosibleCreateShipInX = True
        isPosibleCreateShipInY = True
        down= availablePosible[0]
        up = availablePosible[1]
        right = availablePosible[2]
        left = availablePosible[3]
        spacesToTraverse = holeNumbers-1

        if(up==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)-index
                if player == True:
                    if(PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                        up=False
                else:
                    if(PLAYER2_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                        up=False
        if(down==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                if player == True:
                    if(PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                        down=False
                else:
                    if(PLAYER2_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                        down=False
        if(right==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                if player == True:
                    if(PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                        right=False
                else:
                    if(PLAYER2_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                        right=False
        if(left==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                if player == True:
                    if(PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                        left=False
                else:
                    if(PLAYER2_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                        left=False

        return up or down or right or left

    def analyzShipPos(self,direction,holeNumbers, positionX, positionY):
        #This method analyzes if the coordinate are in the limits
        result = 0
        holeSubtraction = int(holeNumbers)-1
        if(direction == DIRECTIONS['W']):
            result = positionY-holeSubtraction
        elif(direction == DIRECTIONS['S']):
            result = positionY+holeSubtraction
        elif(direction == DIRECTIONS['D']):
            result = positionX+holeSubtraction
        elif(direction == DIRECTIONS['A']):
            result = positionX-holeSubtraction
        if(result<1 or result>10):
            print('No se puede colocar el barco en esa posición')
            return False
        else:
            return True

    def shipExist(self,direction, holeNumbers, player, positionX, positionY):
        #This method verifies if there are ships in the position where a ship is to be placed
        exist = False
        if(direction ==  DIRECTIONS['W']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)-index
                if player == True:
                    if PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                        exist = True
                else:
                    if PLAYER2_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                        exist = True
        elif(direction == DIRECTIONS['S']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                if player == True:
                    if PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                        exist = True
                else:
                    if PLAYER2_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                        exist = True
        elif(direction == DIRECTIONS['D']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                if player == True:
                    if PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                        exist = True
                else:
                    if PLAYER2_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                        exist = True
        elif(direction == DIRECTIONS['A']):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                if player == True:
                    if PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                        exist = True
                else:
                    if PLAYER2_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                        exist = True

        if exist == True:
            return False
        else:
            return True

    def validationCoordinateAddShip(self,coordinate,player, ship):
        #This method verifies if is posible to create a ship in this position and direction, in order to then create the ship
        translateCoordinate = self.translateCoordinate(coordinate)
        positionX = translateCoordinate[0]
        positionY = translateCoordinate[1]
        holeNumbers = int(re.findall(r'\d+',ship)[0])
        availablePosible = self.availablePosible(holeNumbers, positionX, positionY)
        posibleCreate = self.emptySpace(availablePosible, holeNumbers, player, positionX, positionY)
        if posibleCreate == True:
            direction = self.directionShip(player, ship)
            inLimits = self.analyzShipPos(direction,holeNumbers, positionX, positionY)
            if inLimits == True:
                shipExist = self.shipExist(direction, holeNumbers, player, positionX, positionY)
                if shipExist == True:
                    ships.createShip(coordinate, direction, holeNumbers, player, positionX, positionY, ship)
                else:
                    print('Ya existe un barco en esa posición')
                    self.validationCoordinateAddShip(coordinate, player, ship)
            else:
                print('No se puede colocar un barco en esa direccion')
                self.validationCoordinateAddShip(coordinate, player, ship)
        else:
            print('No es posible colocar un barco en esa posición')
            if player == True:
                playerPerson.getCoordinateAddShip(ship)
            else:
                computerPlayer.randomPosition(ship)

class PlayerPerson:

    def correctCoordinateAddShip(self, ship):
        coordinate = self.getCoordinateAddShip(ship)
        aviableCoordinate = self.aviableCoordinate(coordinate)
        if aviableCoordinate == True:
            return coordinate
        else:
            return self.correctCoordinateAddShip(ship)

    def getCoordinateAddShip(self,ship):
        coordinate = input(f"Give me the position of ship {ship}")
        return coordinate

    def aviableCoordinate(self,coordinate):
        validLetter = self.validLetter(coordinate)
        validNumber = self.validNumber(coordinate)
        return validLetter and validNumber

    def validLetter(self, coordinate):
        letter = re.findall(r'[a-zA-Z]',coordinate)
        if len(letter) == 1:
            return len(re.findall(r'[a-jA-J]',coordinate)) == 1
        else:
            return False

    def validNumber(self, coordinate):
        number = re.findall(r'\d+',coordinate)

        if len(number) == 1:
            return int(number[0]) in range(1,11)
        else:
            return False

    def correctCoordinateShoot(self):
        coordinate = self.getPositionShoot()
        aviableCoordinate = self.aviableCoordinate(coordinate)
        if aviableCoordinate == True:
            ships.shotShip(True,coordinate)
        else:
            return self.correctCoordinateShoot()

    def getPositionShoot(self):
        shoot = input('Captain! Where do you want to shoot?')
        return shoot

class ComputerPlayer:
    #This method generates a random coordinate for the computer player
    def randomPosition(self, ship):
        latter = VALID_LETTERS[random.randint(0,9)]
        number = random.randint(1,10)
        coordinate = f"{latter}{number}"
        validationCoordinate.validationCoordinateAddShip(coordinate,False, ship)

    def randomShot(self):
        latter = VALID_LETTERS[random.randint(0,9)]
        number = random.randint(1,10)
        coordinate = f"{latter}{number}"
        ships.shotShip(False,coordinate)

def convertMusic(soundName):
    mainDir = os.path.dirname(__file__)
    rute = os.path.abspath(os.path.join(mainDir, "SoundLibrary", soundName + ".mp3"))
    print(rute)
    return rute

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(loops=-1)

def stop_audio():
    pygame.mixer.music.stop()
# Función para limpiar la consola
def clearConsole():
    # Verificamos el sistema operativo
    if os.name == 'posix':  # Para sistemas Unix/Linux/MacOS
        _ = os.system('clear')
    elif os.name == 'nt':   # Para Windows
        _ = os.system('cls')

def printMessage():
    clearConsole()
    boards.printBoards(PLAYER1_BATTLESHIP_TABLE,PLAYER2_BATTLESHIP_TABLE)
    for message in messages:
        print(message)
    messages.clear()

def gameOver(player):
    messages.append('Game Over')
    if player == True:
        play_audio(convertMusic('victory-game'))
        messages.append('You win')
    else:
        play_audio(convertMusic('game-over'))
        messages.append('You lose')
    reset()

def reset():
    printMessage()
    play = input('Do you like play again? (y/n)')
    if play.lower() == 'y':
        main()
    elif play.lower() == 'n':
        print('Thanks for playing, I hope you enjoyed')
        sys.exit(0)
    else:
        return self.reset()

def main():
    global PLAYER1_BATTLESHIP_TABLE
    global PLAYER2_BATTLESHIP_TABLE
    global SHOOTS_PLAYER
    global SHIPS_PLAYER
    global SHIPS_COMPUTER
    global LIVES_PLAYER
    global LIVES_COMPUTER
    PLAYER1_BATTLESHIP_TABLE = []
    PLAYER2_BATTLESHIP_TABLE = []
    SHOOTS_PLAYER = []
    SHIPS_PLAYER = {}
    SHIPS_COMPUTER = {}
    LIVES_PLAYER = 5
    LIVES_COMPUTER = 5
    play_audio(convertMusic('start-game'))
    clearConsole()
    boards.createBoards()
    boards.printBoards(PLAYER1_BATTLESHIP_TABLE, PLAYER2_BATTLESHIP_TABLE)
    ships.giveMePositionOfShips(True)

if __name__ == "__main__":
    boards = Boards()
    computerPlayer = ComputerPlayer()
    playerPerson = PlayerPerson()
    ships = Ships()
    validationCoordinate = ValidationCoordinate()
    main()