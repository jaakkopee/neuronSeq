#graphical user interface for neuronSeq2

# import libraries
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import neuronSeq2 as ns2
import numpy as np
import networkx as nx


# NSGUINerworkCanvas class
class NSGUINetworkCanvas(FigureCanvasTkAgg):
    def __init__(self, neuron_graph, master=None):
        #create the figure
        self.fig = Figure(figsize=(5, 5), dpi=100)
        #create the axis
        self.ax = self.fig.add_subplot(111)
        #create the canvas
        FigureCanvasTkAgg.__init__(self, self.fig, master=master)
        self.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="W")

        #set the neuron graph
        self.neuron_graph = neuron_graph

        #draw the neuron graph
        self.update_neuron_graph()

    def draw_neuron_graph(self):
        #clear the axis
        self.ax.clear()

        #draw the neuron graph
        nx.draw_networkx(self.neuron_graph, ax=self.ax)

        #draw the canvas
        self.draw()

        return

    def update_neuron_graph(self):
        #update the neuron graph
        self.neuron_graph.create_graph()
        #draw the neuron graph
        self.draw_neuron_graph()

        return
    
# main window class
class NeuronSeq2GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("NeuronSeq2")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.neuronSeq = ns2.NeuronSeq()

        self.create_widgets()

    def create_widgets(self):
        #create add neuron/note button
        self.add_nnote_button = tk.Button(self, text="Add Neuron/Note", command=self.add_neuron_note)
        self.add_nnote_button.grid(row=0, column=0, sticky="W")

        #create add connection button
        self.add_connection_button = tk.Button(self, text="Add Connection", command=self.add_connection)
        self.add_connection_button.grid(row=0, column=1, sticky="W")

        #create a neuron graph
        self.neuron_graph = ns2.NetworkGraph(self.neuronSeq)
        self.neuron_graph.create_graph()       
        self.neuron_graph_canvas = NSGUINetworkCanvas(self.neuron_graph, self)

        #create a label for the neuron list output
        self.neuron_list_label = tk.Label(self, text="Neuron List:")
        self.neuron_list_label.grid(row=2, column=0, sticky="W")

    def add_neuron_note(self):
        #create a new window for adding a neuron/note
        self.add_nnote_window = tk.Toplevel(self)
        self.add_nnote_window.title("Add Neuron/Note")
        self.add_nnote_window.geometry("400x200")
        self.add_nnote_window.resizable(width=False, height=False)

        #create a label for the midi channel
        self.nnote_midi_label = tk.Label(self.add_nnote_window, text="MIDI Channel:")
        self.nnote_midi_label.grid(row=0, column=0, sticky="W")

        #create an entry for the midi channel
        self.nnote_midi_entry = tk.Entry(self.add_nnote_window)
        self.nnote_midi_entry.grid(row=0, column=1, sticky="W")

        #create a label for the note MIDI number
        self.nnote_note_label = tk.Label(self.add_nnote_window, text="Note:")
        self.nnote_note_label.grid(row=1, column=0, sticky="W")

        #create an entry for the note MIDI number
        self.nnote_note_entry = tk.Entry(self.add_nnote_window)
        self.nnote_note_entry.grid(row=1, column=1, sticky="W")

        #create a label for the note velocity
        self.nnote_velocity_label = tk.Label(self.add_nnote_window, text="Velocity:")
        self.nnote_velocity_label.grid(row=2, column=0, sticky="W")

        #create an entry for the note velocity
        self.nnote_velocity_entry = tk.Entry(self.add_nnote_window)
        self.nnote_velocity_entry.grid(row=2, column=1, sticky="W")

        #create a label for the note duration
        self.nnote_duration_label = tk.Label(self.add_nnote_window, text="Duration:")
        self.nnote_duration_label.grid(row=3, column=0, sticky="W")

        #create an entry for the note duration
        self.nnote_duration_entry = tk.Entry(self.add_nnote_window)
        self.nnote_duration_entry.grid(row=3, column=1, sticky="W") 

        #create a label for the neuron/note id
        self.nnote_id_label = tk.Label(self.add_nnote_window, text="ID:")
        self.nnote_id_label.grid(row=4, column=0, sticky="W")

        #create an entry for the neuron/note id
        self.nnote_id_entry = tk.Entry(self.add_nnote_window)
        self.nnote_id_entry.grid(row=4, column=1, sticky="W")


        #create a add neuron/note button
        self.add_nnote_button = tk.Button(self.add_nnote_window, text="Add Neuron/Note", command=self.add_nnote_object)
        self.add_nnote_button.grid(row=5, column=0, columnspan=2, sticky="W")


    def add_connection(self):
        #create a new window for adding a connection
        self.add_connection_window = tk.Toplevel(self)
        self.add_connection_window.title("Add Connection")
        self.add_connection_window.geometry("400x200")
        self.add_connection_window.resizable(width=False, height=False)

        #create a label for the source neuron/note
        self.connection_source_label = tk.Label(self.add_connection_window, text="Source:")
        self.connection_source_label.grid(row=0, column=0, sticky="W")

        #create an entry for the source neuron/note
        self.connection_source_entry = tk.Entry(self.add_connection_window)
        self.connection_source_entry.grid(row=0, column=1, sticky="W")

        #create a label for the destination neuron/note
        self.connection_destination_label = tk.Label(self.add_connection_window, text="Destination:")
        self.connection_destination_label.grid(row=1, column=0, sticky="W")

        #create an entry for the destination neuron/note
        self.connection_destination_entry = tk.Entry(self.add_connection_window)
        self.connection_destination_entry.grid(row=1, column=1, sticky="W")

        #create a label for the connection weight 0 to 1
        self.connection_weight_0_to_1_label = tk.Label(self.add_connection_window, text="Weight 0 to 1:")
        self.connection_weight_0_to_1_label.grid(row=2, column=0, sticky="W")

        #create an entry for the connection weight 0 to 1
        self.connection_weight_0_to_1_entry = tk.Entry(self.add_connection_window)
        self.connection_weight_0_to_1_entry.grid(row=2, column=1, sticky="W")

        #create a label for the connection weight 1 to 0
        self.connection_weight_1_to_0_label = tk.Label(self.add_connection_window, text="Weight 1 to 0:")
        self.connection_weight_1_to_0_label.grid(row=3, column=0, sticky="W")

        #create an entry for the connection weight 1 to 0
        self.connection_weight_1_to_0_entry = tk.Entry(self.add_connection_window)
        self.connection_weight_1_to_0_entry.grid(row=3, column=1, sticky="W")

        #create a label for the connection id
        self.connection_id_label = tk.Label(self.add_connection_window, text="ID:")
        self.connection_id_label.grid(row=4, column=0, sticky="W")

        #create an entry for the connection id
        self.connection_id_entry = tk.Entry(self.add_connection_window)
        self.connection_id_entry.grid(row=4, column=1, sticky="W")

        #create a add connection button
        self.add_connection_button = tk.Button(self.add_connection_window, text="Add Connection", command=self.add_connection_object)
        self.add_connection_button.grid(row=5, column=0, columnspan=2, sticky="W")

    def add_nnote_object(self):
        #get the neuron/note parameters
        midi_channel = int(self.nnote_midi_entry.get())
        note = int(self.nnote_note_entry.get())
        velocity = int(self.nnote_velocity_entry.get())
        duration = float(self.nnote_duration_entry.get())
        identity = self.nnote_id_entry.get()
        #create the neuron/note object
        new_note = self.neuron_graph.add_nnote(midi_channel, note, velocity, duration, identity)
        new_note.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        #update and draw the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #update the neuron list
        self.neuron_list_label["text"] = "Neuron List:\n" + str(self.neuron_graph.neuronSeq.neuron_list_string())

        #destroy the add neuron/note window
        self.add_nnote_window.destroy()


    def add_connection_object(self):
        #get the connection parameters
        source = int(self.connection_source_entry.get())
        destination = int(self.connection_destination_entry.get())
        weight_0_to_1 = float(self.connection_weight_0_to_1_entry.get())
        weight_1_to_0 = float(self.connection_weight_1_to_0_entry.get())
        identity = self.connection_id_entry.get()
        #create the connection object
        self.neuron_graph.add_connection(identity, source, destination, weight_0_to_1, weight_1_to_0)

        #update the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #destroy the add connection window
        self.add_connection_window.destroy()

    def update_neuron_graph(self):
        #update the neuron graph
        self.neuron_graph.create_graph()

        #update the neuron graph canvas
        self.neuron_graph_canvas.draw()


# main function
def main():
    #create the main window
    app = NeuronSeq2GUI()
    #run the main loop
    app.mainloop()

# run main function
if __name__ == "__main__":
    main()


