import time
import mido
import rtmidi
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()

print ("neuronSeq by Jaakko Prattala 2019-2020. Use freely.")

       
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

            #the weight here is for connection from the second neuron to the first
            self.note[0].activation += self.note[1].activation * self.weight[1] + self.note[0].addToCounter
            #and here for connection from the first to the second
            self.note[1].activation += self.note[0].activation * self.weight[0] + self.note[1].addToCounter
            
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
    def __init__(self, note=60, velocity=100, duration = 0.2, notename="midinote", channel = 1):
        self.notename = notename
        
        #MIDI settings
        #velocity and duration will be set by the NN ... possibly ... we'll see
        self.channel = channel

        midiMsg = rtmidi.MidiMessage()


        #set MIDI message params
        self.note_on = midiMsg.noteOn(self.channel, note, velocity)
        self.note_off = midiMsg.noteOff(self.channel, note)

        #time to sleep between note on and note off
        self.note_length = duration

        #NN settings
        self.activation = 0.0
        self.addToCounter = 0.0001
        self.threshold = 1.0
        
    def setNote(self, note=60 , velocity=100, duration=0.2, channel = 1):
        self.channel = channel
        
        midiMsg = rtmidi.MidiMessage()

        #set MIDI message params                                                                                                                                                                           
        self.note_on = midiMsg.noteOn(self.channel, note, velocity)
        self.note_off = midiMsg.noteOff(self.channel, note)

        self.note_length = duration

    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold
        return

    def bang(self):
        midiout.send_message(self.note_on)
        
        #BEGIN DEBUG
        #print("I just send a midi message\non channel: " + str(self.note_on.getChannel())\
        #          + "\nnote nro: " + str(self.note_on.getNoteNumber())\
        #          + "\nvelocity: " + str(self.note_on.getVelocity())+"\n")
        #END DEBUG
       
        time.sleep(self.note_length)
        midiout.send_message(self.note_off)
        return
