#import pygame
import networkx as nx
import math
import numpy as np
import tkinter as tk
import neuronSeq2 as ns
import threading
import time

running = True   
width, height = 800, 600
neuronSeq = ns.NeuronSeq()
G = ns.NetworkGraph(neuronSeq)

def print_neuronSeq_nnotes():
    print("Neurons:")
    for nnote in neuronSeq.nnotes:
        print(nnote.id, nnote.channel, nnote.note, nnote.velocity, nnote.duration)
    return

def print_neuronSeq_connections():
    print("Connections:")
    for connection in neuronSeq.connections:
        print(connection.name, connection.source.id + "->" + connection.destination.id, connection.weight_0_to_1, connection.weight_1_to_0)
    return

class AddNeuronWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Neuron")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.nwr = master.nwr
        self.master = master
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        self.neuron_name_label = tk.Label(self, text="Neuron Name")
        self.neuron_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.neuron_name_entry = tk.Entry(self)
        self.neuron_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.midi_channel_label = tk.Label(self, text="MIDI Channel")
        self.midi_channel_label.grid(row=1, column=0, padx=10, pady=10)
        self.midi_channel_entry = tk.Entry(self)
        self.midi_channel_entry.grid(row=1, column=1, padx=10, pady=10)
        self.midi_note_label = tk.Label(self, text="MIDI Note")
        self.midi_note_label.grid(row=2, column=0, padx=10, pady=10)
        self.midi_note_entry = tk.Entry(self)
        self.midi_note_entry.grid(row=2, column=1, padx=10, pady=10)
        self.velocity_label = tk.Label(self, text="Velocity")
        self.velocity_label.grid(row=3, column=0, padx=10, pady=10)
        self.velocity_entry = tk.Entry(self)
        self.velocity_entry.grid(row=3, column=1, padx=10, pady=10)
        self.duration_label = tk.Label(self, text="Duration")
        self.duration_label.grid(row=4, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_button = tk.Button(self, text="Add", command=self.add_neuron)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)
        
    def add_neuron(self):
        global G
        neuron_name = self.neuron_name_entry.get()
        midi_channel = int(self.midi_channel_entry.get())
        midi_note = int(self.midi_note_entry.get())
        velocity = int(self.velocity_entry.get())
        duration = float(self.duration_entry.get())
        note, distance_vector = G.add_nnote(midi_channel=midi_channel, note=midi_note, duration=duration, id=neuron_name, velocity=velocity, lenX=2**16)
        note.set_activation_function(1)
        G.DVpos[note.get_id()] = distance_vector

        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)

        self.nwr.canvas.delete('all')
        self.nwr.update(None)

        print_neuronSeq_nnotes()
        self.close_window()
        return
    
class AddConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Connection")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.nwr = master.nwr
        self.master = master
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        connection_name_label = tk.Label(self, text="Connection Name")
        connection_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.connection_name_entry = tk.Entry(self)
        self.connection_name_entry.grid(row=0, column=1, padx=10, pady=10)
        source_label = tk.Label(self, text="Source")
        source_label.grid(row=1, column=0, padx=10, pady=10)
        self.source_entry = tk.Entry(self)
        self.source_entry.grid(row=1, column=1, padx=10, pady=10)
        target_label = tk.Label(self, text="Target")
        target_label.grid(row=2, column=0, padx=10, pady=10)
        self.target_entry = tk.Entry(self)
        self.target_entry.grid(row=2, column=1, padx=10, pady=10)
        self.weight0_label = tk.Label(self, text="Weight 0")
        self.weight0_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight0_entry = tk.Entry(self)
        self.weight0_entry.grid(row=3, column=1, padx=10, pady=10)
        self.weight1_label = tk.Label(self, text="Weight 1")
        self.weight1_label.grid(row=4, column=0, padx=10, pady=10)
        self.weight1_entry = tk.Entry(self)
        self.weight1_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_connection_button = tk.Button(self, text="Add", command=self.add_connection)
        self.add_connection_button.grid(row=5, column=0, padx=10, pady=10)

    def add_connection(self):
        global G
        connection_name = self.connection_name_entry.get()
        source = int(self.source_entry.get())
        target = int(self.target_entry.get())
        weight0 = float(self.weight0_entry.get())
        weight1 = float(self.weight1_entry.get())
        connection, distance_vectors = G.add_connection(connection_name, source, target, weight0, weight1)
        G.DVpos[connection.get_id()] = distance_vectors
        print_neuronSeq_connections()
        
        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+" "+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)

        self.nwr.canvas.delete('all')
        self.nwr.update(None)
        self.close_window()
        return

def openAddNeuronWindow():
    global addNeuronWindow, neuronSeq_window
    addNeuronWindow=AddNeuronWindow(neuronSeq_window)
    return

def openAddConnectionWindow():
    global addConnectionWindow, neuronSeq_window
    addConnectionWindow=AddConnectionWindow(neuronSeq_window)
    return

class NeuronSeqWindow(tk.Tk):
    def __init__(self, nwr=None):
        tk.Tk.__init__(self)
        self.nwr = nwr
        self.nwr.set_master(self)
        self.bind('<Key>', self.nwr.update)
        self.title("NeuronSeq")
        self.geometry("1024x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.create_widgets()

    def close_window(self):
        global running
        running = False
        global neuronSeq
        neuronSeq.stop()
        time.sleep(0.1)    
        self.destroy()

    def create_widgets(self):
        global openAddNeuronWindow, openAddConnectionWindow, print_neuronSeq_nnotes, print_neuronSeq_connections
        
        self.add_neuron_button = tk.Button(self, text="Add Neuron", command=openAddNeuronWindow)
        self.add_neuron_button.grid(row=0, column=0, padx=10, pady=10)
        self.add_connection_button = tk.Button(self, text="Add Connection", command=openAddConnectionWindow)
        self.add_connection_button.grid(row=1, column=0, padx=10, pady=10)
        self.nn_conn_label = tk.Label(self, text="Add neurons and connections to start.")
        self.nn_conn_label.grid(row=0, column=4, rowspan=3, padx=10, pady=10)
        self.nwr.update(None)
        return

class NetworkRunner:
    def __init__(self):
        global width, height
        global G
        global zoom_factor, pan_offset
        self.canvas = None

    def set_master(self, nsw):
        canvas = tk.Canvas(nsw, width=width, height=height)
        canvas.grid(row=4, column=0, columnspan=8, padx=10, pady=10)
        self.canvas = canvas

    def update(self, event):
        global zoom_factor
        global pan_offset
        global width, height
        global G

        if event is not None:
            # Handle events
            if event.keysym == 'plus':
                zoom_factor += 10.0
            elif event.keysym == 'minus':
                zoom_factor -= 10.0
            elif event.keysym == 'Left':
                pan_offset[0] -= 20
            elif event.keysym == 'Right':
                pan_offset[0] += 20
            elif event.keysym == 'Up':
                pan_offset[1] -= 20
            elif event.keysym == 'Down':
                pan_offset[1] += 20
            elif event.keysym == 'r':
                for nnote in neuronSeq.nnotes:
                    G.DVpos[nnote.get_id()] = ns.rotate_graph(G.DVpos[nnote.get_id()], 10)
                for connection in neuronSeq.connections:
                    dvs = G.DVpos[connection.get_id()]
                    dvs[0] = ns.rotate_graph(dvs[0], 10)
                    dvs[1] = ns.rotate_graph(dvs[1], 10)

        # Clear screen
        self.canvas.delete('all')

        # Draw edges and nodes
        for connection in neuronSeq.connections:
            dvs = G.DVpos[connection.get_id()]
            x1, y1 = dvs[0].get_coordinates()
            x2, y2 = dvs[1].get_coordinates()
            x1 = x1 * zoom_factor + width / 2 + pan_offset[0]
            y1 = y1 * zoom_factor + height / 2 + pan_offset[1]
            x2 = x2 * zoom_factor + width / 2 + pan_offset[0]
            y2 = y2 * zoom_factor + height / 2 + pan_offset[1]
            self.canvas.create_line(x1, y1, x2, y2, fill='black', width=5)

        # Draw nodes
        for nnote in neuronSeq.nnotes:
            x, y = G.DVpos[nnote.get_id()].get_coordinates()
            x = x * zoom_factor + width / 2 + pan_offset[0]
            y = y * zoom_factor + height / 2 + pan_offset[1]
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill='blue')



# Initial values for zoom and pan
zoom_factor = 1.0
pan_offset = [0, 0]

network_runner = NetworkRunner()
neuronSeq_window = NeuronSeqWindow(network_runner)

neuronSeq_window.mainloop()