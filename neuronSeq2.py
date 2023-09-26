#complete rewrite of neuronSeq.py

import numpy as np
import time
import threading
import rtmidi
import networkx as nx
import math
import mido


#global variables
#neuron parameters
ACTIVATION_FUNCTION_PARAMETER = 0
THRESHOLD_PARAMETER = 1
MIDI_NOTE_PARAMETER = 2
MIDI_VELOCITY_PARAMETER = 3
MIDI_DURATION_PARAMETER = 4
WEIGHT_0_1_PARAMETER = 5
WEIGHT_1_0_PARAMETER = 6
ACT_BUFFER_SIZE_PARAMETER = 7

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

X_AXIS_LENGTH = 2**24

#midi output
MIDI_OUTPUT_PORT_NAME = "NeuronSeq"
MIDI_OUTPUT_PORT_NAME_DEFAULT = "NeuronSeq"
#get midi output ports from rtmidi
midi_output = rtmidi.MidiOut()
available_midi_output_ports = midi_output.get_port_count()
midi_output_port_name = MIDI_OUTPUT_PORT_NAME_DEFAULT
#try opening default port
if available_midi_output_ports:
    midi_output.open_port(0)
else:
    #open virtual port
    midi_output.open_virtual_port(midi_output_port_name)

#NNote is a neuron that outputs a midi events
#TODO: add parameter for len(X).
class NNote:
    def __init__(self, channel=0, note=0, velocity=0, duration=0.0, lenX=X_AXIS_LENGTH, id="NNote"):
        self.lenX = lenX
        self.note = note
        self.velocity = velocity
        self.duration = duration
        self.activation = 0.0
        self.activation_function = NEURON_ACTIVATION_FUNCTION_LINEAR
        self.activation_function_name = NEURON_ACTIVATION_FUNCTION_NAME_LINEAR
        self.id = id
        self.activation_index=0
        self.X = []
        self.Y = []
        self.create_activation_X_axis()
        self.create_activation_Y_axis()
        self.threshold = 1.0
        self.note_thread = None

        self.channel = channel        
        #self.midi_msg = rtmidi.midi_message()

        return
    
    def set_activation_buffer_size(self, lenX):
        self.lenX = lenX
        self.create_activation_X_axis()
        self.create_activation_Y_axis()
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
        self.X = np.arange(0, 1, 1/self.lenX)
        return
    
    def create_activation_Y_axis(self):
        if self.activation_function==NEURON_ACTIVATION_FUNCTION_LINEAR:
            self.Y = self.X
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_SIGMOID:
            temp_X = (self.X-0.5)*24
            self.Y = (1 / (1 + np.exp(-temp_X)))
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_TANH:
            self.Y = np.tanh(self.X)
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_RELU:
            self.Y = np.maximum(self.X, 0)
        elif self.activation_function==NEURON_ACTIVATION_FUNCTION_SOFTMAX:
            self.Y = np.exp(self.X) / np.sum(np.exp(self.X))
        return    

    def create_midi_event(self):
        #create midi event
        midi_event = mido.Message('note_on', note=self.note, velocity=self.velocity, channel=self.channel)
        return midi_event

    def create_midi_event_off(self):
        #create midi event
        midi_event = mido.Message('note_off', note=self.note, velocity=self.velocity, channel=self.channel)
        return midi_event

    def note_thread_start(self):
        #start thread
        self.note_thread = threading.Thread(target=self.execute_note_thread)
        self.note_thread.start()
        return
    
    def get_id(self):
        return self.id
            
    def execute_note_thread(self):
        #create midi event
        midi_event = self.create_midi_event()
        #send midi event
        midi_output.send_message(midi_event.bytes())
        #sleep for duration
        time.sleep(self.duration)
        #create midi event
        midi_event = self.create_midi_event_off()
        #send midi event
        midi_output.send_message(midi_event.bytes())
        return

    def advance_activation_index(self):
        self.activation_index += 1
        if self.activation_index >= len(self.X):
            self.activation_index = len(self.X)-1
        return self.Y[self.activation_index]
    
class Connection(threading.Thread):
    def __init__(self, name, nnote1, nnnote2, weight_0_to_1=0.0, weight_1_to_0=0.0):
        threading.Thread.__init__(self)
        self.weights = [weight_0_to_1, weight_1_to_0]
        self.nnotes = [nnote1, nnnote2]
        self.name = name
        self.source = nnote1
        self.destination = nnnote2
        self.weight_0_to_1 = weight_0_to_1
        self.weight_1_to_0 = weight_1_to_0
        self.running = True
        return
    
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
    
    def get_id(self):
        return self.name

    def run(self):
        while self.running:
            #calculate new activation
            self.nnotes[0].activation += self.nnotes[1].advance_activation_index() * self.weights[1]
            self.nnotes[1].activation += self.nnotes[0].advance_activation_index() * self.weights[0]

            if self.nnotes[0].activation < self.nnotes[0].Y[0]:
                self.nnotes[0].activation = self.nnotes[0].Y[0]
                self.nnotes[0].activation_index = 0
            if self.nnotes[1].activation < self.nnotes[1].Y[0]:
                self.nnotes[1].activation = self.nnotes[1].Y[0]
                self.nnotes[1].activation_index = 0

            #if activation reaches threshold, start note thread
            if self.nnotes[0].activation >= self.nnotes[0].Y[-1]:
                self.nnotes[0].note_thread_start()
                self.nnotes[0].activation_index = 0
                self.nnotes[0].activation = self.nnotes[0].Y[0]
            if self.nnotes[1].activation >= self.nnotes[1].Y[-1]:
                self.nnotes[1].note_thread_start()
                self.nnotes[1].activation_index = 0
                self.nnotes[1].activation = self.nnotes[1].Y[0]

            time.sleep(0.001)

        return
    def stop(self):
        self.running=False
        return
    


class NeuronSeq:
    def __init__(self):
        self.connections = []
        self.nnotes = []
        return
       
    def neuron_list_string(self):
        neuron_list_string = ""
        for nnote in self.nnotes:
            neuron_list_string += nnote.id + " "+ str(nnote.note)  + ", "
        neuron_list_string += "\n"
        for connection in self.connections:
            neuron_list_string += connection.name + ": " + connection.nnotes[0].id + " " + connection.nnotes[1].id + ", "
        return neuron_list_string
    
    def get_nnotes(self):
        return self.nnotes
    
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
        if parameter_idx==ACTIVATION_FUNCTION_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_activation_function(parameter_value)
            print ("Activation Function set to", self.connections[connection_idx].get_nnote(nnote_idx).get_activation_function_name())
        if parameter_idx==THRESHOLD_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_threshold(parameter_value)
            print ("Threshold set to", self.connections[connection_idx].get_nnote(nnote_idx).get_threshold())
        elif parameter_idx==MIDI_NOTE_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_note(parameter_value)
            print ("MIDI Note set to", self.connections[connection_idx].get_nnote(nnote_idx).note)
        elif parameter_idx==MIDI_VELOCITY_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_velocity(parameter_value)
            print ("MIDI Velocity set to", self.connections[connection_idx].get_nnote(nnote_idx).velocity)
        elif parameter_idx==MIDI_DURATION_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_duration(parameter_value)
            print ("Duration set to", self.connections[connection_idx].get_nnote(nnote_idx).duration)
        elif parameter_idx==WEIGHT_0_1_PARAMETER:
            self.connections[connection_idx].set_weight(0, parameter_value)
            print ("Weight 0->1 set to", self.connections[connection_idx].get_weight(0))
        elif parameter_idx==WEIGHT_1_0_PARAMETER:
            self.connections[connection_idx].set_weight(1, parameter_value)
            print ("Weight 1->0 set to", self.connections[connection_idx].get_weight(1))
        elif parameter_idx==ACT_BUFFER_SIZE_PARAMETER:
            self.connections[connection_idx].get_nnote(nnote_idx).set_activation_buffer_size(parameter_value)
            print ("Activation buffer size set to", self.connections[connection_idx].get_nnote(nnote_idx).lenX)
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
    
    def create_nnote(self, channel=0, note=0, velocity=0, duration=0.0, lenX=X_AXIS_LENGTH, id="NNote"):
        nnote = NNote()
        nnote.lenX = lenX
        nnote.create_activation_X_axis()
        nnote.create_activation_Y_axis()
        nnote.set_note(note)
        nnote.set_velocity(velocity)
        nnote.set_duration(duration)
        nnote.set_threshold(1.0)
        nnote.id = id
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
    
    def get_neuron_graph_data_act_func(self):
        neuron_graph_data = []
        for nnote in self.nnotes:
            neuron_graph_data.append(nnote.X)
            neuron_graph_data.append(nnote.Y)
        return neuron_graph_data
    
    def stop(self):
        for connection in self.connections:
            connection.stop()
            connection.join()
        return
    
def get_angle(angle, add_to_angle):
    new_angle = angle+add_to_angle
    return new_angle%360

class DistanceVector():
    def __init__(self, nx_point):
        self.nx_point = nx_point
        #calculate angle in radians
        self.angle = math.atan2(0, 0) - math.atan2(self.nx_point[1], self.nx_point[0]) 
        #convert to degrees
        self.angle = math.degrees(self.angle)
        self.vector_length = math.sqrt(self.nx_point[0]**2 + self.nx_point[1]**2)
        self.update_nx_point()

    def change_angle(self, add_to_angle):
        self.angle = get_angle(self.angle, add_to_angle)
        return self.update_nx_point()
    
    def set_coordinates(self, nx_point):
        self.nx_point = nx_point
        self.vector_length = math.sqrt(self.nx_point[0]**2 + self.nx_point[1]**2)
        self.angle = math.atan2(0, 0) - math.atan2(self.nx_point[1], self.nx_point[0])
        self.angle = math.degrees(self.angle)
        return self
    
    def get_vector_length(self):
        return self.vector_length
    
    def set_vector_length(self, vector_length):
        self.vector_length = vector_length
        return self.update_vector_length()
    
    def update_vector_length(self):
        vector_length = self.vector_length
        new_x = self.nx_point[0]/vector_length
        new_y = self.nx_point[1]/vector_length
        self.nx_point = (new_x, new_y)
        return self

    def update_nx_point(self):
        x, y = self.nx_point
        #𝑥′=𝑥cos𝜃−𝑦sin𝜃
        #𝑦′=𝑥sin𝜃+𝑦cos𝜃
        #rotate point around origin

        new_x = x*math.cos(math.radians(self.angle)) - y*math.sin(math.radians(self.angle))
        new_y = x*math.sin(math.radians(self.angle)) + y*math.cos(math.radians(self.angle))

        self.vector_length = math.sqrt(new_x**2 + new_y**2)
        self.nx_point = (new_x, new_y)
        return self
        
    def get_coordinates(self):
        return self.nx_point
    
    def get_vector_length(self):
        return self.vector_length
    
    
# Define rotation functions
def rotate_graph(distance_vector, add_to_angle):
    distance_vector = distance_vector.change_angle(add_to_angle)
    return distance_vector
    
# network graph class
class NetworkGraph():
    def __init__(self, neuronSeq):
        self.neuronSeq = neuronSeq
        self.DVpos = {}
        self.maxX = 0.001
        self.maxY = 0.001

    def add_nnote(self, midi_channel=0, note=0, velocity=0, duration=0.0, lenX=X_AXIS_LENGTH ,id="NNote"):
        #create the neuron/note object
        new_nnote = self.neuronSeq.create_nnote(midi_channel, note, velocity, duration, lenX, id)
        x1, y1 = np.random.uniform(-32.0, 32.0), np.random.uniform(-32.0, 32.0)
        self.DVpos[new_nnote.get_id()] = DistanceVector((x1, y1))
        self.maxX = max(self.maxX, x1)
        self.maxY = max(self.maxY, y1)
        return new_nnote, self.DVpos[new_nnote.get_id()]

    def add_connection(self, name, nnote1_idx, nnote2_idx, weight_0_to_1=0.0, weight_1_to_0=0.0):
        #create the connection object
        new_connection = self.neuronSeq.create_connection(name, nnote1_idx, nnote2_idx, weight_0_to_1, weight_1_to_0)
        self.DVpos[new_connection.get_id()] = (DistanceVector(self.DVpos[new_connection.get_nnotes()[0].get_id()].get_coordinates()), DistanceVector(self.DVpos[new_connection.get_nnotes()[1].get_id()].get_coordinates()))
        return new_connection, self.DVpos[new_connection.get_id()]

    def rotate(self, angle_change):
        for nnote in self.neuronSeq.get_nnotes():
            self.DVpos[nnote.get_id()] = rotate_graph(self.DVpos[nnote.get_id()], angle_change)
        for connection in self.neuronSeq.get_connections():
            self.DVpos[connection.get_id()] = (self.DVpos[self.neuronSeq.get_nnotes()[0].get_id()], self.DVpos[self.neuronSeq.get_nnotes()[1].get_id()])
        #update DVpos to maxX and maxY
        self.maxX = 0.001
        self.maxY = 0.001
        for nnote in self.neuronSeq.get_nnotes():
            self.maxX = max(self.maxX, self.DVpos[nnote.get_id()].get_coordinates()[0])
            self.maxY = max(self.maxY, self.DVpos[nnote.get_id()].get_coordinates()[1])

        return
    
    def position_nodes_circle(self):
        #position nodes in a circle
        angle = 0
        angle_change = 360/len(self.neuronSeq.get_nnotes())
        for nnote in self.neuronSeq.get_nnotes():
            self.DVpos[nnote.get_id()] = DistanceVector((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
            angle += angle_change
        #position connections
        for connection in self.neuronSeq.get_connections():
            self.DVpos[connection.get_id()] = (self.DVpos[self.neuronSeq.get_nnotes()[0].get_id()], self.DVpos[self.neuronSeq.get_nnotes()[1].get_id()])      

        return
    
    
