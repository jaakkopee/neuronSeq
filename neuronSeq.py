import time
import mido
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()

class NNote (threading.Thread):
    def __init__(self, note=60, velocity=100, duration = 0.5, notename="midinote"):
        threading.Thread.__init__(self)

        self.notename = notename #for debugging mainly
        
        #MIDI settings
        #velocity and duration will be set by the NN ... possibly ... we'll see
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_off = mido.Message('note_off', note = note).bytes()
        self.note_length = duration

        #NN settings
        self.activation = 0.0
        self.addToCounter = 0.001
        self.threshold = 6666.6
        self.connections = [] #connections and weights

        self.tfunc = "linear"

        #Operational settings
        self.running = True
        
    def setNote(self, note=60 , velocity=100, duration=0.5):
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_length = duration
        self.note_off = mido.Message('note_off', note = note).bytes()
        return

    def setTransferFunction(self, tf = "linear"):
        self.tfunc = tf
        return
    
    def transferFunction(self):
        input = self.activation #no need to pass this in function call
        if self.tfunc == "linear":
            return input

        if self.tfunc == "sigmoid":
            return 0.0 #to be implemented!!!!

        if self.tfunc == "heaviside":
            if input > self.threshold/2:
                return self.threshold
            else: return 0.0

        return 0.0
    
    def bang(self):
        midiout.send_message(self.note_on)
        time.sleep(self.note_length)
        midiout.send_message(self.note_off)
        self.activation = 0.0
        return
    
    def runSwitch(self, runner):
        self.running = runner #boolean
        return

    def stopSeq (self):
        self.running = False
        return
    
    def addConnection(self, nnote, strength):
        self.connections += [[nnote, strength]]
        #print self.name +": "+ str(self.connections)
        return

    def setConnectionWeight(self, connectionIndex, newWeight):
        self.connections[connectionIndex][1] = newWeight
        return
    
    def setNNParams(self, activation = 0.0, addToCounter = 0.001, threshold=6666.6):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold
        return
    
    def getActivation(self):
        #print self.name + " getActivation()"
        self.activation += self.addToCounter

        if self.connections:
            for i in self.connections:
                self.activation += i[0].getActivation() * i[1]

        outputValue = self.transferFunction()
                
        if outputValue >= self.threshold:
            
            #bang is in a new thread so that calculating activation continues
            num_threads = threading.activeCount()

            #threads are limited to conserve memory
            #and to filter NN:s output from too many strikes at one instant
            if num_threads < 10:
                t1 = threading.Thread(target = self.bang)
                t1.start()
            
        return self.activation
    
    def cleanup(self):
        midiout.cleanup()
        return
    
    def run(self):
        while self.running:
            self.getActivation()
        return

