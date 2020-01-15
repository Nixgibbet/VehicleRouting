
import tkinter as tk
import tkinter.filedialog
from tkinter.filedialog import askopenfilenames
import os
import json as js
import numpy as np
import matplotlib.pyplot as plt
import ast
import scipy
from matplotlib.widgets import Button
import seaborn as sns
import random
import matplotlib.gridspec as gridspec
from scipy.stats import linregress





coord =[]
tour=[]
tourcost = []
phero = []
X = []
best=0

plt.figure(figsize=(80, 80))

plt.subplot(2,2,1)
plt.title('Pheromones')
plt.subplot(2,2,2)
plt.title('Tourplot')
plt.subplot(2,2,(3,4))
plt.title('Average Tourcost')

plt.subplots_adjust(bottom=0.2)

plt.ioff()

class Index(object):
    ind = 0

    def next(self, event):
        self.ind += 1
        i = self.ind % len(phero)

        plt.subplot(2,2,1)
        plt.cla()
        plt.imshow(phero[self.ind], cmap="Blues", interpolation='nearest')
        plt.title('Phermones Gen_'+str(self.ind))
        plt.draw()

        Index.plotTour([tour[self.ind]],coord,self.ind)


    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(phero)
        plt.subplot(2,2,1)
        plt.cla()
        plt.imshow(phero[self.ind], cmap="Blues", interpolation='nearest')
        plt.title('Phermones Gen_'+str(self.ind))  
    
        Index.plotTour([tour[self.ind]],coord,self.ind)

        plt.draw()



    def getProb(prob):
        global coord
        global best
        coord.clear()
        best=0
        dirname = os.listdir("../data")
        for probs in dirname:
            if probs[0:len(probs)-5] == prob:
                #print(True)
                jsonfile="../data" + "/"+ probs
                with open(jsonfile, 'r') as f:
                    data = f.read()
                    jsondata = js.loads(data)
                    coord.append((jsondata["node_coordinates"]))
                    best = jsondata["Optimal_value"]
                    coord = coord[0]


    def plotTour(tours,coords,count):
        coordX = []
        coordY = []
      #  print("Anfang:" +str(coords))
            
        for node in coords:
            coordX.append(node[0])
            coordY.append(node[1])


        toursX = []
        toursY = []
        for tour in tours:
            # print(tour)
            tourNodesX = []
            tourNodesY = []

            for node in tour:
                tourNodesX.append(coords[node][0])
                tourNodesY.append(coords[node][1])

            toursX.append(tourNodesX)
            toursY.append(tourNodesY)



        plt.subplot(2,2,2)
        plt.cla()
        plt.scatter(coords[0][0], coords[0][1], s=200, color='green', label="Depot")

        for x in range(1, len(coords)):
            plt.scatter(coords[x][0],coords[x][1], color="gold")
            plt.annotate(str("#" + str(x)), (coords[x][0],coords[x][1]))


        for i in range(len(toursX)):
            # print("#" + str(i) + str(toursX[i]) + "/" + str(toursY[i]))
            plt.plot(toursX[i], toursY[i], color=np.random.rand(3,), label="Tour #" + str(i))

        plt.title('Tourplot Gen_'+str(count))
        plt.draw()
    

    def minix():
        indiz = 1
        for avgs in tourcost:            
            indiz += 1
            if avgs==min(tourcost): 
              #  print("Minimum at: "+str(indiz)+" : "+str(min(tourcost)))
                return indiz-2

    def goto(self,event):
        plt.subplot(2,2,1)
        plt.cla()
        plt.imshow(phero[Index.minix()], cmap="Blues", interpolation='nearest')
        plt.title('Phermones Gen_'+str(Index.minix()))

        Index.plotTour([tour[Index.minix()]],coord,Index.minix())

        plt.draw()

    def norm(matrix):
        
    #     for zeile in Matrix:
    #         for spalte in Matrix:
    #             matrix[][]
    #   #  print(type(matrix))
        


        return matrix


    def plotTourcost():
        X=range(len(tourcost))
        b, a, r, p, std = linregress(X,tourcost)
        plt.subplot(2,2,(3,4))
        plt.cla()
        plt.plot(X, tourcost, color="black")
        plt.plot([0,len(tourcost)],[a,a+len(tourcost)*b],c="red",alpha=0.5,lineWidth = 3)
        plt.scatter(Index.minix(), min(tourcost), c="green",linewidths= 3)
        plt.vlines(x=Index.minix(), ymin = 0, ymax = min(tourcost) ,color="green",linestyle='-')
        plt.hlines(min(tourcost),xmin=0, xmax= Index.minix(),colors="green")
        plt.hlines(best,xmin=0, xmax=len(X), colors="orange")
        plt.title('Tourcost')

    def readjson(self, event):    
        global tourcost
        global phero
        global tour
        global X

        tourcost.clear()
        phero.clear()
        tour.clear()

    

        dirname = tk.filedialog.askdirectory(initialdir="/",  title='Please select a directory')
        dirlist = os.listdir(dirname)        
        prob=dirname[:dirname.index("-")].split('/')[-1]
        plt.suptitle(str(prob), fontsize=16)
        Index.getProb(prob)

        
        i=0
        for json in dirlist:
            i+=1
            jsonfile=dirname + "/"+ json
            if json:
                with open(jsonfile, 'r') as f:
                    data = f.read()
                    jsondata = js.loads(data)
                    tourcost.append(jsondata["tourCost"][0])
                    phero.append(jsondata["pheromons"])
                    tour.append(jsondata["antTour"][0])
        #Plot Pheros
        plt.subplot(2,2,1)
        plt.imshow(Index.norm(np.asmatrix(phero[0])), cmap="Blues", interpolation='nearest')
        plt.title('Pheromones Gen_0')

       
        # print("GEILER SCHEIß PHEEEEEEEEEEEEERO")
        # for lenas in phero:
        #     print(lenas)
        # print("IS KLAR DIGGA VADDA")

        # i=0
        # for cost in tourcost:
        #     print("Indizie: "+str(i)+":"+ str(cost))
        #     i=i+1




        #Plot Tourcost
        Index.plotTourcost()

        #Plot Graph
        Index.plotTour([tour[0]],coord,0)

        plt.draw()
        

  
        
                




    
                



    

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
axsel = plt.axes([0.5, 0.05, 0.1, 0.075])
axgoto = plt.axes([0.2, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)
bsel = Button(axsel,'Select Data')
bsel.on_clicked(callback.readjson)
bgoto = Button(axgoto,'Goto Minimum')
bgoto.on_clicked(callback.goto)

        

plt.show()