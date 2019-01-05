import time
import mido
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()
print "neuronSeq by Jaakko Prattala 2019. Use freely."

       
class Connection (threading.Thread):
    def __init__(self, note0, note1, weight0, weight1):
        threading.Thread.__init__(self)

        self.note = [note0, note1]
        self.weight = [weight0, weight1]
        self.running = True
       

       
    def run(self):
        while self.running:
            #Two-way activation:set weights to >0.0, One-way: set either weight to 0.0, free oscillation: set both weights to 0.0
            self.note[0].activation += self.note[1].activation * self.weight[0] + self.note[0].addToCounter
            self.note[1].activation += self.note[0].activation * self.weight[1] + self.note[1].addToCounter
            
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
    def __init__(self, note=60, velocity=100, duration = 0.2, notename="midinote"):
        self.notename = notename
        
        #MIDI settings
        #velocity and duration will be set by the NN ... possibly ... we'll see
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_off = mido.Message('note_off', channel=0, note = note, velocity=0).bytes()
        self.note_length = duration

        #NN settings
        self.activation = 0.0
        self.addToCounter = 0.0001
        self.threshold = 1.0
        
    def setNote(self, note=60 , velocity=100, duration=0.2):
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_length = duration
        self.note_off = mido.Message('note_off', channel=0, note = note, velocity=0).bytes()
        return
    
    def bang(self):
        #when a neuron reaches threshold, e.g. fires, two things happen:
        #first, activation is set 0.0 (in getActivation())
        #second, a MIDI note is played (here)
        midiout.send_message(self.note_on)
        time.sleep(self.note_length)
        midiout.send_message(self.note_off)
        return
    
    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold
        return
