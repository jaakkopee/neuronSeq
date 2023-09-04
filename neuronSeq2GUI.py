import neuronSeq2 as ns2
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter.simpledialog as tkSimpleDialog
import tkinter.scrolledtext as tkScrolledText
import tkinter.colorchooser as tkColorChooser
import tkinter.constants as tkConstants
import tkinter.dnd as tkDnd
import tkinter.tix as tkTix

class NSGUICreateNNoteWindow(tk.Toplevel):
    def __init__(self, master=None, ns=None):
        super().__init__(master)
        self.title("Create N Note")
        self.master = master
        self.ns = ns
        self.create_widgets()

    def create_widgets(self):
        self.nnote_channel_label = tk.Label(self)
        self.nnote_channel_label["text"] = "Channel:"
        self.nnote_channel_label.pack(side="left")
        self.nnote_channel_entry = tk.Entry(self)
        self.nnote_channel_entry.pack(side="left")
        self.nnote_midi_note_label = tk.Label(self)
        self.nnote_midi_note_label["text"] = "MIDI note:"
        self.nnote_midi_note_label.pack(side="left")
        self.nnote_midi_note_entry = tk.Entry(self)
        self.nnote_midi_note_entry.pack(side="left")
        self.nnote_midi_velocity_label = tk.Label(self)
        self.nnote_midi_velocity_label["text"] = "MIDI velocity:"
        self.nnote_midi_velocity_label.pack(side="left")
        self.nnote_midi_velocity_entry = tk.Entry(self)
        self.nnote_midi_velocity_entry.pack(side="left")
        self.nnote_midi_duration_label = tk.Label(self)
        self.nnote_midi_duration_label["text"] = "MIDI duration:"
        self.nnote_midi_duration_label.pack(side="left")
        self.nnote_midi_duration_entry = tk.Entry(self)
        self.nnote_midi_duration_entry.pack(side="left")
        self.nnote_id_label = tk.Label(self)
        self.nnote_id_label["text"] = "ID:"
        self.nnote_id_label.pack(side="left")
        self.nnote_id_entry = tk.Entry(self)
        self.nnote_id_entry.pack(side="left")
        self.nnote_create_button = tk.Button(self)
        self.nnote_create_button["text"] = "Create"
        self.nnote_create_button["command"] = self.create_nnote
        self.nnote_create_button.pack(side="left")
        return
    
    def create_nnote(self):
        nnote_channel = int(self.nnote_channel_entry.get())
        nnote_midi_note = int(self.nnote_midi_note_entry.get())
        nnote_midi_velocity = int(self.nnote_midi_velocity_entry.get())
        nnote_midi_duration = float(self.nnote_midi_duration_entry.get())
        nnote_id = self.nnote_id_entry.get()
        nnote = self.ns.create_nnote(nnote_channel, nnote_midi_note, nnote_midi_velocity, nnote_midi_duration, nnote_id)
        nnote.set_activation_function(ns2.NEURON_ACTIVATION_FUNCTION_SIGMOID)
        self.destroy()
        return
    
class NSGUICreateConnectionWindow(tk.Toplevel):
    def __init__(self, master=None, ns=None):
        super().__init__(master)
        self.title("Create Connection")
        self.master = master
        self.ns = ns
        self.create_widgets()

    def create_widgets(self):
        self.conn_name_label = tk.Label(self)
        self.conn_name_label["text"] = "Connection name:"
        self.conn_name_label.pack(side="left")
        self.conn_name_entry = tk.Entry(self)
        self.conn_name_entry.pack(side="left")
        self.conn_from_label = tk.Label(self)
        self.conn_from_label["text"] = "From:"
        self.conn_from_label.pack(side="left")
        self.conn_from_entry = tk.Entry(self)
        self.conn_from_entry.pack(side="left")
        self.conn_to_label = tk.Label(self)
        self.conn_to_label["text"] = "To:"
        self.conn_to_label.pack(side="left")
        self.conn_to_entry = tk.Entry(self)
        self.conn_to_entry.pack(side="left")
        self.conn_weight_0_to_1_label = tk.Label(self)
        self.conn_weight_0_to_1_label["text"] = "Weight 0 to 1:"
        self.conn_weight_0_to_1_label.pack(side="left")
        self.conn_weight_0_to_1_entry = tk.Entry(self)
        self.conn_weight_0_to_1_entry.pack(side="left")
        self.conn_weight_1_to_0_label = tk.Label(self)
        self.conn_weight_1_to_0_label["text"] = "Weight 1 to 0:"
        self.conn_weight_1_to_0_label.pack(side="left")
        self.conn_weight_1_to_0_entry = tk.Entry(self)
        self.conn_weight_1_to_0_entry.pack(side="left")
        self.conn_create_button = tk.Button(self)
        self.conn_create_button["text"] = "Create"
        self.conn_create_button["command"] = self.create_conn
        self.conn_create_button.pack(side="left")
        return
        
    def create_conn(self):
        conn_name = self.conn_name_entry.get()
        conn_from = int(self.conn_from_entry.get())
        conn_to = int(self.conn_to_entry.get())
        conn_weight_0_to_1 = float(self.conn_weight_0_to_1_entry.get())
        conn_weight_1_to_0 = float(self.conn_weight_1_to_0_entry.get())

        self.ns.create_connection(conn_name, conn_from, conn_to, conn_weight_0_to_1, conn_weight_1_to_0)
        self.destroy()
        return
    
class NSGUISLider(tk.Scale):
    def __init__(self, master=None, ns=None, ci=None, ni=None, pi=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = pi
        self.create_widgets()
        return
    
    def create_widgets(self):
        if self.pi == ns2.THRESHOLD_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 1.0
            self["resolution"] = 0.01
        elif self.pi == ns2.MIDI_NOTE_PARAMETER:
            self["from_"] = 0
            self["to"] = 127
            self["resolution"] = 1
        elif self.pi == ns2.MIDI_VELOCITY_PARAMETER:
            self["from_"] = 0
            self["to"] = 127
            self["resolution"] = 1
        elif self.pi == ns2.MIDI_DURATION_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 10.0
            self["resolution"] = 0.1
        elif self.pi == ns2.WEIGHT_0_1_PARAMETER:
            self["from_"] = -0.1
            self["to"] = 0.1
            self["resolution"] = 0.001
        elif self.pi == ns2.WEIGHT_1_0_PARAMETER:
            self["from_"] = -0.1
            self["to"] = 0.1
            self["resolution"] = 0.001

        self.pack(side="left")
        self.bind("<ButtonRelease-1>", self.update_parameter)
        return

    def update_parameter(self, event):
        self.ns.change_parameter(self.ci, self.ni, self.pi, self.get())
        return

class NSGUICreateSliderWindow(tk.Toplevel):
    def __init__(self, master=None, ns=None, ci=None, ni=None, pi=None):
        self.master = master
        self.ns = ns
        self.ci = ci
        self.ni = ni
        self.pi = pi
        self.create_widgets()
        return
    
    def create_widgets(self):
        self.slider_creation_window = tk.Toplevel(self.master)
        self.slider_creation_window.title("Create Slider")
        self.slider_creation_window.master = self.master
        #ci entry
        self.slider_creation_window.ci_label = tk.Label(self.slider_creation_window)
        self.slider_creation_window.ci_label["text"] = "Connection index:"
        self.slider_creation_window.ci_label.pack(side="left")
        self.slider_creation_window.ci_entry = tk.Entry(self.slider_creation_window)
        self.slider_creation_window.ci_entry.pack(side="left")
        #ni entry
        self.slider_creation_window.ni_label = tk.Label(self.slider_creation_window)
        self.slider_creation_window.ni_label["text"] = "Neuron index:"
        self.slider_creation_window.ni_label.pack(side="left")
        self.slider_creation_window.ni_entry = tk.Entry(self.slider_creation_window)
        self.slider_creation_window.ni_entry.pack(side="left")
        #pi entry
        self.slider_creation_window.pi_label = tk.Label(self.slider_creation_window)
        self.slider_creation_window.pi_label["text"] = "Parameter index:"
        self.slider_creation_window.pi_label.pack(side="left")
        self.slider_creation_window.pi_entry = tk.Entry(self.slider_creation_window)
        self.slider_creation_window.pi_entry.pack(side="left")

        #create slider button
        self.slider_creation_window.create_slider_button = tk.Button(self.slider_creation_window)
        self.slider_creation_window.create_slider_button["text"] = "Create Slider"
        self.slider_creation_window.create_slider_button["command"] = self.create_slider
        self.slider_creation_window.create_slider_button.pack(side="left")

        return
    
    def create_slider(self):
        self.slider = NSGUISLider(self.master, self.ns, self.ci, self.ni, self.pi)
        self.slider_creation_window.destroy()
        return self.slider

class NSGUIMainWindow(tk.Frame):
    def __init__(self, master=None, ns=None):
        super().__init__(master)
        self.master = master
        self.ns = ns
        self.pack()
        self.create_widgets()
        self.sliders = []

    def create_widgets(self):
        self.create_nnote_button = tk.Button(self)
        self.create_nnote_button["text"] = "Create N Note"
        self.create_nnote_button["command"] = self.create_nnote
        self.create_nnote_button.pack(side="left")
        self.create_connection_button = tk.Button(self)
        self.create_connection_button["text"] = "Create Connection"
        self.create_connection_button["command"] = self.create_connection
        self.create_connection_button.pack(side="left")
        self.create_slider_button = tk.Button(self)
        self.create_slider_button["text"] = "Create Slider"
        self.create_slider_button["command"] = self.create_slider
        self.create_slider_button.pack(side="left")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="left")
        return
    
    def create_nnote(self):
        self.nsgui_create_nnote_window = NSGUICreateNNoteWindow(self.master, self.ns)
        return
    
    def create_connection(self):
        self.nsgui_create_connection_window = NSGUICreateConnectionWindow(self.master, self.ns)
        return
    
    def create_slider(self):
        self.nsgui_create_slider_window = NSGUICreateSliderWindow(self.master, self.ns)
        return
    
class NSGUI(tk.Frame):
    def __init__(self, master=None, ns=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.ns = ns
        self.create_widgets()
        return
    
    def create_widgets(self):
        self.nsgui_main_window = NSGUIMainWindow(self.master, self.ns)
        return
    
#usage example
root = tk.Tk()
ns = ns2.NeuronSeq()
nsgui = NSGUI(root, ns)
nsgui.mainloop()
