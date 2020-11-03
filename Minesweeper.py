import random as rand
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
#
#
# KEY FOR BOARD
# -1 : mine, 0-8: #of surrounding mines, 10 : flag, 9 : visited
#
class msBoard:
    def placeMine(self,i,j):
        cardinal = [(-1,0), (0,-1), (1,0), (0,1),(-1,-1), (1,-1), (1,1), (-1,1)]
        self.board[i,j] = -1
        for mov in cardinal:
            x = i; y = j
            x += mov[0]; y += mov[1]
            if (x >= 0 and x < self.dim and y >=0 and y < self.dim): #ensure in bounds and update surrounding squares 
                if self.board[x,y] != -1: self.board[x,y]+=1 

    def genBoard(self):
        toBePlaced = self.mines
        while toBePlaced > 0:
            x = rand.randint(0,self.dim-1); y = rand.randint(0,self.dim-1)
            if self.board[x,y] != -1:
                self.placeMine(x,y)
                toBePlaced -= 1

    def __init__(self,dim,mines):
        self.dim = dim
        self.mines = mines
        self.board = np.zeros((dim,dim), dtype= int)
        self.userBoard = np.zeros((dim,dim), dtype= int)
        self.genBoard()
        
    def clearUserBoard(self):
        self.userBoard = np.zeros((self.dim,self.dim), dtype= int)


    def printBoard(self,boardType):
        """Prints board given the type to print

        Args:
            boardType (int): if 0 print actual board, if 1 print agent perspective
        """
        board = self.board if boardType == 0 else self.userBoard
        pltMap = {-1 : "M", 10 : "F", 9 : "v", 13 : "E"}
        for i in range(9): pltMap[i] = i
        
        plt.figure(figsize = (9,9))
        #colors = ["beige"]
        #colormap =  matplotlib.colors.ListedColormap(colors)
        plt.pcolor(board,edgecolors = "black", cmap = 'Set3', linewidths = 1)
        for (j,i),label in np.ndenumerate(board): #consider using a mapping for label to mine/flag
            plt.text(i,j,pltMap[label],ha='left',va='bottom')
        plt.tight_layout()
        #plt.gca().invert_yaxis()
        plt.show()