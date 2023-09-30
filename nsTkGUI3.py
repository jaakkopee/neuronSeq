# ... (previous code)
import networkx as nx
import math
import numpy as np
import tkinter as tk
import neuronSeq2 as ns
import threading
import time

running = True
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
        note.set_activation_function(1) #sigmoid
        G.DVpos[note.get_id()] = distance_vector

        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)

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
        nnotedict = {}
        for nnote in neuronSeq.nnotes:
            nnotedict[nnote.id] = nnote

        source = nnotedict[self.source_entry.get()]
        target = nnotedict[self.target_entry.get()]
        weight0 = float(self.weight0_entry.get())
        weight1 = float(self.weight1_entry.get())
        source_idx = neuronSeq.nnotes.index(source)
        target_idx = neuronSeq.nnotes.index(target)
        connection, distance_vectors = G.add_connection(connection_name, source_idx, target_idx, weight0, weight1)
        G.DVpos[connection.get_id()] = distance_vectors
        print_neuronSeq_connections()
        
        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+" "+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)
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


class NetworkCanvas(tk.Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.zoom_factor = 10.0
        self.pan_offset = [400, 400]

    def set_edge_color(self, edge_color):
        tk_rgb = "#%02x%02x%02x" % edge_color
        self.edge_color = tk_rgb

    def set_node_color(self, node_color):
        tk_rgb = "#%02x%02x%02x" % node_color
        self.node_color = tk_rgb

    def get_rgb(self, w01, w10, total_activation):
        random_factor = np.random.uniform(0.0, 1.0)
        color = int (random_factor * total_activation * 255)
        if color > 255:
            color = 255
        if color < 0:
            color = 0
        if w01 > 0 and w10 > 0:
            rgb = (color, 0, 0)
        elif w01 < 0 and w10 < 0:
            rgb = (0, 0, color)
        elif w01 > 0 and w10 < 0:
            rgb = (0, color, 0)
        elif w01 < 0 and w10 > 0:
            rgb = (color, color, 0)
        elif w01 == 0 and w10 == 0:
            rgb = (0, 0, 0)
        elif w01 == 0 and w10 > 0:
            rgb = (color, 0, color)
        elif w01 == 0 and w10 < 0:
            rgb = (0, color, color)
        elif w01 > 0 and w10 == 0:
            rgb = (color, color, color)
        elif w01 < 0 and w10 == 0:
            rgb = (color, color, color)

        return rgb
    
    def update_canvas(self):
        zoom_factor = self.zoom_factor
        pan_offset = self.pan_offset
        global width, height
        global G
        self.delete('all')
        for connection in neuronSeq.connections:
            source = connection.source
            target = connection.destination
            source_pos = G.DVpos[source.get_id()]
            target_pos = G.DVpos[target.get_id()]
            source_x = source_pos.get_coordinates()[0] * zoom_factor + pan_offset[0]
            source_y = source_pos.get_coordinates()[1] * zoom_factor + pan_offset[1]
            target_x = target_pos.get_coordinates()[0] * zoom_factor + pan_offset[0]
            target_y = target_pos.get_coordinates()[1] * zoom_factor + pan_offset[1]
            text_x = (source_x + target_x) / 2
            text_y = (source_y + target_y) / 2
            total_activation = source.activation + target.activation
            self.set_edge_color(self.get_rgb(connection.weight_0_to_1, connection.weight_1_to_0, total_activation))
            self.create_line(source_x, source_y, target_x, target_y, fill=self.edge_color, width=3)
            self.create_text(text_x, text_y, text=connection.get_id())

        for nnote in neuronSeq.nnotes:
            node_color = int(nnote.activation * 255)
            rgb = (node_color, node_color, node_color)
            self.set_node_color(rgb)
            pos = G.DVpos[nnote.get_id()]
            x = pos.get_coordinates()[0] * zoom_factor + pan_offset[0]
            y = pos.get_coordinates()[1] * zoom_factor + pan_offset[1]
            self.create_oval(x-9, y-9, x+9, y+9, fill=self.node_color)
            self.create_text(x, y-13, text=nnote.get_id())
        self.update()
        return

def openEditNeuronWindow(nnote):
    global editNeuronWindow, neuronSeq_window
    editNeuronWindow=EditNeuronWindow(neuronSeq_window, nnote)
    return

class EditNeuronWindow(tk.Toplevel):
    def __init__(self, master, nnote):
        super().__init__(master)
        self.title("Edit Neuron")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master = master
        self.nnote = nnote
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        self.neuron_name_label = tk.Label(self, text="Neuron Name")
        self.neuron_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.neuron_name_entry = tk.Entry(self)
        #set initial value
        self.neuron_name_entry.insert(0, self.nnote.id)

        self.neuron_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.midi_channel_label = tk.Label(self, text="MIDI Channel")
        self.midi_channel_label.grid(row=1, column=0, padx=10, pady=10)
        self.midi_channel_entry = tk.Entry(self)
        #set initial value
        self.midi_channel_entry.insert(0, self.nnote.channel)

        self.midi_channel_entry.grid(row=1, column=1, padx=10, pady=10)
        self.midi_note_label = tk.Label(self, text="MIDI Note")
        self.midi_note_label.grid(row=2, column=0, padx=10, pady=10)
        self.midi_note_entry = tk.Entry(self)
        #set initial value
        self.midi_note_entry.insert(0, self.nnote.note)

        self.midi_note_entry.grid(row=2, column=1, padx=10, pady=10)
        self.velocity_label = tk.Label(self, text="Velocity")
        self.velocity_label.grid(row=3, column=0, padx=10, pady=10)
        self.velocity_entry = tk.Entry(self)
        #set initial value
        self.velocity_entry.insert(0, self.nnote.velocity)

        self.velocity_entry.grid(row=3, column=1, padx=10, pady=10)
        self.duration_label = tk.Label(self, text="Duration")
        self.duration_label.grid(row=4, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(self)
        #set initial value
        self.duration_entry.insert(0, self.nnote.duration)

        self.duration_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_button = tk.Button(self, text="Update", command=self.update_neuron)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

    def update_neuron(self):
        global G
        neuron_name = self.neuron_name_entry.get()
        midi_channel = int(self.midi_channel_entry.get())
        midi_note = int(self.midi_note_entry.get())
        velocity = int(self.velocity_entry.get())
        duration = float(self.duration_entry.get())
        nnote_idx = neuronSeq.nnotes.index(self.nnote)
        note, dvs = G.update_nnote(nnote_idx, midi_channel=midi_channel, midi_note=midi_note, duration=duration, id=neuron_name, velocity=velocity, lenX=2**16)
        note.set_activation_function(1) #sigmoid

        #update the nn_conn_label
        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+" "+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)

        print_neuronSeq_nnotes()
        self.close_window()
        return

def openEditConnectionWindow(connection):
    global editConnectionWindow, neuronSeq_window
    editConnectionWindow=EditConnectionWindow(neuronSeq_window, connection)
    return

class EditConnectionWindow(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("Edit Connection")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master = master
        self.connection = connection
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        connection_name_label = tk.Label(self, text="Connection Name")
        connection_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.connection_name_entry = tk.Entry(self)
        #set initial value
        self.connection_name_entry.insert(0, self.connection.name)

        self.connection_name_entry.grid(row=0, column=1, padx=10, pady=10)
        source_label = tk.Label(self, text="Source")
        source_label.grid(row=1, column=0, padx=10, pady=10)
        self.source_entry = tk.Entry(self)
        #set initial value
        self.source_entry.insert(0, self.connection.source.id)

        self.source_entry.grid(row=1, column=1, padx=10, pady=10)
        target_label = tk.Label(self, text="Target")
        target_label.grid(row=2, column=0, padx=10, pady=10)
        self.target_entry = tk.Entry(self)
        #set initial value
        self.target_entry.insert(0, self.connection.destination.id)

        self.target_entry.grid(row=2, column=1, padx=10, pady=10)
        self.weight0_label = tk.Label(self, text="Weight 0")
        self.weight0_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight0_entry = tk.Entry(self)
        #set initial value
        self.weight0_entry.insert(0, self.connection.weight_0_to_1)

        self.weight0_entry.grid(row=3, column=1, padx=10, pady=10)
        self.weight1_label = tk.Label(self, text="Weight 1")
        self.weight1_label.grid(row=4, column=0, padx=10, pady=10)
        self.weight1_entry = tk.Entry(self)
        #set initial value
        self.weight1_entry.insert(0, self.connection.weight_1_to_0)

        self.weight1_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_connection_button = tk.Button(self, text="Update", command=self.update_connection)
        self.add_connection_button.grid(row=5, column=0, padx=10, pady=10)

    def update_connection(self):
        global G
        connection_name = self.connection_name_entry.get()
        nnotedict = {}
        for nnote in neuronSeq.nnotes:
            nnotedict[nnote.id] = nnote

        source = nnotedict[self.source_entry.get()]
        target = nnotedict[self.target_entry.get()]
        weight0 = float(self.weight0_entry.get())
        weight1 = float(self.weight1_entry.get())
        source_idx = neuronSeq.nnotes.index(source)
        target_idx = neuronSeq.nnotes.index(target)
        connection_idx = neuronSeq.connections.index(self.connection)
        connection, distance_vectors = G.update_connection(connection_idx, connection_name, source_idx, target_idx, weight0, weight1)
        print_neuronSeq_connections()
        
        nn_conn_str="Neurons:\n"
        for nnote in neuronSeq.nnotes:
            nn_conn_str += str(nnote.id) + ": " + str(nnote.channel) + " " + str(nnote.note) + " " + str(nnote.velocity) + " " + str(nnote.duration) + "\n"
        nn_conn_str += "\nConnections:\n"
        for connection in neuronSeq.connections:
            nn_conn_str += str(connection.name) + ": " + str(connection.source.id) + "->" + str(connection.destination.id) + str(connection.weight_0_to_1)+" "+str(connection.weight_1_to_0)+"\n"
        self.master.nn_conn_label.config(text=nn_conn_str)
        self.close_window()
        return
    
def openAddModulatorWindow():
    global addModulatorWindow, neuronSeq_window
    addModulatorWindow=AddModulatorWindow(neuronSeq_window)
    return

class AddModulatorWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Modulator")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master = master
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        #create dropdown menu with modulator names
        self.modulator_name_label = tk.Label(self, text="Modulator Name")
        self.modulator_name_label.grid(row=0, column=0, padx=10, pady=10)
        variable = tk.StringVar(self)
        variable.set("NNoteVelocitySineModulator") # default value
        self.modulator_name_entry = tk.OptionMenu(self, variable, "NNoteVelocitySineModulator", "NNoteDurationSineModulator", "NNoteNoteSineModulator", "ConnectionWeight0to1SineModulator", "ConnectionWeight1to0SineModulator")
        self.modulator_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.nnote_label = tk.Label(self, text="Neuron or Connection Name")
        self.nnote_label.grid(row=1, column=0, padx=10, pady=10)
        self.nnote_entry = tk.Entry(self)
        self.nnote_entry.grid(row=1, column=1, padx=10, pady=10)
        self.add_button = tk.Button(self, text="Add", command=lambda: self.add_modulator(variable))
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

    def add_modulator(self, variable):
        global G
        modulator_name = variable.get()
        if modulator_name == "NNoteVelocitySineModulator":
            nnote = G.get_nnote_by_id(self.nnote_entry.get())
            modulator = ns.NNoteVelocitySineModulator(nnote, self.master, neuronSeq)
        elif modulator_name == "NNoteDurationSineModulator":
            nnote = G.get_nnote_by_id(self.nnote_entry.get())
            modulator = ns.NNoteDurationSineModulator(nnote, self.master, neuronSeq)
        elif modulator_name == "NNoteNoteSineModulator":
            nnote = G.get_nnote_by_id(self.nnote_entry.get())
            modulator = ns.NNoteNoteSineModulator(nnote, self.master, neuronSeq)
        elif modulator_name == "ConnectionWeight0to1SineModulator":
            connection = G.get_connection_by_id(self.nnote_entry.get())
            modulator = ns.ConnectionWeight0To1SineModulator(connection, self.master, neuronSeq)
        elif modulator_name == "ConnectionWeight1to0SineModulator":
            modulator = ns.ConnectionWeight1To0SineModulator(connection, self.master, neuronSeq)
        neuronSeq.modulators.append(modulator)
        modulator.start()
        self.close_window()
        return

    
class NeuronSeqWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("NeuronSeq")
        self.geometry("1024x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.create_widgets()
        self.bind('<Key>', self.key_press)
        self.bind('<Button-1>', self.mouse_hit)
        self.pan_offset = self.network_canvas.pan_offset
        self.zoom_factor = self.network_canvas.zoom_factor
        self.vector_length = 0.1

    def mouse_hit(self, event):
        #find the closest node
        global G
        x = (event.x - self.pan_offset[0]) / self.zoom_factor
        y = (event.y - self.pan_offset[1]) / self.zoom_factor

        closest_node = None
        closest_node_distance = 5
        for nnote in neuronSeq.nnotes:
            pos = G.DVpos[nnote.get_id()]
            distance = math.sqrt((pos.get_coordinates()[0] - x)**2 + (pos.get_coordinates()[1] - y)**2)
            if distance < closest_node_distance:
                closest_node = nnote
                openEditNeuronWindow(closest_node)


        #find the closest connection
        closest_connection = None
        closest_connection_distance = 8
        for connection in neuronSeq.connections:
            source = connection.source
            target = connection.destination
            source_pos = G.DVpos[source.get_id()]
            target_pos = G.DVpos[target.get_id()]
            source_x = source_pos.get_coordinates()[0] * self.zoom_factor + self.pan_offset[0]
            source_y = source_pos.get_coordinates()[1] * self.zoom_factor + self.pan_offset[1]
            target_x = target_pos.get_coordinates()[0] * self.zoom_factor + self.pan_offset[0]
            target_y = target_pos.get_coordinates()[1] * self.zoom_factor + self.pan_offset[1]
            text_x = (source_x + target_x) / 2
            text_y = (source_y + target_y) / 2
            distance = math.sqrt((text_x - event.x)**2 + (text_y - event.y)**2)
            if distance < closest_connection_distance:
                closest_connection = connection
                openEditConnectionWindow(closest_connection)
        return
    

    def create_widgets(self):
        global openAddNeuronWindow, openAddConnectionWindow, print_neuronSeq_nnotes, print_neuronSeq_connections

        self.network_canvas = NetworkCanvas(self, width=800, height=800)
        self.network_canvas.grid(row=0, column=0, padx=10, pady=10)

        self.add_neuron_button = tk.Button(self, text="Add Neuron", command=openAddNeuronWindow)
        self.add_neuron_button.grid(row=0, column=1, padx=10, pady=10)

        self.add_connection_button = tk.Button(self, text="Add Connection", command=openAddConnectionWindow)
        self.add_connection_button.grid(row=0, column=2, padx=10, pady=10)

        self.add_modulator_button = tk.Button(self, text="Add Modulator", command=openAddModulatorWindow)
        self.add_modulator_button.grid(row=0, column=3, padx=10, pady=10)

        self.nn_conn_label = tk.Label(self, text="Neurons:\n\nConnections:\n")
        self.nn_conn_label.grid(row=0, column=4, padx=10, pady=10)

        return
    

    def key_press(self, event):
        # Handle key presses for zoom and pan
        # Update the canvas based on key presses
        global G

        if event.char == 'z':
            self.zoom_factor += 0.1
            self.network_canvas.zoom_factor = self.zoom_factor

        elif event.char == 'Z':
            self.zoom_factor -= 0.1
            self.network_canvas.zoom_factor = self.zoom_factor

        elif event.char == 'w':
            self.pan_offset[1] -= 10
            self.network_canvas.pan_offset = self.pan_offset

        elif event.char == 's':
            self.pan_offset[1] += 10
            self.network_canvas.pan_offset = self.pan_offset

        elif event.char == 'a':
            self.pan_offset[0] -= 10
            self.network_canvas.pan_offset = self.pan_offset

        elif event.char == 'd':
            self.pan_offset[0] += 10
            self.network_canvas.pan_offset = self.pan_offset

        elif event.char == 'r':
            G.rotate(0.001)

        elif event.char == 'R':
            G.rotate(-0.001)

        elif event.char == 't':
            G.position_nodes_circle()

        elif event.char == 'T':
            G.position_nodes_random()

        elif event.char == 'y':
            G.position_nodes_grid()

        else:
            return

        return


    def close_window(self):
        global running
        running = False
        global neuronSeq
        neuronSeq.stop()
        time.sleep(0.1)
        self.destroy()

class NetworkRunner:
    def __init__(self, neuronSeq_window):
        global width, height
        global G
        global zoom_factor, pan_offset
        self.neuronSeq_window = neuronSeq_window
        self.canvas = neuronSeq_window.network_canvas

    def update(self):
        global running
        global width, height
        global G
        global zoom_factor, pan_offset
        if running:
            self.canvas.update_canvas()
            self.neuronSeq_window.after(10, self.update)
        return

neuronSeq_window = NeuronSeqWindow()
network_runner = NetworkRunner(neuronSeq_window)
network_runner.update()
neuronSeq_window.mainloop()
