import keyboard
import re
import os

#Constant

UPPER_FRAME =        "╔═══════════════════════════════════════════╗"
TITLE_TABLE1 =       "║                 Your ships                ║"
TITLE_TABLE2 =       "║                 Your shots                ║"
MIDDLE_LINES_TITLE = "╠═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╣"
CHARACTERS =         "║   ║ A ║ B ║ C ║ D ║ E ║ F ║ G ║ H ║ I ║ J ║"
MIDDLE_LINES =       "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣"
LOW_FRAME =          "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝"
PLAYER1_BATTLESHIP_TABLE = []
PLAYER2_BATTLESHIP_TABLE = []
SHIPS_POSITION1 = {}
VALID_NUMBERS = ['1','2','3','4','5','6','7','8','9','10']
VALID_LETTERS = ['A','B','C','D','E','F','G','H','I','J']
SHIPS_NAMES_HOLES = ['Destroyer (2 holes)','Submarine (3 holes)','Cruiser (3 holes)','Battleship (4 holes)','Carrier (5 holes)']

#Class

#This class creates and prints game tables
class Tables:

#This method fills the list of player tables in the game
    def createTables(self):
        for lista in range(0,10):
            PLAYER1_BATTLESHIP_TABLE.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])
            PLAYER2_BATTLESHIP_TABLE.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])

#This method prints the game tables of the player
    def printTables(self,tablero1, tablero2):
        print(f"{UPPER_FRAME}     {UPPER_FRAME}")
        print(f"{TITLE_TABLE1}     {TITLE_TABLE2}")
        print(f"{MIDDLE_LINES_TITLE}     {MIDDLE_LINES_TITLE}")
        print(f"{CHARACTERS}     {CHARACTERS}")
        print(f"{MIDDLE_LINES}     {MIDDLE_LINES}")
        rowCount=0
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

#This class creates ships for the players and verifies if the position si correct
class AddShips:

#This method requests the position of ships
    def giveMePositionOfShips(self):
        for ship in SHIPS_NAMES_HOLES:
            self.getCoordinate(ship)
            clearConsole()
            tables.printTables(PLAYER1_BATTLESHIP_TABLE,PLAYER2_BATTLESHIP_TABLE)
        for clave, valor in SHIPS_POSITION1.items():
            print(clave, valor)

#This method verifies if the coordinate has the correct characters 
    def getCoordinate(self,ship):
        caracterLetra = False
        caracterNumero = False
        message = None
        coordinate = input(f"Give me the position of ship {ship}")
        #Her verifies if the coordinate sizes is 2 or 3, later verifies if tis have correct characters
        if(len(coordinate)==2):
            for caracter in coordinate:
                if caracter.upper() in VALID_LETTERS and caracterLetra == False:
                    caracterLetra = True
                elif(caracter in VALID_NUMBERS and caracterNumero == False):
                    caracterNumero = True
            if(caracterNumero and caracterLetra == True):
                self.validationCoordinate(coordinate, ship)
            else:
                print('La coordenada no es correcta, intentelo de nuevo')
                self.getCoordinate(ship)
        elif(len(coordinate)==3):
            if len(re.findall(r'\d+', coordinate)) == 1:
                for index, caracter in enumerate(coordinate):
                    if caracter.upper() in VALID_LETTERS and caracterLetra == False:
                        caracterLetra = True
                    elif(caracter in VALID_NUMBERS and caracterNumero == False):
                        caracterNumero = True
                        if(caracter == '1'):
                            if(coordinate[index+1] !='0'):
                                caracterNumero = False
                        
                if(caracterNumero and caracterLetra == True):
                    self.validationCoordinate(coordinate, ship)
                else:
                    print('La coordenada no es correcta, intentelo de nuevo')
                    self.getCoordinate(ship)
            else:
                print('La coordenada no es correcta, intentelo de nuevo')
                self.getCoordinate(ship)
        else:
            print('La coordenada no es correcta, intentelo de nuevo')
            self.getCoordinate(ship)

#This method translates the player input coordinate
    def translateCoordinate(self, coordinate):
        positionX = None
        positionY = int(re.findall(r'\d+', coordinate)[0])
        for index, character in enumerate(VALID_LETTERS):
            if character == re.findall(r'[a-zA-Z]+', coordinate)[0].upper():
                positionX = index+1
        result = [positionX, positionY]
        return result

#This method takes the expansion direction of the ships
    def directionShip(self,ship):
        tecla_pulsada = None
        print(f'En que direccion se extiende el barco {ship}?')
        print('W(Arriba), S(Abajo), D(Derecha), A(Izquierda)')

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

        return tecla_pulsada

#This method checks if it´s possibles to create a ship at this position, provided it´s whithin the game board 
    def availablePosible(self, holeNumbers, positionX, positionY):
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

#This method checks if exist there is a ship in any direction where you want to place your ship
    def emptySpace(self, holeNumbers, positionX, positionY, availablePosible):
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
                if(PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                    up=False
        if(down==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                if(PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o'):
                    down=False
        if(right==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                if(PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                    right=False
        if(left==True):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                if (PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o'):
                    left=False

        return up or down or right or left

#This method analyzes if the coordinate are in the limits 
    def analyzShipPos(self,direction,holeNumbers, positionX, positionY):
        result = 0
        holeSubtraction = int(holeNumbers)-1
        if(direction=='W'):
            result = positionY-holeSubtraction
        elif(direction=='S'):
            result = positionY+holeSubtraction
        elif(direction=='D'):
            result = positionX+holeSubtraction
        elif(direction=='A'):
            result = positionX-holeSubtraction
        if(result<1 or result>10):
            print('No se puede colocar el barco en esa posición')
            return False
        else:
            return True

#This method verifies if there are ships in the position where a ship is to be placed
    def shipExist(self,direction, holeNumbers, positionX, positionY):
        exist = False
        if(direction == 'W'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)-index
                if PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                    exist=True
        elif(direction =='S'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                if PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] == 'o':
                    exist=True
        elif(direction =='D'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                if PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                    exist=True
        elif(direction =='A'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                if PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] == 'o':
                    exist = True
        if exist == True:
            print("Ya existe un barco en esa posición")
            return False
        else:
            return True

#This method verifies if is posible to create a ship in this position and direction, in order to then create the ship
    def validationCoordinate(self,coordinate, ship):
        translateCoordinate = self.translateCoordinate(coordinate)
        positionX = translateCoordinate[0]
        positionY = translateCoordinate[1]
        holeNumbers = int(re.findall(r'\d+',ship)[0])
        availablePosible = self.availablePosible(holeNumbers, positionX, positionY)
        posibleCreate = self.emptySpace(holeNumbers, positionX, positionY, availablePosible)
        if posibleCreate == True:
            direction = self.directionShip(ship)
            inLimits = self.analyzShipPos(direction,holeNumbers, positionX, positionY)
            if inLimits == True:
                shipExist = self.shipExist(direction, holeNumbers, positionX, positionY)
                if shipExist == True:
                    self.createShip(holeNumbers,direction,positionX,positionY,coordinate,ship)
                else:
                    print('Ya existe un barco en esa posición')
                    self.validationCoordinate(coordinate, ship)
            else:
                print('No se puede colocar un barco en esa direccion')
                self.validationCoordinate(coordinate, ship)
        else:
            print('No es posible colocar un barco en esa posición')
            self.getCoordinate(ship)

#This method creates a ship on the game tables for players
    def createShip(self,holeNumbers,direction,positionX,positionY,coordinate,ship):
        if(direction=='W'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)-index
                PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] = 'o'
        elif(direction=='S'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionY-1)+index
                PLAYER1_BATTLESHIP_TABLE[piceOfShip][positionX] = 'o'
        elif(direction=='D'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)+index
                PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] = 'o'
        elif(direction=='A'):
            for index in range(0,int(holeNumbers)):
                piceOfShip = (positionX)-index
                PLAYER1_BATTLESHIP_TABLE[positionY-1][piceOfShip] = 'o'
        SHIPS_POSITION1[ship.split()[0]] = [direction,coordinate]

# Función para limpiar la consola
def clearConsole():
    # Verificamos el sistema operativo
    if os.name == 'posix':  # Para sistemas Unix/Linux/MacOS
        _ = os.system('clear')
    elif os.name == 'nt':   # Para Windows
        _ = os.system('cls')

if __name__ == "__main__":
    tables = Tables()
    tables.createTables()
    tables.printTables(PLAYER1_BATTLESHIP_TABLE, PLAYER2_BATTLESHIP_TABLE)
    
    ships = AddShips()
    ships.giveMePositionOfShips()