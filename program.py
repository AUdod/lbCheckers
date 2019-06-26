import os
import random
import time

def confirmInput():
    confirm = input("Все правильно? [Y|N] [Д|Н] ")
    if confirm in ["Y","Д"]:
        return True
    elif confirm in ["N", "Н"]:
        return False
    else:
        return confirmInput()

def printStackers(stateArr):
    out = stateArr.copy()
    out[out.index(0)] = "_"
    i = 0
    while i < 8:
            print(out[i], " ", out[i+1], " ", out[i+2])
            i += 3

            
def getInput():
    newInput = input ("Введите 9 цифр от 0 до 8 через пробел (пустая ячейка = 0): ")
    # Валидация
    """ result = False """
    allowedChars = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '0']
    positions = [0,1,2,3,4,5,6,7,8]
    if len(newInput) == 17:
        for char in newInput:
            """ print(char) """
            if not char  in allowedChars:
                print("Вы ввели некорректные символы!")
                getInput()
        parsedInput = list(map(int, newInput.split(" ")))
        """ print(parsedInput) """
        for num in parsedInput:
            if num in positions:
                positions.remove(num)
            else:
                print("Вы ввели неправильный номер ячейки")
                getInput()
        print("Введенное состояние: ")
       
        printStackers(parsedInput)
        
        if not confirmInput():
            getInput()
        else:
            return parsedInput

    else:
        print("Вы ввели слишком много символов")
        getInput()
    """ print("Вы ввели: ", parsedInput) """
    return False

def generateStates(stateArr, directionsDicts):
    """ print(directionsDicts) """
    #Найти 0
    position = stateArr.index(0)
    newStates = dict()
    for direct, pos in directionsDicts[position].items():
        currState = stateArr.copy()
        currState[position] = currState[pos]
        currState[pos] = 0
        newStates.update({direct : currState})
    
    return newStates

## Генерация вариантов перемещений для каждой из позиций
def generateStatesDirections(size):
    positions = []
    for i in range(size*size):
        positions.append(i)
    
    directions = dict()
    for pos in positions:
        newPositions = dict()
        if  pos - size in positions:
            newPositions.update({'u' : pos - size})
        if pos + 1 in positions and (pos % size) < (size - 1):
            newPositions.update({'r' : pos + 1})
            """ newPositions.append('r')
            newPositions['r'].update(pos + 1) """
        if pos + size in positions:
            newPositions.update({'d' : pos + size})
            """ newPositions['d'].append(pos + size) """
        if pos - 1 in positions and pos % size > 0:
            newPositions.update({'l' : pos - 1})
            """ newPositions['l'].append(pos - 1) """
        directions.update({ pos : newPositions})
        """ print("Полученные перемещения ", directions) """
    """ print("Позиции ", positions) """
    return directions

def deapthSearch(state, searchingState, directionsDicts, exitParam):
    print("Поиск в глубину")
    start_time = time.time()
    path = ''
    currState = state.copy()
    findedStates = []
    steps = 0
    finded = False
    stpBack = {'u' : 'd', 'd' : 'u', 'r' : 'l', 'l' : 'r'}

    while exitParam > len(findedStates) and not finded : ##Вопрос: какое правильное условие выхода?
        print(" ",len(findedStates),"/", exitParam, " состояний найдено. ", steps, " шагов", end="\r")
        states = generateStates(currState, directionsDicts)
        if not currState in findedStates:
            findedStates.append(currState)
        possibleDirections = []
        steps += 1

        if searchingState in list(states.values()):
            finded = True
            
            for dirn, st in states.items():
                if st == searchingState:
                    path += dirn
            
    
        for dirn, st in states.items():
            if not st in findedStates:
                possibleDirections.append(dirn)
        
        if len(possibleDirections) > 0 :
            newDirection = possibleDirections[random.randint(0, len(possibleDirections)-1)]
            currState = states[newDirection]
            path += newDirection
            """ print("Нов. состояние: ", currState) """

        else:
            newDirection = stpBack[path[-1:]]
            currState = states[newDirection]
            path = path[:-1]
            """ print("Назад") """
        
    
    if finded:
        print("Состояние найдено. Путь: ", path, " Глубина: ", len(path), " Шагов: ", steps)
    else:
        print("Состояние не найдено. Путь: ", path, " Глубина: ", len(path), " Шагов: ", steps)

    print("--- %s seconds ---" % (time.time() - start_time))
    return path

def widthSearch(startState, searchState, directionsDicts, deapth):
    start_time = time.time()
    print("Поиск в ширину. Глубина: ", deapth)
    findedStates = [startState]
    front = [startState]
    resultPath = ''
    history = dict()
    history.update({''.join(map(str, startState)) : ''}) ##Кратчайшие пути до всех состояний
    finded = False
    currDeapth = 0
    while deapth >= currDeapth and not finded:
        print(" ",len(findedStates), " состояний найдено. ",  " Текущая глубина: ",currDeapth, " Размер фронта: ", len(front), end="\r")
        currDeapth += 1
        newFront = []
        for st in front:
            dirSt = generateStates(st, directionsDicts)
            for dirn, newSt in dirSt.items():
                if not newSt in findedStates:
                    
                    pathToSt = history[''.join(map(str, st))] + dirn
                    history.update({''.join(map(str, newSt)) : pathToSt})
                    if newSt == searchState:
                        
                        resultPath = pathToSt
                        finded = True
                    else:
                        findedStates.append(newSt)
                        newFront.append(newSt)
        front = newFront
    print("\nГлубина: ", currDeapth)
    print("--- %s seconds ---" % (time.time() - start_time))
    return resultPath
    
def traceSearch(startState, searchState,directionsDicts, lenght):
    


    checkedPathes = [] ## Пути конечной длины
    fullyChecked = [] ## Родительские пути
    searchedPathes = []
    pos = startState.index(0)
    checker = ''
    stpBack = {'u' : 'd', 'd' : 'u', 'r' : 'l', 'l' : 'r'}

    


    def moveForward(): 
        ##Идти вперед до упора
        """ for dirn, nPos in directionsDicts[pos]:
            if  """
        newPoses = directionsDicts[pos]
        for dirn, nPos in newPoses:
            newPath = checker + dirn
            ## Проверка на не упор
            if len(newPath) < lenght and not newPath in fullyChecked:
                checker = newPath
                print("Неполный путь: ", newPath)
                pos = nPos
                moveForward()
            if len(newPath) == lenght and not newPath in checkedPathes:
                checker = newPath
                pos = nPos
                print("Полный путь: ", newPath)
                break
 
        
    def moveBackward(): ## Идти назад до нахождения ноды, от которой есть куда идти
        lastStep = checker[-1:]
        checker = checker[:-1]
        sBack = stpBack[lastStep]
        pos = directionsDicts[pos][sBack]
        print("Шаг назад: ", sBack, " Полученная позиция: ", pos) 
        newPoses = directionsDicts[pos]
        haveWay = False
        for dirn, nPos in newPoses:
            newPath = checker+dirn
            if len(newPath) < lenght and not newPath in fullyChecked:
                haveWay = True
            if len(newPath) == lenght and not newPath in checkedPathes:
                haveWay = True
        if not haveWay:
            print("Нет пути от ", checker)
            fullyChecked.append(checker)
            moveBackward()
    
    
    def generateStateFromPath():
        indexPos = startState.index(0)
        currState = startState.copy()
        for c in checker:
            currPos = directionsDicts[indexPos][c]
            currState[indexPos] = currState[currPos]
            currState[currPos] = 0
            indexPos = currPos
        return currState




    while True: ##Основной цикл
        moveForward()
        
        ##проверка чекера на длину и включение. В случае, если достигли нужной длины, проверяем состояние
        
        if len(checker) == lenght:
            newState = generateStateFromPath()
            if newState == searchState:
                searchedPathes.append(checker)
                checkedPathes.append(checker)
            else:
                checkedPathes.append(checker)
        if checker == '':
            print("Граф закончился")
            break

        moveBackward()


        

    
# Main
print("Расположение позиций:")
i = 0
while i < 8:
    print(i, " ", i+1, " ", i+2)
    i += 3

print("Введите начальное состояние")
startState = getInput()
""" print("Вы ввели: ", startState) """
os.system('cls')

print("Введите искомое состояние")
endState = getInput()
""" print("Вы ввели: ", startState) """
os.system('cls')

print("Начальное состояние: ", startState)
print("Искомое состояние: ", endState)
print("Направления: \n\tu\t\nl\t*\tr\n\td\t")

directions = generateStatesDirections(3)
""" dfsPath = deapthSearch(startState, endState, directions, 362880) """
""" wsPath = widthSearch(startState, endState, directions, 100) """
tsResult = traceSearch(startState, endState, directions, 4)
""" print(directions) """
print("\nПолученный путь поиска по лучу на заданную глубину: ", tsResult)

""" directions = generateStatesDirections(3) """


print()
  
""" print(swapList(newList))  """
