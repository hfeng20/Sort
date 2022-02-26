




import tkinter as tk
import random
import matplotlib.backends.backend_tkagg
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import time
class GUI:
    def __init__(self):
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True

        self.root = tk.Tk()
        self.root.wm_title("Sorting Visualizer")

        plt.axes(xlim=(0, 2), ylim=(-2, 2))
        self.fig = plt.Figure(dpi=100)
        self.ax = self.fig.add_subplot(xlim=(0, 50), ylim=(0, 50))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        self.canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        self.quitButton = tk.Button(master=self.root, text="Quit", command=self.root.quit)
        self.quitButton.pack(side=tk.BOTTOM)

        self.showButton = tk.Button(master=self.root, text="Generate", command= lambda:array.show(self))
        self.showButton.pack(side=tk.BOTTOM)

        self.shuffleButton = tk.Button(master=self.root, text="Shuffle", command= lambda:array.shuffle(self))

        self.bubbleSortButton = tk.Button(master=self.root, text="Bubble Sort", command= lambda:array.BubbleSort(self))

        self.selectionSortButton = tk.Button(master=self.root, text="Selection Sort", command = lambda:array.SelectionSort(self))

        self.insertionSortButton = tk.Button(master=self.root, text="Insertion Sort", command = lambda:array.InsertionSort(self))

        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.lines = []
        
    def showShuffle(self):
        self.shuffleButton.pack(side=tk.BOTTOM)
        self.bubbleSortButton.pack_forget()
        self.selectionSortButton.pack_forget()
        self.insertionSortButton.pack_forget()

    def showSorts(self):
        self.shuffleButton.pack_forget()
        self.bubbleSortButton.pack(side=tk.BOTTOM)
        self.selectionSortButton.pack(side = tk.BOTTOM)
        self.insertionSortButton.pack(side = tk.BOTTOM)


    def graphRectangle(self, rect, col):
        xcoord = rect.x
        height = rect.height
        lines = [[[xcoord, 0],[xcoord, height]], [[xcoord, height], [xcoord + 1, height]], [[xcoord + 1, 0],[xcoord + 1, height]]]
        linesArray = []
        for line in lines:
            xs, ys = zip(*line)
            curLine = self.ax.plot(xs,ys,color = col)
            # print(self.ax.lines)
            linesArray.append(curLine)
            self.canvas.draw()
            self.root.update()
        self.lines.append(linesArray)
    
    def insertRectangle(self, rect, index, col):
        self.graphRectangle(rect, col)
        for i in range(3):
            self.ax.lines.insert(index * 3, self.ax.lines.pop(len(self.ax.lines) - 1))
    
    def removeRectangle(self, index):
        for i in range(3):
            self.ax.lines.pop(index * 3)
    
    def removeLastRectangle(self):
        for i in range(3):
            self.ax.lines.pop(len(self.ax.lines) - 1)

class Sort:
    def __init__(self,size):
        self.array = [i + 1 for i in range(size)]
        self.GUIArray = []
        for i in range(len(self.array)):
            self.GUIArray.append(GUIRectangle(self.array[i], i))
        self.inAction = False

    def show(self, gui):
        self.graphRectangles(gui)
        gui.showButton.pack_forget()
        gui.showShuffle()

    def shuffle(self, gui):
        if not self.inAction:
            self.inAction = True
            gui.fig.clear()
            gui.ax = gui.fig.add_subplot(xlim=(0, 50), ylim=(0, 50))
            random.shuffle(self.array)
            self.GUIArray = []
            for i in range(len(self.array)):
                self.GUIArray.append(GUIRectangle(self.array[i], i))
            self.graphRectangles(gui)
            self.inAction = False
            gui.showSorts()
        else:
            return
    def positionRectangle(self, gui, index, rect, col):
        self.array.insert(index, self.array.pop(self.array.index(rect.height)))
        self.GUIArray.insert(index, self.GUIArray.pop(self.GUIArray.index(rect)))
        gui.insertRectangle(rect, index, col)

    def InsertionSort(self, gui):
        if not self.inAction:
            self.inAction = True
            for i in range(len(self.array)):
                index = i
                for t in range(i):
                    if self.array[t] > self.array[i]:
                        index = t
                        break
                gui.removeRectangle(i)
                self.GUIArray[i].x = index
                for x in range(index, i):
                    self.GUIArray[x].x += 1
                    gui.removeRectangle(x)
                    gui.insertRectangle(self.GUIArray[x],, "green")
                self.positionRectangle(gui, index, self.GUIArray[i], "green")
                gui.canvas.draw()
            self.inAction = False
        else:
            return

    def SelectionSort(self, gui):
        if not self.inAction:
            self.inAction = True
            for i in range(len(self.array)):
                cur = self.GUIArray[i]
                gui.graphRectangle(cur, "red")
                minimum = self.array[i]
                for t in range(i + 1, len(self.array)):
                    if self.array[t] < minimum:
                        minimum = self.array[t]
                if minimum == self.array[i]:
                    gui.removeRectangle(i)
                    gui.removeLastRectangle()
                    gui.insertRectangle(self.GUIArray[i], i, "green")
                    time.sleep(0.5)
                    gui.canvas.draw()
                else:
                    minRect = self.GUIArray[self.array.index(minimum)]
                    gui.graphRectangle(minRect, "red")
                    gui.removeLastRectangle()
                    gui.removeLastRectangle()
                    time.sleep(0.5)
                    self.swap(gui, cur, minRect, "blue", "green")
                    gui.canvas.draw()
            self.inAction = False
        else:
            return
        gui.showShuffle()

    def BubbleSort(self, gui):
        if not self.inAction:
            self.inAction = True
            swaps = 1
            iteration = 0
            while swaps != 0:
                swaps = 0
                for i in range(len(self.array) - 1 - iteration):
                    cur = self.GUIArray[i]
                    right = self.GUIArray[i+1]
                    gui.graphRectangle(cur, "red")
                    gui.graphRectangle(right, "red")
                    if right.height < cur.height:
                        gui.removeLastRectangle()
                        gui.removeLastRectangle()
                        swaps += 1
                        self.swap(gui, cur, right, "blue", "blue")
                    else:
                        gui.removeLastRectangle()
                        gui.removeLastRectangle()
                    gui.canvas.draw()
                    gui.root.update()
                iteration += 1
            self.inAction = False
        else:
            return
        gui.showShuffle()
        

    def swap(self, gui, rect1, rect2, col1, col2):
        temp = rect1.x
        rect1.x = rect2.x
        rect2.x = temp
        self.GUIArray[rect2.x] = rect2
        self.GUIArray[rect1.x] = rect1
        self.array[rect2.x] = rect2.height
        self.array[rect1.x] = rect1.height
        index1 = rect1.x
        index2 = rect2.x
        if(index1 < index2):
            gui.removeRectangle(index2)
            gui.removeRectangle(index1)
            
        else:
            gui.removeRectangle(index1)
            gui.removeRectangle(index2)
        gui.graphRectangle(rect1, col1)
        gui.graphRectangle(rect2, col2)
        for i in range(3):
            gui.ax.lines.insert(index2 * 3, gui.ax.lines.pop(len(gui.ax.lines) - 1))
        for i in range(3):
            gui.ax.lines.insert(index1 * 3, gui.ax.lines.pop(len(gui.ax.lines) - 1))
            



    def graphRectangles(self, gui):
        gui.fig.clear()
        gui.ax = gui.fig.add_subplot(xlim=(0, 50), ylim=(0, 50))
        for rectangle in self.GUIArray:
            gui.graphRectangle(rectangle, "blue")
        


        

class GUIRectangle:
    def __init__(self, height, x):
        self.x = x
        self.height = height
        self.width = 1


array = Sort(10)

GUI = GUI()
tk.mainloop()