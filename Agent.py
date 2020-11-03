from Cell import cell
import random as rand
import numpy as np
from sympy import * 

cardinal = [(-1,0), (0,-1), (1,0), (0,1),(-1,-1), (1,-1), (1,1), (-1,1)]
dim = 0; explosions = 0 
inferred = set(); visited = set()
solvedCells = dict()

def setupKB(dim,unvisited):
    kb = [[cell(j,i) for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(dim):
            unvisited.add((i,j))
    return kb

def checkNeighbors(cell,kb): #initial check to record data for a cell
    """Checks neighbors for a given cell and stores findings within cell object

    Args:
        cell (cell): cell to be checked
    """
    safeSurr = 0; mineSurr = 0; hiddenSurr = 0
    for mov in cardinal:
        
        x = cell.x; y = cell.y
        x += mov[0]; y += mov[1]
        if (x >= 0 and x < dim and y >=0 and y < dim):
            currCell = kb[x][y]
            #print("checked neighbor status:", currCell.status,x,y)
            if currCell.status == -1:
                hiddenSurr += 1
            elif currCell.status == 0:
                safeSurr += 1 
            else:
                mineSurr += 1 
    
    cell.mineSurr = mineSurr; cell.hiddenSurr = hiddenSurr; cell.safeSurr = safeSurr #we may not need safeSurr

def markHidden(status,cell,q,kb):
    if status == "MINE": 
        mark = 10
    elif status == "SAFE":
        mark = 0
    for mov in cardinal:
        x = cell.x; y = cell.y
        x += mov[0]; y += mov[1]
        if (x >= 0 and x < dim and y >=0 and y < dim):
            currCell = kb[x][y]
            if currCell.status == -1:
                currCell.status = mark
                if (x,y) not in q: 
                    q.append((x,y)) #avoid adding duplicates to q
                    #print("in MarkHidden adding: ", x,y)
            elif currCell.status != 10 and status == "SAFE": 
                if (x,y) not in q: 
                    q.append((x,y))
                    #print("adding already uncovered: ", x,y)

def recheckNeighbors(Q,toVisitQ,unvisited,userBoard,kb,flag): #adds safe neighbors to q for rechecking when a cell is marked as a mine/safe
    while Q:
        x1,y1 = Q.pop()
        if flag == "MINE": 
            userBoard[x1,y1] = 10
            kb[x1][y1].status = 10
        unvisited.discard((x1,y1))
        for mov in cardinal:
            x = x1; y = y1
            x += mov[0]; y += mov[1]
            if (x >= 0 and x < dim and y >=0 and y < dim):
                currCell = kb[x][y]
                if currCell.status != 0: continue
                if (x,y) not in toVisitQ: 
                    #print("readded ",x,y, " to check")
                    toVisitQ.append((x,y))

def uncoverCell(cell,msBoard):
    """[summary]

    Args:
        cell ([type]): [description]
        msBoard ([type]): [description]

    Returns:
        boolean : true if mine false otherwise
    """
    cell.status = 0 
    cell.clue = msBoard.board[cell.x,cell.y]
    msBoard.userBoard[cell.x,cell.y] = cell.clue
    if cell.clue == -1: 
        #print("boom!") #bomb went off
        return True
    else:
        return False

def addrandom(toVisitQ,unvisited):
    toVisitQ.append(rand.choice(tuple(unvisited)))

def basicAgent(msBoard):
    global dim; global explosions
    explosions = 0
    dim = msBoard.dim
    toVisitQ = []
    mineQ = []
    unvisited = set()
    kb = setupKB(msBoard.dim,unvisited)
    addrandom(toVisitQ,unvisited)
    while unvisited:
        #print(len(unvisited)) #to show progress
        if toVisitQ: #
            #msBoard.printBoard(1) #use this to print board per iteration
            currX,currY = toVisitQ.pop()
            currCell = kb[currX][currY]
            #print ("here",currX,currY)
            unvisited.discard((currX,currY))
            
            if uncoverCell(currCell,msBoard): #if uncovered cell was a bomb
                explosions+=1
                currCell.status = 10 #flag the bomb we set off
                msBoard.userBoard[currX,currY] = 10
                mineQ.append((currX,currY))
                recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")

            checkNeighbors(currCell,kb)
            #print("clue: ", currCell.clue, "hidden: ",currCell.hiddenSurr,"flags: ",currCell.mineSurr)

            #Basic logical inference + propagation when conclusions are made that may affect adjacent safe cells
            if currCell.hiddenSurr == currCell.clue - currCell.mineSurr and currCell.hiddenSurr > 0: # every hidden cell is a mine
                #print("set mines")
                markHidden("MINE",currCell,mineQ,kb)
                recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")
            elif currCell.clue == currCell.mineSurr and currCell.hiddenSurr > 0: #every hidden cell is safe
                #print("set safe")
                tempList = []
                markHidden("SAFE",currCell,tempList,kb)
                for coords in tempList:
                    if coords not in toVisitQ: toVisitQ.append(coords)
                recheckNeighbors(tempList,toVisitQ,unvisited,msBoard.userBoard,kb,"SAFE")

            
        else:
            #print("had to add random")
            addrandom(toVisitQ,unvisited)
        
    return explosions

def getEqPosition(x,y):
    """Given an x and y, gives the position in the clue equation

    Args:
        x (int): x coordinate
        y (int): y coordinate
    """
    return x*dim+y

def getCoords(EqPosition):
    x = EqPosition // dim
    y = EqPosition % dim
    return (x,y)



def genClueEquation(cell,kb):
    checkNeighbors(cell,kb)
    clueEq = np.zeros(dim**2+2) #first position is unique clue cell number last is clue
    if cell.hiddenSurr == 0: return (False,clueEq)
    clueEq[dim**2] = cell.clue - cell.mineSurr
    clueEq[dim**2+1] = getEqPosition(cell.x,cell.y)
    for mov in cardinal:
        x = cell.x; y = cell.y
        x += mov[0]; y += mov[1]
        if (x >= 0 and x < dim and y >=0 and y < dim):
            currCell = kb[x][y]
            if currCell.status == -1: #for the hidden cells add their locations as 1 to the clueEq
                clueEq[getEqPosition(x,y)] = 1
    
    #print("clue eq: ", clueEq)
    return (True, clueEq)

    

def updateKBmatrix(kbMatrix, kb,newVisited):
    for x,y in newVisited:
        cell = kb[x][y]
        if cell.clue != -1: #if cell is not a mine/ undiscovered
            
            for row in kbMatrix:
                if row[dim**2+1] == getEqPosition(cell.x,cell.y): #when unique cellRow Ids are equal
                    eqTuple = genClueEquation(cell,kb)
                    if eqTuple[0]: row[:] = eqTuple[1] 
                    break
            else: #row for current cell does not exist
                eqTuple = genClueEquation(cell,kb)
                if eqTuple[0]: kbMatrix.append(eqTuple[1])

def writeSolvedCells(augMat,solvedCells):
    for i in range(augMat.shape[0]):
        for j in range(augMat.shape[1] - 1):
            coords = getCoords(j)
            if coords in solvedCells:
                val = solvedCells[coords]
                augMat[i,augMat.shape[1]-1] -= val*augMat[i,j]
                augMat[i,j] = 0


def simplifyKBmatrix(kbMatrix, toVisitQ, mineQ, kb, unvisited, msBoard):
    newInfo = False
    augMat = np.array(kbMatrix)[:,:dim**2+1]
    augMat = augMat[~(augMat==0).all(1)] #remove all 0 rows 
    writeSolvedCells(augMat,solvedCells)
    #print(augMat)

    kbRref,pivots = [Matrix(augMat).rref()[i] for i in range(2)]
    #print("Simplified matrix")
    #print(kbRref)

    #print("pivots: ", len(pivots),"rows in rref: ", kbRref.shape[0]) 
    i = 0; k = 0
    while i<kbRref.shape[0] and k < len(pivots): 
        pivot = pivots[k]
        #print("i ",i,"pivot ", pivot)
        varList = []
        varSum = 0
        for j in range(pivot, kbRref.shape[1]-1):
            
            if kbRref[i,j] != 0:
                varList.append((j, kbRref[i,j]))
                varSum += kbRref[i,j]        

        #all cells are mines
        if kbRref[i,kbRref.shape[1]-1] == varSum and kbRref[i,kbRref.shape[1]-1] == len(varList): 
            
            for cell in varList:
                x,y = getCoords(cell[0])
                if (x,y) in inferred: 
                    continue
                newInfo = True
                inferred.add((x,y))
                #print("CLUE ROW:",kbRref[i,:])
                #print("Successfully inferred: ",x,y, " is a mine")

                mineQ.append((x,y))
            
            kbRref = np.delete(kbRref,i,0) #Once a clue is used completely, delete it
            i-=1
            recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")
        
        #all cells are safe  
        elif varSum == len(varList) and kbRref[i,kbRref.shape[1]-1] == 0:
            tempList = []
            for cell in varList:
                x,y = getCoords(cell[0])
                if (x,y) in inferred: 
                    continue
                newInfo = True
                inferred.add((x,y))
                #print("CLUE ROW:",kbRref[i,:])
                #print("Successfully inferred: ",x,y, " is SAFE")
                
                tempList.append((x,y))

            kbRref = np.delete(kbRref,i,0) #Once a clue is used completely, delete it
            i-=1
            for coords in tempList:
                if coords not in toVisitQ: toVisitQ.append(coords)
            recheckNeighbors(tempList,toVisitQ,unvisited,msBoard.userBoard,kb,"SAFE")


        #if 2 variables and 1 is negative and 1 possible mine -> one must be mine and one must be safe
        elif len(varList) == 2 and varSum == 0 and kbRref[i,kbRref.shape[1]-1] == 1:
            #print("We are at 2 variables")
            #print("CLUE ROW:",kbRref[i,:])
            tempList = []
            cell1 = varList[0]
            cell2 = varList[1]
            x1,y1 = getCoords(cell1[0])
            x2,y2 = getCoords(cell2[0])
            #print("cell 1: ",cell1[1],"cell 2: ",cell2[1], "is cell 1 a mine: ",1 * cell1[1] + 0 * cell2[1] == 1)
            if 1 * cell1[1] + 0 * cell2[1] == 1:
                if (x1,y1) not in inferred: 
                    newInfo = True
                    inferred.add((x1,y1))
                    #print("Successfully inferred1: ",x1,y1, " is a mine")
                    mineQ.append((x1,y1))
                
                if (x2,y2) not in inferred:
                    newInfo = True
                    inferred.add((x2,y2))
                    tempList.append((x2,y2))
            
            else: # cell2 is a mine, cell1 is safe
                if (x2,y2) not in inferred: 
                    newInfo = True
                    inferred.add((x2,y2))
                    #print("Successfully inferred2: ",x2,y2, " is a mine")
                    mineQ.append((x2,y2))
                
                if (x1,y1) not in inferred:
                    newInfo = True
                    inferred.add((x1,y1))
                    tempList.append((x1,y1))

            
            if newInfo:
                kbRref = np.delete(kbRref,i,0) #Once a clue is used completely, delete it
                i-=1
                recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")
                for coords in tempList:
                    if coords not in toVisitQ: toVisitQ.append(coords)
                recheckNeighbors(tempList,toVisitQ,unvisited,msBoard.userBoard,kb,"SAFE")
        i+=1; k+=1
    
    #print("kbRref len: ", kbRref.shape[0])
    kbMatrix = np.hstack((kbRref,np.full((kbRref.shape[0],1),-1)))#make this the rref + column of -1 to its right

    return newInfo

def improvedAgent(msBoard):
    randomAdds = 0
    global dim; global explosions; global inferred; global visited; global solvedCells
    explosions = 0; dim = msBoard.dim; inferred = set(); visited = set(); solvedCells = dict()
    prevVisited = set()
    toVisitQ = []
    mineQ = []
    unvisited = set()
    kbMatrix = []
    kb = setupKB(msBoard.dim,unvisited)
    addrandom(toVisitQ,unvisited)
    while unvisited:
        #print(len(unvisited))
        if toVisitQ: #
            currX,currY = toVisitQ.pop()
            currCell = kb[currX][currY]
            #print ("here",currX,currY)
            unvisited.discard((currX,currY))
            visited.add((currX,currY))
            #msBoard.printBoard(1)
            
            if uncoverCell(currCell,msBoard): #if uncovered cell was a bomb
                explosions+=1
                currCell.status = 10 #flag the bomb we set off
                msBoard.userBoard[currX,currY] = 10
                mineQ.append((currX,currY))
                recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")

            checkNeighbors(currCell,kb)
            solvedCells[(currX,currY)] = 1 if currCell.clue == -1 else 0 

            #print("clue: ", currCell.clue, "hidden: ",currCell.hiddenSurr,"flags: ",currCell.mineSurr)
            #Basic logical inference + propagation when conclusions are made that may affect adjacent safe cells
            if currCell.hiddenSurr == currCell.clue - currCell.mineSurr and currCell.hiddenSurr > 0: # every hidden cell is a mine
                #print("set mines")
                markHidden("MINE",currCell,mineQ,kb)
                recheckNeighbors(mineQ,toVisitQ,unvisited,msBoard.userBoard,kb,"MINE")
            elif currCell.clue == currCell.mineSurr and currCell.hiddenSurr > 0: #every hidden cell is safe
                #print("set safe")
                tempList = []
                markHidden("SAFE",currCell,tempList,kb)
                for coords in tempList:
                    if coords not in toVisitQ: toVisitQ.append(coords)
                recheckNeighbors(tempList,toVisitQ,unvisited,msBoard.userBoard,kb,"SAFE")
            
        else:
            #if basic agent cannot make conclusions: generate equations and try to solve
            #print("Updating kb")
            newVisited = visited-prevVisited
            if len(newVisited) < 10:
                addrandom(toVisitQ,unvisited)
                continue

            updateKBmatrix(kbMatrix,kb,newVisited)
            prevVisited = visited.copy()
            

            #print(kbMatrix)
            newInfo = False
            if kbMatrix:
                #print("simplifying rref rn")
                newInfo = simplifyKBmatrix(kbMatrix, toVisitQ, mineQ, kb, unvisited, msBoard)
            
            if not newInfo: 
                #print("had to add random")
                addrandom(toVisitQ,unvisited)
                
    print("Improved Agent explosions: ",explosions)
    return explosions

        

                
                



                
        
            
