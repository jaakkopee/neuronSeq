#complete rewrite of neuronSeq.py

import numpy as np
import time
import threading
import rtmidi

#global variables
#neuron parameters
ACTIVATION_FUNCTION_PARAMETER = 0
THRESHOLD_PARAMETER = 1
MIDI_NOTE_PARAMETER = 2
MIDI_VELOCITY_PARAMETER = 3
MIDI_DURATION_PARAMETER = 4
WEIGHT_0_1_PARAMETER = 5
WEIGHT_1_0_PARAMETER = 6
#neuron parameter names
NEURON_PARAMETER_NAMES = []
NEURON_PARAMETER_NAMES.append("Activation Function")
NEURON_PARAMETER_NAMES.append("Threshold")
NEURON_PARAMETER_NAMES.append("MIDI Note")
NEURON_PARAMETER_NAMES.append("MIDI Velocity")
NEURON_PARAMETER_NAMES.append("MIDI Duration")
NEURON_PARAMETER_NAMES.append("Weight 0->1")
NEURON_PARAMETER_NAMES.append("Weight 1->0")
#neuron activation functions
NEURON_ACTIVATION_FUNCTION_LINEAR = 0
NEURON_ACTIVATION_FUNCTION_SIGMOID = 1
NEURON_ACTIVATION_FUNCTION_TANH = 2
NEURON_ACTIVATION_FUNCTION_RELU = 3
NEURON_ACTIVATION_FUNCTION_SOFTMAX = 4
#neuron activation function names
NEURON_ACTIVATION_FUNCTION_NAME_LINEAR = "Linear"
NEURON_ACTIVATION_FUNCTION_NAME_SIGMOID = "Sigmoid"
NEURON_ACTIVATION_FUNCTION_NAME_TANH = "Tanh"
NEURON_ACTIVATION_FUNCTION_NAME_RELU = "ReLU"
NEURON_ACTIVATION_FUNCTION_NAME_SOFTMAX = "Softmax"

#MIDI drum note numbers
KICK = 36
SNARE = 38
CLOSED_HIHAT = 42
OPEN_HIHAT = 46
CRASH = 49
RIDE = 51
TOM1 = 48
TOM2 = 45
TOM3 = 43
TOM4 = 41


#midi output
MIDI_OUTPUT_PORT_NAME = "NeuronSeq"
MIDI_OUTPUT_PORT_NAME_DEFAULT = "NeuronSeq"
#get midi output ports from rtmidi
midi_output = rtmidi.RtMidiOut()
available_midi_output_ports = midi_output.getPortCount()
midi_output_port_name = MIDI_OUTPUT_PORT_NAME_DEFAULT
#try opening default port
if available_midi_output_ports:
    midi_output.openPort(0)
else:
    #open virtual port
    midi_output.openVirtualPort(midi_output_port_name)

#NNote is a neuron that outputs a midi events
class NNote:
    def __init__(self, channel=0, note=0, velocity=0, duration=0.0, id="NNote"):
        self.note = note
        self.velocity = velocity
        self.duration = duration
        self.activation = 0.0
        self.activation_function = NEURON_ACTIVATION_FUNCTION_LINEAR
        self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_LINEAR

        self.activation_index=0
        self.X = []
        self.Y = []
        self.create_activation_X_axis()
        self.create_activation_Y_axis()
        self.threshold = 1.0
        self.note_thread = None

        self.channel = channel        
        self.midi_msg = rtmidi.MidiMessage()

        return

    def set_note(self, note):
        self.note = note
        return

    def set_velocity(self, velocity):
        self.velocity = velocity
        return

    def set_duration(self, duration):
        self.duration = duration
        return

    def set_threshold(self, threshold):
        self.threshold = threshold
        return

    def get_threshold(self):
        return self.threshold
           
    def set_activation_function(self, activation_function):
        self.activation_function = activation_function
        if activation_function==NEURON_ACTIVATION_FUNCTION_LINEAR:
            self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_LINEAR
            #recalculate Y axis
            self.create_activation_Y_axis()
        elif activation_function==NEURON_ACTIVATION_FUNCTION_SIGMOID:
            self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_SIGMOID
            #recalculate Y axis
            self.create_activation_Y_axis()
        elif activation_function==NEURON_ACTIVATION_FUNCTION_TANH:
            self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_TANH
            #recalculate Y axis
            self.create_activation_Y_axis()
        elif activation_function==NEURON_ACTIVATION_FUNCTION_RELU:
            self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_RELU
            #recalculate Y axis
            self.create_activation_Y_axis()
        elif activation_function==NEURON_ACTIVATION_FUNCTION_SOFTMAX:
            self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_SOFTMAX
            #recalculate Y axis
            self.create_activation_Y_axis()
        return
        
    def get_activation_function_name(self):
        return self.activation_function_name
    
    def get_activation_function(self):
        return self.activation_function
    
    #activation function
    def create_activation_X_axis(self):
        self.X = np.arange(0, 32767)
        return
    
    def create_activation_Y_axis(self):
        if self.activation_function==NEURON_ACTIVATION_FUNCTION_LINEAR:
            self.Y = self.X
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_SIGMOID:
            self.Y = 1.0 / (1.0 + np.exp(-self.X))
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_TANH:
            self.Y = np.tanh(self.X)
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_RELU:
            self.Y = np.maximum(self.X, 0)
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_SOFTMAX:
            self.Y = np.exp(self.X) / np.sum(np.exp(self.X))
        return    

    def create_midi_event(self):
        #create midi event
        midi_event = self.midi_msg.noteOn(self.channel, self.note, self.velocity)
        return midi_event

    def create_midi_event_off(self):
        #create midi event
        midi_event = self.midi_msg.noteOn(self.channel, self.note, 0)
        return midi_event

    def note_thread_start(self):
        #start thread
        self.note_thread = threading.Thread(target=self.execute_note_thread)
        self.note_thread.start()
        return
            
    def execute_note_thread(self):
        #create midi event
        midi_event = self.create_midi_event()
        #send midi event
        midi_output.sendMessage(midi_event)
        #sleep for duration
        time.sleep(self.duration)
        #create midi event
        midi_event = self.create_midi_event_off()
        #send midi event
        midi_output.sendMessage(midi_event)
        return

    def advance_activation_index(self):
        self.activation_index += 1
        if self.activation_index >= len(self.X):
            self.activation_index = len(self.X)-1
        return
    
class Connection(threading.Thread):
    def __init__(self, name, nnote1, nnnote2, weight_0_to_1=0.0, weight_1_to_0=0.0):
        threading.Thread.__init__(self)
        self.weights = (weight_0_to_1, weight_1_to_0)
        self.nnotes = (nnote1, nnnote2)
        self.name = name

    def set_weight(self, weight_idx, weight_value):
        self.weights[weight_idx] = weight_value
        return
    
    def get_weight(self, weight_idx):
        return self.weights[weight_idx]
    
    def get_weights(self):
        return self.weights
    
    def set_nnote(self, nnote_idx, nnote):
        self.nnotes[nnote_idx] = nnote
        return
    
    def get_nnote(self, nnote_idx):
        return self.nnotes[nnote_idx]
    
    def get_nnotes(self):
        return self.nnotes
    
    def run(self):
        while True:
            if self.nnotes[0].Y[self.nnotes[0].activation_index] < self.nnotes[0].threshold:
                self.nnotes[1].advance_activation_index()
            if self.nnotes[1].Y[self.nnotes[1].activation_index] < self.nnotes[1].threshold:
                self.nnotes[0].advance_activation_index()
            
            #calculate new activation
            self.nnotes[0].activation += self.nnotes[1].Y[self.nnotes[1].activation_index] * self.weights[0]
            self.nnotes[1].activation += self.nnotes[0].Y[self.nnotes[0].activation_index] * self.weights[1]

            #if activation reaches threshold, start note thread
            if self.nnotes[0].activation >= self.nnotes[0].threshold:
                self.nnotes[0].note_thread_start()
                self.nnotes[0].activation_index = 0
                self.nnotes[0].activation = 0.0
            if self.nnotes[1].activation >= self.nnotes[1].threshold:
                self.nnotes[1].note_thread_start()
                self.nnotes[1].activation_index = 0
                self.nnotes[1].activation = 0.0

            time.sleep(0.001)
        return

class NeuronSeq:
    def __init__(self):
        self.connections = []
        self.neurons = []
        self.nnotes = []
        return
    
    def add_connection(self, connection):
        self.connections.append(connection)
        #start connection thread
        connection.start()
        return
    
    def get_nnotes(self):
        nnotes = []
        for connection in self.connections:
            nnotes.append(connection.get_nnotes()[0])
            nnotes.append(connection.get_nnotes()[1])
        return nnotes
    
    def get_connections(self):
        return self.connections
    
    def set_threshold(self, connection_idx, nnote_idx, threshold):
        self.connections[connection_idx].get_nnote(nnote_idx).set_threshold(threshold)
        return
    
    def get_threshold(self, connection_idx, nnote_idx):
        return self.connections[connection_idx].get_nnote(nnote_idx).get_threshold()
    
    def set_midi_note(self, connection_idx, nnote_idx, note):
        self.connections[connection_idx].get_nnote(nnote_idx).set_note(note)
        return
    
    def get_midi_note(self, connection_idx, nnote_idx):
        return self.connections[connection_idx].get_nnote(nnote_idx).note
    
    def set_midi_velocity(self, connection_idx, nnote_idx, velocity):
        self.connections[connection_idx].get_nnote(nnote_idx).set_velocity(velocity)
        return
    
    def get_midi_velocity(self, connection_idx, nnote_idx):
        return self.connections[connection_idx].get_nnote(nnote_idx).velocity
    
    def set_midi_duration(self, connection_idx, nnote_idx, duration):
        self.connections[connection_idx].get_nnote(nnote_idx).set_duration(duration)
        return
    
    def get_midi_duration(self, connection_idx, nnote_idx):
        return self.connections[connection_idx].get_nnote(nnote_idx).duration
    
    def set_weight_0_to_1(self, connection_idx, weight):
        self.connections[connection_idx].set_weight(0, weight)
        return
    
    def get_weight_0_to_1(self, connection_idx):
        return self.connections[connection_idx].get_weight(0)
    
    def set_weight_1_to_0(self, connection_idx, weight):
        self.connections[connection_idx].set_weight(1, weight)
        return
    
    def get_weight_1_to_0(self, connection_idx):
        return self.connections[connection_idx].get_weight(1)
    

    
    def change_parameter(self, connection_idx, nnote_idx, parameter_idx, parameter_value):
        if parameter_idx==THRESHOLD_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_threshold(parameter_value)
        elif parameter_idx==MIDI_NOTE_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_note(parameter_value)
        elif parameter_idx==MIDI_VELOCITY_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_velocity(parameter_value)
        elif parameter_idx==MIDI_DURATION_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_duration(parameter_value)
        elif parameter_idx==WEIGHT_0_1_PARAMETER:
            self.connections[connection_idx].set_weight(0, parameter_value)
        elif parameter_idx==WEIGHT_1_0_PARAMETER:
            self.connections[connection_idx].set_weight(1, parameter_value)
        return
    
    def get_parameter(self, connection_idx, nnote_idx, parameter_idx):
        if parameter_idx==THRESHOLD_PARAMETER:
            return self.connections[connection_idx].get_nnote(nnote_idx).get_threshold()
        elif parameter_idx==MIDI_NOTE_PARAMETER:
            return self.connections[connection_idx].get_nnote(nnote_idx).note
        elif parameter_idx==MIDI_VELOCITY_PARAMETER:
            return self.connections[connection_idx].get_nnote(nnote_idx).velocity
        elif parameter_idx==MIDI_DURATION_PARAMETER:
            return self.connections[connection_idx].get_nnote(nnote_idx).duration
        elif parameter_idx==WEIGHT_0_1_PARAMETER:
            return self.connections[connection_idx].get_weight(0)
        elif parameter_idx==WEIGHT_1_0_PARAMETER:
            return self.connections[connection_idx].get_weight(1)
        return
    
    def create_nnote(self, channel=0, note=0, velocity=0, duration=0.0, id="NNote"):
        nnote = NNote()
        nnote.set_note(note)
        nnote.set_velocity(velocity)
        nnote.set_duration(duration)
        nnote.set_activation_function(NEURON_ACTIVATION_FUNCTION_LINEAR)
        nnote.set_threshold(1.0)
        nnote.channel = channel
        self.nnotes.append(nnote)
        return nnote
    
    def create_connection(self, name, nnote1_idx, nnote2_idx, weight_0_to_1=0.0, weight_1_to_0=0.0):
        connection = Connection(name, self.nnotes[nnote1_idx], self.nnotes[nnote2_idx], weight_0_to_1, weight_1_to_0)
        self.connections.append(connection)
        #start connection thread
        connection.start()
        return connection

    def get_connection_name(self, connection_idx):
        return self.connections[connection_idx].name
    
if __name__ == "__main__": 
    #usage example
    ns = NeuronSeq()

    #create 6 NNotes
    kick = NNote(channel=0, note=KICK, velocity=127, duration=0.1, id="kick")
    snare = NNote(channel=0, note=SNARE, velocity=127, duration=0.1, id="snare")
    closed_hihat = NNote(channel=0, note=CLOSED_HIHAT, velocity=127, duration=0.1, id="closed_hihat")
    open_hihat = NNote(channel=0, note=OPEN_HIHAT, velocity=127, duration=0.1, id="open_hihat")
    crash = NNote(channel=0, note=CRASH, velocity=127, duration=0.1, id="crash")
    ride = NNote(channel=0, note=RIDE, velocity=127, duration=0.1, id="ride")

    #change activation function
    kick.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)
    snare.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)
    closed_hihat.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)
    open_hihat.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)
    crash.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)
    ride.set_activation_function(NEURON_ACTIVATION_FUNCTION_SIGMOID)

    #add NNotes to NeuronSeq
    ns.add_connection(Connection(kick, snare, weight_0_to_1=0.0001, weight_1_to_0=-0.0001))
    ns.add_connection(Connection(snare, closed_hihat, weight_0_to_1=0.002, weight_1_to_0=0.002))
    ns.add_connection(Connection(closed_hihat, open_hihat, weight_0_to_1=-0.001, weight_1_to_0=-0.001))
    ns.add_connection(Connection(open_hihat, crash, weight_0_to_1=-0.001, weight_1_to_0=-0.001))
    ns.add_connection(Connection(crash, ride, weight_0_to_1=-0.001, weight_1_to_0=-0.001))
    ns.add_connection(Connection(ride, kick, weight_0_to_1=0.008, weight_1_to_0=0.008))

