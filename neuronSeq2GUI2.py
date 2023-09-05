#graphical user interface for neuronSeq2

# import libraries
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import neuronSeq2 as ns2

#main window class with connection creation form and graph window
#main window class
class NSGUIMainWindow:
    #constructor
    def __init__(self, master, ns):
        #initialize main window
        self.master = master
        master.title("NeuronSeq2")
        master.geometry("1000x600")
        master.resizable(False, False)
        #initialize connection creation form
        self.connectionCreationForm = NSGUIConnectionCreationForm(self.master)
        #initialize graph window
        self.graphWindow = NSGUIGraphWindow(self.master)
        #initialize connection list
        self.connectionList = []
        #initialize connection counter
        self.connectionCounter = 0
        #initialize connection dictionary
        self.connectionDict = {}
        self.ns = ns

    #add connection to connection list
    def addConnection(self, connection):
        self.connectionList.append(connection)
        self.connectionCounter += 1
        self.connectionDict[connection] = self.connectionCounter
        self.ns.add_connection(connection)

    #remove connection from connection list
    def removeConnection(self, connection):
        self.connectionList.remove(connection)
        self.connectionDict.pop(connection)
        self.ns.remove_connection(connection)