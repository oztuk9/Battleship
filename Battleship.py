import keyboard
import re

upperFrame =        "╔═══════════════════════════════════════════╗"
titleTable1 =       "║                 Your ships                ║"
titleTable2 =       "║                 Your shots                ║"
middleLinesTitle =  "╠═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╣"
characters =        "║   ║ A ║ B ║ C ║ D ║ E ║ F ║ G ║ H ║ I ║ J ║"
middleLines =       "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣"
lowFrame =          "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝"
player1BattleshipTable = []
player2BattleshipTable = []
shipsPosition1 = {}
numerosValidos = ['1','2','3','4','5','6','7','8','9','10']
letrasValidas = ['A','B','C','D','E','F','G','H','I','J']
ships = ['Destroyer (2 holes)','Submarine (3 holes)','Cruiser (3 holes)','Battleship (4 holes)','Carrier (5 holes)']


def fillList():
    for lista in range(0,10):
        player1BattleshipTable.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])
        player2BattleshipTable.append([str(lista+1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])

def printTables(tablero1, tablero2):
    print(f"{upperFrame}     {upperFrame}")
    print(f"{titleTable1}     {titleTable2}")
    print(f"{middleLinesTitle}     {middleLinesTitle}")
    print(f"{characters}     {characters}")
    print(f"{middleLines}     {middleLines}")
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
            print(f"{middleLines}     {middleLines}")
        else:
            print(f"{lowFrame}     {lowFrame}")
        rowCount+=1

def giveMePositionOfShips():
    for ship in ships: 
        coordValidation(ship)
    for clave, valor in shipsPosition1.items():
        print(clave, valor)
        
def coordValidation(ship):
    caracterLetra = False
    caracterNumero = False
    coordinate = input(f"Give me the position of ship {ship}")
    if(len(coordinate)==2):
        print('La coordenada tiene el tamaño adecuado es de 2')
        for caracter in coordinate:
            if caracter.upper() in letrasValidas and caracterLetra == False:
                caracterLetra = True
            elif(caracter in numerosValidos and caracterNumero == False):
                caracterNumero = True
        if(caracterNumero and caracterLetra == True):
            directionShip(coordinate,ship)
            print(f'Letra: {caracterLetra} Numero: {caracterNumero}')
            print('La coordenada cumple con los caracteres correspondientes')
        else:
            print('La coordenada no es correcta, intentelo de nuevo')
            coordValidation(ship)
    elif(len(coordinate)==3):
        print('La coordenada tiene el tamaño adecuadi, es de 3')
        for index, caracter in enumerate(coordinate):
            if caracter.upper() in letrasValidas and caracterLetra == False:
                caracterLetra = True
            elif(caracter in numerosValidos and caracterNumero == False):
                if(caracter == '1'):
                    if(coordinate[index+1]=='0'):
                        caracterNumero = True
        if(caracterNumero and caracterLetra == True):
            directionShip(coordinate,ship)
            print(f'Letra: {caracterLetra} Numero: {caracterNumero}')
            print('La coordenada cumple con los caracteres correspondientes')
        else:
            print('La coordenada no es correcta, intentelo de nuevo')
            coordValidation(ship)
    else:
        print('La coordenada no es correcta, intentelo de nuevo')
        coordValidation(ship)

def directionShip(coordinate,ship):
    print(f'En que direccion se extiende el barco {ship}?')
    print('W(Arriba), S(Abajo), D(Derecha), A(Izquierda)')
    tecla_pulsada = ''
    while True:
        evento = keyboard.read_event(suppress=True)
        tecla_pulsada = evento.name.upper()
        print(f"Presionaste la tecla: {tecla_pulsada}")
        if tecla_pulsada == 'W':
            print("Arriba")
            break
        if tecla_pulsada == 'S':
            print("Abajo")
            break
        if tecla_pulsada == 'A':
            print("Izquierda")
            break
        if tecla_pulsada == 'D':
            print("Derecha")
            break
    analyzShipPos(coordinate, tecla_pulsada,ship)
    print(f'Barco: {ship.split()[0]}, Direccion: {tecla_pulsada}, Coordenada: {coordinate}')
    shipsPosition1[ship.split()[0]] = [tecla_pulsada,coordinate]
    
def analyzShipPos(coordinate, direccion,ship):
    positionX = None
    positionY = None
    result = None
    holeNumbers = int(re.findall(r'\d+',ship)[0])-1
    for indexC, character in enumerate(coordinate):
        index=0
        while index < len(letrasValidas):
            if character.upper()==letrasValidas[index]:
                positionX=index+1
                break
            elif(str(index+1)==character):
                if(character=='1' and len(coordinate)==3):
                    print('El numero encontrado es 1')
                    print(f'El siguiente valor es {coordinate[indexC+1]}')
                    if(coordinate[indexC+1]=='0'):
                        positionY = 10
                    else:
                        positionY=int(character)
                else:
                    positionY=int(character)
                break
            index+=1
    print(f'positionX: {positionX}, positionY {positionY}')
    if(direccion=='W'):
        result = positionY-int(holeNumbers)
    elif(direccion=='S'):
        result = positionY+int(holeNumbers)
    elif(direccion=='D'):
        result = positionX+int(holeNumbers)
    elif(direccion=='A'):
        result = positionX-int(holeNumbers)
    if(result<1 or result>10):
        print('La cooredenada supera los limites del tablero del juego')
        directionShip(coordinate,ship)
    else:
        player1BattleshipTable[positionY][positionX] = 'o'
        if(direccion=='W'):
            result = positionY-int(holeNumbers)
        elif(direccion=='S'):
            result = positionY+int(holeNumbers)
        elif(direccion=='D'):
            result = positionX+int(holeNumbers)
        elif(direccion=='A'):
            result = positionX-int(holeNumbers)
        printTables(player1BattleshipTable,player2BattleshipTable)
        print(f'Resultados: {result}')

fillList()
printTables(player1BattleshipTable,player2BattleshipTable)
giveMePositionOfShips()