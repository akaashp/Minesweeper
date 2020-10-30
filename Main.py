from Minesweeper import *
from Agent import *
from statistics import mean
import numpy as np
from matplotlib import pyplot as plt


mineDensity = np.arange(0.1,.91,.05)
successRate = np.zeros(len(mineDensity))
for m in range(len(mineDensity)):
    currDensity = mineDensity[m]
    dim = 50; mines = int(dim**2 * currDensity)
    resArr = np.zeros(10)
    print("CURRENT MINE DENSITY: ",currDensity)
    for i in range(10):
        temp = msBoard(dim,mines)
        #temp.printBoard(0)
        resArr[i] = basicAgent(temp)
        print("Explosions: ",resArr[i], "Mines: ",mines)
        #temp.printBoard(1)

    avSucc = 1- mean(resArr)/mines
    print (avSucc, " % success")
    successRate[m] = avSucc

plt.figure(figsize = (10,6))
colors = ["orange","cyan","purple"]
colormap =  matplotlib.colors.ListedColormap(colors)
plt.plot(mineDensity,successRate,label="Basic Agent")
#plt.plot(qVals,A2Successes,label="Approach 2: Adaptive A*")
#plt.plot(qVals,A3Successes,label="Approach 3: HUPSAA")
plt.xticks(mineDensity)
plt.title("Average Success Rate vs Mine Density" )
plt.xlabel("Mine Density")
plt.ylabel("Average Success rate")
plt.legend()
plt.show()
