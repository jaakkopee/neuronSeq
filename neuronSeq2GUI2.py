#graphical user interface for neuronSeq2

# import libraries
import tkinter as tk
from tkinter import ttk
from tkinter import constants as tkConstants
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import neuronSeq2 as ns2
import numpy as np
import networkx as nx

class NSGUISliderWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.sliders = []
        return

    def create_widgets(self):
        #create the sliders
        for slider in self.sliders:
            slider.create_widgets()

        self.update()
        return
    
    def add_slider(self, slider):
        self.sliders.append(slider)
        return
    
    def erase_display(self):
        for widget in self.winfo_children():
            widget.destroy()
        return
    
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
        nx.draw_networkx(self.neuron_graph, ax=self.ax, pos=nx.spring_layout(self.neuron_graph), node_color="blue", edge_color="black", font_color="black", font_size=10, node_size=480)
        #nx.draw_networkx_edge_labels(self.neuron_graph, ax=self.ax, pos=nx.spring_layout(self.neuron_graph), edge_labels=nx.get_edge_attributes(self.neuron_graph, 'label'))


        #draw the canvas
        self.draw()

        return

    def update_neuron_graph(self):
        #update the neuron graph
        self.neuron_graph.create_graph()
        #draw the neuron graph
        self.draw_neuron_graph()

        return

class NSGUIThresholdSlider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None, ni=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = ns2.THRESHOLD_PARAMETER
        return
    
    def create_widgets(self):
        self.threshold_slider = tk.Scale(self.master)
        self.threshold_slider["from_"] = 0
        self.threshold_slider["to"] = 1
        self.threshold_slider["resolution"] = 0.01
        self.threshold_slider["orient"] = tkConstants.VERTICAL
        self.threshold_slider["length"] = 200
        self.threshold_slider["label"] = "Threshold "+str(self.ci)+","+str(self.ni)
        self.threshold_slider["command"] = self.set_threshold
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.threshold_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_threshold(self, value):
        self.ns.set_threshold(self.ci, self.ni, float(value))
        return

class NSGUIMidiNoteSlider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None, ni=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = ns2.MIDI_NOTE_PARAMETER
        return
    
    def create_widgets(self):
        self.midi_note_slider = tk.Scale(self.master)
        self.midi_note_slider["from_"] = 0
        self.midi_note_slider["to"] = 127
        self.midi_note_slider["resolution"] = 1
        self.midi_note_slider["orient"] = tkConstants.VERTICAL
        self.midi_note_slider["length"] = 200
        self.midi_note_slider["label"] = "MIDI note "+str(self.ci)+","+str(self.ni)
        self.midi_note_slider["command"] = self.set_midi_note
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.midi_note_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_midi_note(self, value):
        self.ns.set_midi_note(self.ci, self.ni, int(value))
        return

class NSGUIMidiVelocitySlider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None, ni=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = ns2.MIDI_VELOCITY_PARAMETER
        return
    
    def create_widgets(self):
        self.midi_velocity_slider = tk.Scale(self.master)
        self.midi_velocity_slider["from_"] = 0
        self.midi_velocity_slider["to"] = 127
        self.midi_velocity_slider["resolution"] = 1
        self.midi_velocity_slider["orient"] = tkConstants.VERTICAL
        self.midi_velocity_slider["length"] = 200
        self.midi_velocity_slider["label"] = "MIDI velocity "+str(self.ci)+","+str(self.ni)
        self.midi_velocity_slider["command"] = self.set_midi_velocity
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.midi_velocity_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_midi_velocity(self, value):
        self.ns.set_midi_velocity(self.ci, self.ni, int(value))
        return
    
class NSGUIMidiDurationSlider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None, ni=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = ns2.MIDI_DURATION_PARAMETER
        return
    
    def create_widgets(self):
        self.midi_duration_slider = tk.Scale(self.master)
        self.midi_duration_slider["from_"] = 0
        self.midi_duration_slider["to"] = 10
        self.midi_duration_slider["resolution"] = 0.1
        self.midi_duration_slider["orient"] = tkConstants.VERTICAL
        self.midi_duration_slider["length"] = 200
        self.midi_duration_slider["label"] = "MIDI duration "+str(self.ci)+","+str(self.ni)
        self.midi_duration_slider["command"] = self.set_midi_duration
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.midi_duration_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_midi_duration(self, value):
        self.ns.set_midi_duration(self.ci, self.ni, float(value))
        return
    
class NSGUIW0to1Slider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = 0
        self.pi = ns2.WEIGHT_0_1_PARAMETER
        return
    
    def create_widgets(self):
        self.w0to1_slider = tk.Scale(self.master)
        self.w0to1_slider["from_"] = -1
        self.w0to1_slider["to"] = 1
        self.w0to1_slider["resolution"] = 0.01
        self.w0to1_slider["orient"] = tkConstants.VERTICAL
        self.w0to1_slider["length"] = 200
        self.w0to1_slider["label"] = "W 0 to 1, "+str(self.ci)
        self.w0to1_slider["command"] = self.set_w0to1
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.w0to1_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_w0to1(self, value):
        self.ns.set_weight_0_to_1(self.ci, float(value))
        return
    
class NSGUIW1to0Slider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = 0
        self.pi = ns2.WEIGHT_1_0_PARAMETER
        return
    
    def create_widgets(self):
        self.w1to0_slider = tk.Scale(self.master)
        self.w1to0_slider["from_"] = -1
        self.w1to0_slider["to"] = 1
        self.w1to0_slider["resolution"] = 0.01
        self.w1to0_slider["orient"] = tkConstants.VERTICAL
        self.w1to0_slider["length"] = 200
        self.w1to0_slider["label"] = "W 1 to 0, "+str(self.ci)
        self.w1to0_slider["command"] = self.set_w1to0
        column_n = 0
        for slider in self.master.sliders:
            column_n += 1
            if slider.pi==self.pi and slider.ci==self.ci and slider.ni==self.ni:
                break    
        self.w1to0_slider.grid(row=0, column=column_n, sticky="W")
        return
    
    def set_w1to0(self, value):
        self.ns.set_weight_1_to_0(self.ci, float(value))
        return    

 
# main window class
class NeuronSeq2GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("NeuronSeq2")
        self.geometry("800x600")
        self.resizable(width=True, height=False)
        self.neuronSeq = ns2.NeuronSeq()
        #handle closing the window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def on_closing(self):
        #stop the neuronSeq
        self.neuronSeq.stop()
        #destroy the window
        self.destroy()
        return

    def create_widgets(self):
        #create add neuron/note button
        self.add_nnote_button = tk.Button(self, text="Add Neuron/Note", command=self.add_neuron_note)
        self.add_nnote_button.grid(row=0, column=0, sticky="W")

        #create add connection button
        self.add_connection_button = tk.Button(self, text="Add Connection", command=self.add_connection)
        self.add_connection_button.grid(row=0, column=1, sticky="W")

        #create add slider button
        self.add_slider_button = tk.Button(self, text="Add Slider", command=self.add_slider)
        self.add_slider_button.grid(row=0, column=2, sticky="W")

        #create create drum set button
        self.create_drum_set_button = tk.Button(self, text="Create Drum Set", command=self.create_drum_set)
        self.create_drum_set_button.grid(row=0, column=3, sticky="W")

        #create a button for edit parameter button
        self.edit_parameter_button = tk.Button(self, text="Edit Parameter", command=self.edit_parameter)
        self.edit_parameter_button.grid(row=0, column=4, sticky="W")

        #create a neuron graph
        self.neuron_graph = ns2.NetworkGraph(self.neuronSeq)
        self.neuron_graph.create_graph()       
        self.neuron_graph_canvas = NSGUINetworkCanvas(self.neuron_graph, self)

        #create a label for the neuron list output
        self.neuron_list_label = tk.Label(self, text="Neuron/Connection List:")
        self.neuron_list_label.grid(row=2, column=0, columnspan=4, sticky="W")

        #create slider window
        self.slider_window = NSGUISliderWindow(self)
        self.slider_window.title("Sliders")
        self.slider_window.geometry("400x200")
        self.slider_window.resizable(width=True, height=False)

    def edit_parameter(self):
        #create a new window for editing a parameter
        self.edit_parameter_window = tk.Toplevel(self)
        self.edit_parameter_window.title("Edit Parameter")
        self.edit_parameter_window.geometry("400x200")
        self.edit_parameter_window.resizable(width=False, height=False)

        #create a label for the connection index
        self.edit_parameter_connection_index_label = tk.Label(self.edit_parameter_window, text="Connection Index:")
        self.edit_parameter_connection_index_label.grid(row=0, column=0, sticky="W")

        #create an entry for the connection index
        self.edit_parameter_connection_index_entry = tk.Entry(self.edit_parameter_window)
        self.edit_parameter_connection_index_entry.grid(row=0, column=1, sticky="W")

        #create a label for the neuron index
        self.edit_parameter_neuron_index_label = tk.Label(self.edit_parameter_window, text="Neuron Index:")
        self.edit_parameter_neuron_index_label.grid(row=1, column=0, sticky="W")

        #create an entry for the neuron index
        self.edit_parameter_neuron_index_entry = tk.Entry(self.edit_parameter_window)
        self.edit_parameter_neuron_index_entry.grid(row=1, column=1, sticky="W")

        #create a label for the parameter index
        self.edit_parameter_parameter_index_label = tk.Label(self.edit_parameter_window, text="Parameter Index:")
        self.edit_parameter_parameter_index_label.grid(row=2, column=0, sticky="W")

        #create an entry for the parameter index
        self.edit_parameter_parameter_index_entry = tk.Entry(self.edit_parameter_window)
        self.edit_parameter_parameter_index_entry.grid(row=2, column=1, sticky="W")

        #create a label for the parameter value
        self.edit_parameter_parameter_value_label = tk.Label(self.edit_parameter_window, text="Parameter Value:")
        self.edit_parameter_parameter_value_label.grid(row=3, column=0, sticky="W")

        #create an entry for the parameter value
        self.edit_parameter_parameter_value_entry = tk.Entry(self.edit_parameter_window)
        self.edit_parameter_parameter_value_entry.grid(row=3, column=1, sticky="W")

        #create a edit parameter button
        self.edit_parameter_button = tk.Button(self.edit_parameter_window, text="Edit Parameter", command=self.edit_parameter_fuction)
        self.edit_parameter_button.grid(row=4, column=0, columnspan=2, sticky="W")

    def edit_parameter_fuction(self):
        #get the parameter values
        connection_index = int(self.edit_parameter_connection_index_entry.get())
        neuron_index = int(self.edit_parameter_neuron_index_entry.get())
        parameter_index = int(self.edit_parameter_parameter_index_entry.get())
        if parameter_index==ns2.ACTIVATION_FUNCTION_PARAMETER:
            parameter_value = int(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.THRESHOLD_PARAMETER:
            parameter_value = float(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.MIDI_NOTE_PARAMETER:
            parameter_value = int(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.MIDI_VELOCITY_PARAMETER:
            parameter_value = int(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.MIDI_DURATION_PARAMETER:
            parameter_value = float(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.WEIGHT_0_1_PARAMETER:
            parameter_value = float(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.WEIGHT_1_0_PARAMETER:
            parameter_value = float(self.edit_parameter_parameter_value_entry.get())
        elif parameter_index==ns2.ACT_BUFFER_SIZE_PARAMETER:
            parameter_value = 2**int(self.edit_parameter_parameter_value_entry.get())
        
        #edit the parameter
        self.neuronSeq.change_parameter(connection_index, neuron_index, parameter_index, parameter_value)

        #update the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #update the neuron list
        self.neuron_list_label["text"] = "Neuron/Connection List:\n" + str(self.neuron_graph.neuronSeq.neuron_list_string())

        #destroy the edit parameter window
        self.edit_parameter_window.destroy()

        return

    def create_drum_set(self):
        kick = self.neuron_graph.add_nnote(1, ns2.KICK, 127, 0.1, 2**24, "kick")
        kick.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        snare = self.neuron_graph.add_nnote(1, ns2.SNARE, 127, 0.1, 2**24, "snare")
        snare.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        closed_hihat = self.neuron_graph.add_nnote(1, ns2.CLOSED_HIHAT, 127, 0.1, 2**24, "chh")
        closed_hihat.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        open_hihat = self.neuron_graph.add_nnote(1, ns2.OPEN_HIHAT, 127, 0.1, 2**24, "ohh")
        open_hihat.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        crash = self.neuron_graph.add_nnote(1, ns2.CRASH, 127, 0.1, 2**24, "crash")
        crash.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        ride = self.neuron_graph.add_nnote(1, ns2.RIDE, 127, 0.1, 2**24, "ride")
        ride.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        tom1 = self.neuron_graph.add_nnote(1, ns2.TOM1, 127, 0.1, 2**24, "tom1")
        tom1.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        tom2 = self.neuron_graph.add_nnote(1, ns2.TOM2, 127, 0.1, 2**24, "tom2")
        tom2.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        tom3 = self.neuron_graph.add_nnote(1, ns2.TOM3, 127, 0.1, 2**24, "tom3")
        tom3.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        
        #update the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #update the neuron list
        self.neuron_list_label["text"] = "Neuron/Connection List:\n" + str(self.neuron_graph.neuronSeq.neuron_list_string())

        return

    def add_slider(self):
        #create a new window for adding a slider
        self.add_slider_window = tk.Toplevel(self)
        self.add_slider_window.title("Add Slider")
        self.add_slider_window.geometry("400x200")
        self.add_slider_window.resizable(width=False, height=False)
    
        #create a label for the connection index
        self.slider_connection_index_label = tk.Label(self.add_slider_window, text="Connection Index:")
        self.slider_connection_index_label.grid(row=0, column=0, sticky="W")

        #create an entry for the connection index
        self.slider_connection_index_entry = tk.Entry(self.add_slider_window)
        self.slider_connection_index_entry.grid(row=0, column=1, sticky="W")

        #create a label for the neuron index
        self.slider_neuron_index_label = tk.Label(self.add_slider_window, text="Neuron Index:")
        self.slider_neuron_index_label.grid(row=1, column=0, sticky="W")

        #create an entry for the neuron index
        self.slider_neuron_index_entry = tk.Entry(self.add_slider_window)
        self.slider_neuron_index_entry.grid(row=1, column=1, sticky="W")

        #create a laber for the parameter index
        self.slider_parameter_index_label = tk.Label(self.add_slider_window, text="Parameter Index:")
        self.slider_parameter_index_label.grid(row=2, column=0, sticky="W")

        #create an entry for the parameter index
        self.slider_parameter_index_entry = tk.Entry(self.add_slider_window)
        self.slider_parameter_index_entry.grid(row=2, column=1, sticky="W")

        #create a add slider button
        self.add_slider_button = tk.Button(self.add_slider_window, text="Add Slider", command=self.add_slider_object)
        self.add_slider_button.grid(row=3, column=0, columnspan=2, sticky="W")

        
    def add_slider_object(self):
        #get the slider parameters
        connection_index = int(self.slider_connection_index_entry.get())
        neuron_index = int(self.slider_neuron_index_entry.get())
        parameter_index = int(self.slider_parameter_index_entry.get())

        #create slider
        if parameter_index==ns2.THRESHOLD_PARAMETER:
            slider = NSGUIThresholdSlider(self.slider_window, self.neuronSeq, connection_index, neuron_index)
        elif parameter_index==ns2.MIDI_NOTE_PARAMETER:
            slider = NSGUIMidiNoteSlider(self.slider_window, self.neuronSeq, connection_index, neuron_index)
        elif parameter_index==ns2.MIDI_VELOCITY_PARAMETER:
            slider = NSGUIMidiVelocitySlider(self.slider_window, self.neuronSeq, connection_index, neuron_index)
        elif parameter_index==ns2.MIDI_DURATION_PARAMETER:
            slider = NSGUIMidiDurationSlider(self.slider_window, self.neuronSeq, connection_index, neuron_index)
        elif parameter_index==ns2.WEIGHT_0_1_PARAMETER:
            slider = NSGUIW0to1Slider(self.slider_window, self.neuronSeq, connection_index)
        elif parameter_index==ns2.WEIGHT_1_0_PARAMETER:
            slider = NSGUIW1to0Slider(self.slider_window, self.neuronSeq, connection_index)
        else:
            print("Error: invalid parameter index")
        #empty the slider window
        self.slider_window.erase_display()

        #add the slider to the slider window
        self.slider_window.add_slider(slider)

        #create the slider widgets
        self.slider_window.create_widgets()


        #destroy the add slider window
        self.add_slider_window.destroy()

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

        #create a label for lenX
        self.nnote_lenX_label = tk.Label(self.add_nnote_window, text="Activation Buffer Length:") 
        self.nnote_lenX_label.grid(row=4, column=0, sticky="W")

        #create an entry for lenX
        self.nnote_lenX_entry = tk.Entry(self.add_nnote_window)
        self.nnote_lenX_entry.grid(row=4, column=1, sticky="W")

        #create a label for the neuron/note id
        self.nnote_id_label = tk.Label(self.add_nnote_window, text="ID:")
        self.nnote_id_label.grid(row=5, column=0, sticky="W")

        #create an entry for the neuron/note id
        self.nnote_id_entry = tk.Entry(self.add_nnote_window)
        self.nnote_id_entry.grid(row=5, column=1, sticky="W")


        #create a add neuron/note button
        self.add_nnote_button = tk.Button(self.add_nnote_window, text="Add Neuron/Note", command=self.add_nnote_object)
        self.add_nnote_button.grid(row=6, column=0, columnspan=2, sticky="W")


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
        lenX = 2**int(self.nnote_lenX_entry.get())
        identity = self.nnote_id_entry.get()
        #create the neuron/note object. neuron_graph.add_nnote() updates neuronSeq instance too.
        new_note = self.neuron_graph.add_nnote(midi_channel, note, velocity, duration, lenX, identity)
        new_note.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        print("new note: ", new_note.get_id(), new_note.channel, new_note.note, new_note.velocity, new_note.duration, new_note.lenX, new_note.Y[0], new_note.Y[-1])
        #update and draw the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #update the neuron list
        self.neuron_list_label["text"] = "Neuron/Connection List:\n" + str(self.neuron_graph.neuronSeq.neuron_list_string())

        #destroy the add neuron/note window
        self.add_nnote_window.destroy()


    def add_connection_object(self):
        #get the connection parameters
        source = int(self.connection_source_entry.get())
        destination = int(self.connection_destination_entry.get())
        weight_0_to_1 = float(self.connection_weight_0_to_1_entry.get())
        weight_1_to_0 = float(self.connection_weight_1_to_0_entry.get())
        identity = self.connection_id_entry.get()
        #create the connection object. neuron_graph.add_connection() updates neuronSeq instance too.
        self.neuron_graph.add_connection(identity, source, destination, weight_0_to_1, weight_1_to_0)

        print("new connection: ", self.neuronSeq.connections[-1].get_id(), self.neuronSeq.connections[-1].source.get_id(), self.neuronSeq.connections[-1].destination.get_id(), self.neuronSeq.connections[-1].weight_0_to_1, self.neuronSeq.connections[-1].weight_1_to_0)

        #update the neuron graph
        self.neuron_graph_canvas.update_neuron_graph()

        #update the neuron list
        self.neuron_list_label["text"] = "Neuron/Connection List:\n" + str(self.neuron_graph.neuronSeq.neuron_list_string())

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


