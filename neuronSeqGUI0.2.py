import tkinter as tk
import tkinter.ttk as ttk
import neuronSeq as ns

class NeuronSeqGUISlider(tk.Scale):
    def __init__(self, master=None, pmh=None, ci=0, ni=0, pi=0):
        super().__init__(master, from_=-1.0, to=1.0, resolution=0.01, orient=tk.VERTICAL)
        self.name = ""
        #create slider name string
        self.name += "Conn: " + str(ci) + " Neuron:" + str(ni) + " Parameter: " + ns.get_param_name(pi)
        self.name += " slider"
        self["label"] = self.name
        self["length"] = 300
        self["width"] = 20
        self["showvalue"] = 1
        self["sliderlength"] = 20
        self["sliderrelief"] = tk.RAISED
        self["relief"] = tk.RAISED
        self["bd"] = 2
        self["highlightthickness"] = 0
        self["troughcolor"] = "grey"
        self["activebackground"] = "grey"
        self["bg"] = "grey"
        self["fg"] = "black"
        self["highlightcolor"] = "black"
        self["highlightbackground"] = "black"
        self["command"] = self.update_parameter
        #set slider's scale of values
        if pi==ns.ACTIVATION_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 1.0
            self["resolution"] = 0.01
        elif pi==ns.ADC_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 0.1
            self["resolution"] = 0.001
        elif pi==ns.THRESHOLD_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 1.0
            self["resolution"] = 0.01
        elif pi==ns.MIDI_NOTE_PARAMETER:
            self["from_"] = 0
            self["to"] = 127
            self["resolution"] = 1
        elif pi==ns.MIDI_VELOCITY_PARAMETER:
            self["from_"] = 0
            self["to"] = 127
            self["resolution"] = 1
        elif pi==ns.MIDI_DURATION_PARAMETER:
            self["from_"] = 0.0
            self["to"] = 10.0
            self["resolution"] = 0.1
        elif pi==ns.WEIGHT_0_1_PARAMETER:
            self["from_"] = -0.1
            self["to"] = 0.1
            self["resolution"] = 0.001
        elif pi==ns.WEIGHT_1_0_PARAMETER:
            self["from_"] = -0.1
            self["to"] = 0.1
            self["resolution"] = 0.001

        self.pack(side="left")
        self.bind("<ButtonRelease-1>", self.update_parameter)
        self.parameter_modulation_hub = None
        self.parameter_modulation_hub = pmh
        self.conn_idx = ci
        self.neuron_idx = ni
        self.parameter_idx = pi
        return

    def update_parameter(self, event):
        self.parameter_modulation_hub.change_parameter(self.conn_idx, self.neuron_idx, self.parameter_idx, self.get())
        return
    
class NeuronSeqGUI(tk.Frame):
    def __init__(self, master=None, pmh=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.parameter_modulation_hub = pmh
        self.create_widgets()
        self.sliders = []

    def create_widgets(self):
        self.add_slider_button = tk.Button(self)
        self.add_slider_button["text"] = "Add slider"
        self.add_slider_button["command"] = self.add_slider
        self.add_slider_button.pack(side="left")

    def add_slider(self):
        self.slider_creation_window = tk.Toplevel(self)
        self.slider_creation_window.title("Create slider")
        self.slider_creation_window.geometry("300x300")
        self.slider_creation_window.resizable(False, False)
        self.slider_creation_window.protocol("WM_DELETE_WINDOW", self.slider_creation_window.destroy)

        self.slider_creation_window_canvas = tk.Canvas(self.slider_creation_window)
        self.slider_creation_window_canvas.pack(side="left", fill="both", expand=True)

        self.slider_creation_window_scrollbar = ttk.Scrollbar(self.slider_creation_window, orient="vertical", command=self.slider_creation_window_canvas.yview)
        self.slider_creation_window_scrollbar.pack(side="right", fill="y")

        self.slider_creation_window_canvas.configure(yscrollcommand=self.slider_creation_window_scrollbar.set)
        self.slider_creation_window_canvas.bind('<Configure>', lambda e: self.slider_creation_window_canvas.configure(scrollregion=self.slider_creation_window_canvas.bbox("all")))

        self.slider_creation_window_scrollable_frame = tk.Frame(self.slider_creation_window_canvas)
        self.slider_creation_window_canvas.create_window((0, 0), window=self.slider_creation_window_scrollable_frame, anchor="nw")

        self.slider_parameter_select_buttons = []
        for parameter in self.parameter_modulation_hub.get_parameter_list():
            self.slider_parameter_select_buttons.append(tk.Button(self.slider_creation_window_scrollable_frame))
            self.slider_parameter_select_buttons[-1]["text"] = str(parameter)
            self.slider_parameter_select_buttons[-1]["command"] = lambda parameter=parameter: self.create_slider(parameter)
            self.slider_parameter_select_buttons[-1].pack(side="top")

    def create_slider(self, parameter):
        self.sliders.append(NeuronSeqGUISlider(self, self.parameter_modulation_hub, parameter[0], parameter[1], parameter[2]))

# Rest of your code remains unchanged

if __name__ == "__main__":
    #create NNote objects
    kick = ns.NNote(id = "Kick", note = 36, velocity = 100, duration = 0.5, channel = 1, activation = 0.0, addToCounter = 0.00001, threshold = 1.0)
    snare = ns.NNote(id = "Snare", note = 38, velocity = 100, duration = 0.5, channel = 1, activation = 0.0, addToCounter = 0.00001, threshold = 1.0)
    hihat = ns.NNote(id = "Hihat", note = 42, velocity = 100, duration = 0.5, channel = 1, activation = 0.0, addToCounter = 0.00001, threshold = 1.0)
    bass01 = ns.NNote(id = "Bass01", note = 48, velocity = 100, duration = 0.5, channel = 1, activation = 0.0, addToCounter = 0.00001, threshold = 1.0)

    #create Connection objects
    drumConnection00 = ns.Connection(kick, snare, -0.001, -0.001)
    drumConnection01 = ns.Connection(snare, hihat, -0.001, -0.001)
    drumConnection02 = ns.Connection(hihat, kick, -0.001, -0.001)

    #create parameter modulation hub
    parameter_modulation_hub = ns.ParameterModulationHub()

    #add connections to parameter modulation hub
    parameter_modulation_hub.add_connection(drumConnection00)
    parameter_modulation_hub.add_connection(drumConnection01)
    parameter_modulation_hub.add_connection(drumConnection02)

    root = tk.Tk()
    app = NeuronSeqGUI(master=root, pmh=parameter_modulation_hub)
    app.mainloop()
