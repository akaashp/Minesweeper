from Cell import cell
import random as rand
cardinal = [(-1,0), (0,-1), (1,0), (0,1),(-1,-1), (1,-1), (1,1), (-1,1)]
dim = 0; explosions = 0 
def setupKB(dim,unvisited):
    kb = [[cell(j,i) for i in range(dim)] for j in range(dim)]

    for i in range(dim):
        for j in range(dim):
        #if (i == 0 or i == dim-1) and (j ==0 or j == dim-1):
        #       kb[i][j] = cell(i,j,possNeighbors = 3)
        #    elif i == 0 or i == dim-1 or j ==0 or j == dim-1: 
        #        kb[i][j] = cell(i,j,possNeighbors = 5)  
        #    else:   
        #        kb[i][j] = cell(i,j)
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
        #print("cells coord",x,y,mov[0],mov[1])
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
    
    cell.mineSurr = mineSurr; cell.hiddenSurr = hiddenSurr; cell.safeSurr = safeSurr

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
                    #print("adding: ", x,y)
            elif currCell.status != 10 and status == "SAFE": #check if this actually helps 
                if (x,y) not in q: 
                    q.append((x,y))
                    #print("adding already uncovered: ", x,y)

def recheckNeighbors(Q,toVisitQ,unvisited,userBoard,kb,flag): #adds safe neighbors to q for rechecking when a cell is marked as a mine/safe
    while Q:
        x1,y1 = Q.pop()
        if flag == "MINE": userBoard[x1,y1] = 10
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
        #print("boom!")
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
        #print(len(unvisited))
        if toVisitQ: #
            #msBoard.printBoard(1)
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

        

                
                



                
        
            
