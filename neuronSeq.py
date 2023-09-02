import time
import rtmidi
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()

print ("\n\nneuronSeq by Jaakko Prattala 2019-2020. Use freely.\n\n\n")

ACTIVATION_PARAMETER = 0
ADC_PARAMETER = 1
THRESHOLD_PARAMETER = 2
MIDI_NOTE_PARAMETER = 3
MIDI_VELOCITY_PARAMETER = 4
MIDI_DURATION_PARAMETER = 5

def get_param_name(parameter_idx):
    if parameter_idx == ACTIVATION_PARAMETER:
        return "activation"
    elif parameter_idx == ADC_PARAMETER:
        return "adc"
    elif parameter_idx == THRESHOLD_PARAMETER:
        return "threshold"
    elif parameter_idx == MIDI_NOTE_PARAMETER:
        return "midi note"
    elif parameter_idx == MIDI_VELOCITY_PARAMETER:
        return "midi velocity"
    elif parameter_idx == MIDI_DURATION_PARAMETER:
        return "midi duration"
    else:
        return "error"

class Connection (threading.Thread):
    def __init__(self, note0, note1, weight0to1, weight1to0):
        threading.Thread.__init__(self)

        self.note = [note0, note1]
        self.weight = [weight0to1, weight1to0]
        self.running = True
       
    def run(self):
        while self.running:
            #Two-way activation:set weights to >0.0,
            #One-way: set either weight to 0.0, other to >0.0
            #free oscillation: set both weights to 0.0

            #handling negative activation values, this is the hacker's duct tape: arbitrary threshold values.
            if (self.note[0].activation < -100000.0):
                self.note[0].activation = 0.0
            if (self.note[1].activation < -100000.0):
                self.note[1].activation == 0.0

            #Calculate Activation:
            #   Connection from the first neuron (note[0]) to the second (note[1]) increases activation of note[1]
            #   Notice also addToCounter, which is a constant added to note[1]'s activation on each interation of Connection.run()'s while loop.
            self.note[1].activation += self.note[0].activation * self.weight[0] + self.note[1].addToCounter
            #   ...and here connection from the second to the first, by which activation of note[0] is increased + addToCounter.
            self.note[0].activation += self.note[1].activation * self.weight[1] + self.note[0].addToCounter
            
            #Compare activation to threshold:
            #   If activation reaches treshold, it is set to zero and NNote.bang()-function is awakened.
            if self.note[0].activation >= self.note[0].threshold:
                self.note[0].activation = 0.0
                num_threads = threading.activeCount()
                if num_threads < 2000:
                    t0 = threading.Thread(target = self.note[0].bang)
                    t0.start()            

            if self.note[1].activation >= self.note[1].threshold:
                self.note[1].activation = 0.0
                num_threads = threading.activeCount()
                if num_threads < 2000:
                    t1 = threading.Thread(target = self.note[1].bang)
                    t1.start()            

        return

    def stopSeq(self):
        self.running = False

    def cleanup(self):
        midiout.cleanup() #closes port for all NNotes!!!
        return



class NNote:
    def __init__(self, note=60, velocity=100, duration = 0.2, id = "", channel = 1, activation = 0.0, addToCounter = 0.0001, threshold = 1.0, parameter_modulation_hub = None):

        self.id = self.setId(id)
        self.infostr = ""
        self.channel = channel
        self.note_length = duration
        self.velocity = velocity
        self.midinote = note
        self.midiout = midiout

        #MIDI settings:
        #   Velocity and duration will be set by the NN eventually.

        midiMsg = rtmidi.MidiMessage()

        #   set MIDI message params
        self.note_on = midiMsg.noteOn(self.channel, self.midinote, self.velocity)
        self.note_off = midiMsg.noteOn(self.channel, self.midinote, 0)

        #NN settings:
        self.activation = activation #Initial activation level.
        self.addToCounter = addToCounter #Activation increase per call to Connection.run().
        self.threshold = threshold #Activation threshold, which, when reached, results to activation set to 0.0 and NNote.bang() is called.

        self.infostr += self.id + " " + str(self.note_on) +"\n"+ str(self.note_off)
        self.infostr += "\n" + "Duration: "+str(self.note_length)
        self.infostr += "\n"+ "Neural Network Parameters:\n"
        self.infostr += "Activation level: "+ str(self.activation)+"\n"
        self.infostr += "Activation counter increase: "+ str(self.addToCounter)+"\n"
        self.infostr += "Activation threshold: " + str(self.threshold)+"\n\n\n"

        print ("Constructed a neuron: " + str(self))

    def setId(self, id):
        if id == "":
            id = "NNote"
        return id

    def setNote(self, note=60 , velocity=100, duration=0.2, channel = 1):
        self.channel = channel
        self.midinote = note
        self.velocity = velocity
        self.note_length = duration
        self.channel = channel

        midiMsg = rtmidi.MidiMessage()

        #set MIDI message params                                                                                                                                                                           
        self.note_on = midiMsg.noteOn(self.channel, self.midinote, self.velocity)
        #NOTE_OFF equals NOTE_ON with velocity 0
        self.note_off = midiMsg.noteOn(self.channel, self.midinote, 0)

        #Update info string
        self.infostr = self.id + " " + str(self.note_on) + "\n" + str(self.note_off)
        self.infostr += "\n" + "Duration: "+str(self.note_length)
        self.infostr += "\n"+ "Neural Network Parameters:\n"
        self.infostr += "Activation level: "+ str(self.activation)+"\n"
        self.infostr += "Activation counter increase: "+ str(self.addToCounter)+"\n"
        self.infostr += "Activation threshold: " + str(self.threshold)+"\n\n\n"

        print("Note data parameter change: "+ str(self))

        return

    def set_activation(self, activation):
        self.activation = activation
        return
    
    def get_activation(self):
        return self.activation

    def set_adc(self, adc):
        self.addToCounter = adc
        return
    
    def get_adc(self):
        return self.addToCounter
    
    def set_threshold(self, threshold):
        self.threshold = threshold
        return
    
    def get_threshold(self):
        return self.threshold
    
    def set_midi_note(self, note):
        self.note = note
        return
    
    def get_midi_note():
        return self.note
    
    def set_midi_velocity(self, velocity):
        self.velocity = velocity
        return
    
    def get_midi_velocity(self):
        return self.velocity
    
    def set_midi_duration(self, duration):
        self.note_length = duration
        return
    
    def get_midi_duration(self):
        return self.note_length
     
    
    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold

        self.infostr = self.id +" "+ str(self.note_on)+"\n"+str(self.note_off)
        self.infostr += "\n" + "Duration: "+str(self.note_length)
        self.infostr += "\n"+ "Neural Network Parameters:\n"
        self.infostr += "Activation level: "+ str(self.activation)+"\n"
        self.infostr += "Activation counter increase: "+ str(self.addToCounter)+"\n"
        self.infostr += "Activation threshold: " + str(self.threshold)+"\n\n\n"

        print("Neural Network parameter change:\n"+ str(self))
        
        return

    def bang(self):

        #Output MIDI data (a NOTE_ON event)
        midiout.send_message(self.note_on)
        
        #BEGIN DEBUG
        #print("I just send a midi message\non channel: " + str(self.note_on.getChannel())\
        #          + "\nnote nro: " + str(self.note_on.getNoteNumber())\
        #          + "\nvelocity: " + str(self.note_on.getVelocity())+"\n")
        #END DEBUG

        #wait for the duration of the note
        time.sleep(self.note_length)
        #...and send a NOTE_OFF MIDI event
        midiout.send_message(self.note_off)
        return

    def __str__(self):
        return self.infostr

class ParameterModulationHub:
    
    def __init__(self):
        self.connection_list = []
        self.modulators = []
        self.running = True
        self.mod_threads = [] 

    def get_parameter_list(self):
        parameter_list = []
        for conn in range(len(self.connection_list)):
            for note in range(2):
                for parameter_idx in range(6):
                    parameter_list.append((conn, note, parameter_idx))

        return parameter_list
        
    def add_connection(self, connection):
        self.connection_list.append(connection)
        connection.start()
        return        

    def get_connection_list_length(self):
        return len(self.connection_list)
    
    def change_parameter(self, connection_idx, neuron_idx, parameter_idx, value):
        for conn in self.connection_list:
            if conn.note[neuron_idx] == self.connection_list[connection_idx].note[neuron_idx]:
                if parameter_idx == ACTIVATION_PARAMETER:
                    conn.note[neuron_idx].set_activation(value)
                elif parameter_idx == ADC_PARAMETER:
                    conn.note[neuron_idx].set_adc(value)
                elif parameter_idx == THRESHOLD_PARAMETER:
                    conn.note[neuron_idx].set_threshold(value)
                elif parameter_idx == MIDI_NOTE_PARAMETER:
                    conn.note[neuron_idx].set_midi_note(value)
                elif parameter_idx ==  MIDI_VELOCITY_PARAMETER:
                    conn.note[neuron_idx].set_midi_velocity(value)
                elif parameter_idx ==  MIDI_DURATION_PARAMETER:
                    conn.note[neuron_idx].set_midi_duration(value)
                    
                else:
                    print("Error: parameter index out of range")

    def reset_parameter(self, connection_idx, neuron_idx, parameter_idx):
        for conn in self.connection_list:
            if conn.note[neuron_idx] == self.connection_list[connection_idx].note[neuron_idx]:
                if parameter_idx == ACTIVATION_PARAMETER:
                    conn.note[neuron_idx].set_activation(0.0)
                elif parameter_idx == ADC_PARAMETER:
                    conn.note[neuron_idx].set_adc(0.0001)
                elif parameter_idx == THRESHOLD_PARAMETER:
                    conn.note[neuron_idx].set_threshold(1.0)
                elif parameter_idx == MIDI_NOTE_PARAMETER:
                    conn.note[neuron_idx].set_midi_note(60)
                elif parameter_idx ==  MIDI_VELOCITY_PARAMETER:
                    conn.note[neuron_idx].set_midi_velocity(100)
                elif parameter_idx ==  MIDI_DURATION_PARAMETER:
                    conn.note[neuron_idx].set_midi_duration(0.2)
                else:
                    print("Error: parameter index out of range")
                    
    def add_modulator(self, modulator):
        self.modulators.append(modulator)
        #activate modulator
        modulation_thread = threading.Thread(target = modulator.run)
        modulation_thread.start()
        self.mod_threads.append(modulation_thread)
        return
    
    def stop_modulator(self, modulator_idx):
        self.mod_threads[modulator_idx].join()
        return
    
    def stop_all_modulators(self):
        for modulator in self.mod_threads:
            modulator.join()
        return
        
class SineModulator:
    def __init__(self, connection_idx, neuron_idx, parameter_idx, amplitude = 0.0, frequency = 0.0, phase = 0.0, offset = 0.0, parameter_modulation_hub = None):
        self.connection_idx = connection_idx
        self.neuron_idx = neuron_idx
        self.parameter_idx = parameter_idx
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.offset = offset
        self.parameter_modulation_hub = parameter_modulation_hub

    def run(self):
    
        #calculate modulation value
        modulation_value = self.amplitude * math.sin(self.frequency * time.time() + self.phase) + self.offset
        #change parameter
        self.parameter_modulation_hub.change_parameter(self.connection_idx, self.neuron_idx, self.parameter_idx, modulation_value)
        #wait for 1 ms
        time.sleep(0.001)
        return

class SawModulator:
    def __init__(self, connection_idx, neuron_idx, parameter_idx, amplitude = 0.0, frequency = 0.0, phase = 0.0, offset = 0.0, parameter_modulation_hub = None):
        self.connection_idx = connection_idx
        self.neuron_idx = neuron_idx
        self.parameter_idx = parameter_idx
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.offset = offset
        self.parameter_modulation_hub = parameter_modulation_hub

    def run(self):
    
        #calculate modulation value
        modulation_value = self.amplitude * (time.time() * self.frequency + self.phase) % 1.0 + self.offset
        #change parameter
        self.parameter_modulation_hub.change_parameter(self.connection_idx, self.neuron_idx, self.parameter_idx, modulation_value)
        #wait for 1 ms
        time.sleep(0.001)
        return
    
class SquareModulator:
    def __init__(self, connection_idx, neuron_idx, parameter_idx, amplitude = 0.0, frequency = 0.0, phase = 0.0, offset = 0.0, parameter_modulation_hub = None):
        self.connection_idx = connection_idx
        self.neuron_idx = neuron_idx
        self.parameter_idx = parameter_idx
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.offset = offset
        self.parameter_modulation_hub = parameter_modulation_hub

    def run(self):
    
        #calculate modulation value
        modulation_value = self.amplitude * math.copysign(1, math.sin(self.frequency * time.time() + self.phase)) + self.offset
        #change parameter
        self.parameter_modulation_hub.change_parameter(self.connection_idx, self.neuron_idx, self.parameter_idx, modulation_value)
        #wait for 1 ms
        time.sleep(0.001)
        return
    
def main():
    #create four NNotes
    kick = NNote(id = "Kick", note = 36, velocity = 100, duration = 0.1, channel = 1, activation = 0.0, addToCounter = 0.00000000000000030303, threshold = 1.0)
    snare = NNote(id = "Snare", note = 38, velocity = 100, duration = 0.1, channel = 1, activation = 0.0, addToCounter = 0.00000000000000030303, threshold = 1.0)
    hihat = NNote(id = "Hihat", note = 42, velocity = 100, duration = 0.1, channel = 1, activation = 0.0, addToCounter = 0.00000000000000030303, threshold = 1.0)
    bass01 = NNote(id = "Bass01", note = 48, velocity = 100, duration = 0.1, channel = 1, activation = 0.0, addToCounter = 0.00000000000000030303, threshold = 1.0)

    #create three connections
    drumConnection00 = Connection(kick, snare, 0.00000121, 0.00000121)
    dc00_idx = 0
    dc00_kick_idx = 0
    dc00_snare_idx = 1
    drumConnection01 = Connection(snare, hihat, 0.00000121, 0.00000121)
    dc01_idx = 1
    dc01_snare_idx = 0
    dc01_hihat_idx = 1
    drumConnection02 = Connection(hihat, kick, 0.00000121, 0.00000121)
    dc02_idx = 2
    dc02_hihat_idx = 0
    dc02_kick_idx = 1

    #create two connections
    bassConnection00 = Connection(bass01, kick, 0.00000121, 0.00000121)
    bc00_idx = 3
    bc00_bass01_idx = 0
    bc00_kick_idx = 1

    bassConnection01 = Connection(bass01, snare, 0.00000121, 0.00000121)
    bc01_idx = 4
    bc01_bass01_idx = 0
    bc01_snare_idx = 1

    #create a parameter modulation hub
    parameter_modulation_hub = ParameterModulationHub()

    #create a sine modulator
    sine_modulator = SineModulator(dc00_idx, dc00_snare_idx, ACTIVATION_PARAMETER, amplitude = 0.0001, frequency = 0.1, phase = 0.0, offset = 0.0, parameter_modulation_hub = parameter_modulation_hub)

    #create a saw modulator
    saw_modulator = SawModulator(bc01_idx, bc01_bass01_idx, THRESHOLD_PARAMETER, amplitude = 0.0001, frequency = 0.1, phase = 0.0, offset = 0.0, parameter_modulation_hub = parameter_modulation_hub)

    #create a square modulator
    square_modulator = SquareModulator(bc00_idx, bc00_kick_idx, ACTIVATION_PARAMETER, amplitude = 0.0001, frequency = 0.1, phase = 0.0, offset = 0.0, parameter_modulation_hub = parameter_modulation_hub)

    #add connections to the hub
    parameter_modulation_hub.add_connection(drumConnection00)
    parameter_modulation_hub.add_connection(drumConnection01)
    parameter_modulation_hub.add_connection(drumConnection02)
    parameter_modulation_hub.add_connection(bassConnection00)
    parameter_modulation_hub.add_connection(bassConnection01)

    #start connections
    drumConnection00.start()
    drumConnection01.start()
    drumConnection02.start()
    bassConnection00.start()
    bassConnection01.start()
 
    #add modulators to the hub
    parameter_modulation_hub.add_modulator(sine_modulator)
    parameter_modulation_hub.add_modulator(saw_modulator)
    parameter_modulation_hub.add_modulator(square_modulator)

    time.sleep(1.0)

    #stop connections
    drumConnection00.stopSeq()
    drumConnection01.stopSeq()
    drumConnection02.stopSeq()
    bassConnection00.stopSeq()
    bassConnection01.stopSeq()

    #stop modulators
    parameter_modulation_hub.stop_all_modulators()

    #clean up
    drumConnection00.cleanup()

    time.sleep(3.0)

    return

if __name__ == "__main__":
    main()

