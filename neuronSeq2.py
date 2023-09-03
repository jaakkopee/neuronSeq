#complete rewrite of neuronSeq.py

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd
import os
import sys
import time
import copy
import pickle
import threading
import queue
import subprocess
import platform
import re
import socket
import struct
import select
import json
import rtmidi

#global variables
#neuron parameters
ACTIVATION_PARAMETER = 0
ADC_PARAMETER = 1
THRESHOLD_PARAMETER = 2
MIDI_NOTE_PARAMETER = 3
MIDI_VELOCITY_PARAMETER = 4
MIDI_DURATION_PARAMETER = 5
WEIGHT_0_1_PARAMETER = 6
WEIGHT_1_0_PARAMETER = 7
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
    def __init__(self, nnote1, nnnote2, weight_0_to_1=0.0, weight_1_to_0=0.0):
        threading.Thread.__init__(self)
        self.weights = (weight_0_to_1, weight_1_to_0)
        self.nnotes = (nnote1, nnnote2)

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
