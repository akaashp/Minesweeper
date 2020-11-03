from Minesweeper import *
from Agent import *
from statistics import mean
import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer
import Agent_copy as a2

# to run improved agent Once
#dim = 30
#mines = int(dim**2 *.33333)
#temp = msBoard(dim,mines)
#start = timer()
#print("explosions: ", improvedAgent(temp), "mines: ",mines)
#end = timer()
#print("time: ", end-start)
#temp.printBoard(1)


mineDensity = np.arange(0.1,.91,.05)
successRate = np.zeros(len(mineDensity))
successRate2 = np.zeros(len(mineDensity))
for m in range(len(mineDensity)): #to generate all data
    currDensity = mineDensity[m]
    dim = 50; mines = int(dim**2 * currDensity)
    dim2 = 30; mines2 = int(dim2**2 * currDensity)
    resArr = np.zeros(10)
    
    print("CURRENT MINE DENSITY: ",currDensity)
    for i in range(10):
        temp = msBoard(dim,mines)
        #temp.printBoard(0) #print initial board
        resArr[i] = basicAgent(temp)
        print("Explosions: ",resArr[i], "Mines: ",mines)
        #temp.printBoard(1) #print final agent board
    
    temp2 = msBoard(dim2,mines2)
    successRate2[m] = 1 - improvedAgent(temp2)/mines2

    avSucc = 1- mean(resArr)/mines
    print (avSucc, " % success")
    successRate[m] = avSucc

plt.figure(figsize = (10,6))
colors = ["orange","cyan","purple"]
colormap =  matplotlib.colors.ListedColormap(colors)
plt.plot(mineDensity,successRate,label="Basic Agent")
plt.plot(mineDensity,successRate2,label = "Improved Agent")
plt.xticks(mineDensity)
plt.title("Average Success Rate vs Mine Density" )
plt.xlabel("Mine Density")
plt.ylabel("Average Success rate")
plt.legend()
plt.show()