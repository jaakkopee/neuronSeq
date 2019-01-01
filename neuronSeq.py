import time
import mido
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()

class NNote (threading.Thread):
    def __init__(self, note=60, velocity=100, duration = 0.2, notename="midinote", transferFunction="linear"):
        threading.Thread.__init__(self)

        self.notename = notename #for debugging mainly
        
        #MIDI settings
        #velocity and duration will be set by the NN ... possibly ... we'll see
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_off = mido.Message('note_off', channel=0, note = note, velocity=0).bytes()
        self.note_length = duration

        #NN settings
        self.activation = 0.0
        self.addToCounter = 0.0001
        self.threshold = 1.0
        self.connections = [] #connections and weights

        self.tfunc = transferFunction

        #Operational settings
        self.running = True
        
    def setNote(self, note=60 , velocity=100, duration=0.2):
        self.note_on = mido.Message('note_on', channel=0, note = note, velocity = velocity).bytes()
        self.note_length = duration
        self.note_off = mido.Message('note_off', channel=0, note = note, velocity=0).bytes()
        return

    def setTransferFunction(self, tf = "linear"):
        self.tfunc = tf
        return
    
    def transferFunction(self):
        input = self.activation #no need to pass this in function call
        if self.tfunc == "linear":
            return input

        if self.tfunc == "sigmoid":
            return 0.0 #to be implemented!!!! possibly have to scale activation to 0.0 ... 1.0

        if self.tfunc == "heaviside":
            if input > self.threshold/2: #something wrong here...
                return self.threshold
            else: return 0.0

        return 0.0
    
    def bang(self):
        #when a neuron reaches threshold, e.g. fires, two things happen:
        #first, activation is set 0.0
        #second, a MIDI note is played
        self.activation = 0.0
        midiout.send_message(self.note_on)
        time.sleep(self.note_length)
        midiout.send_message(self.note_off)
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
    
    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
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

        outputValue = self.transferFunction() #transfer functions do not work atm. use "linear".
                
        if outputValue >= self.threshold:
            
            num_threads = threading.activeCount()
            
            #set max threads here. can be used to filter out overflowing bangs with smaller values
            #try 10 or so for example.
            if num_threads < 2000:
                #bang is in a new thread so that calculating activation continues
                t1 = threading.Thread(target = self.bang)
                t1.start()
            
        return self.activation
    
    def cleanup(self):
        midiout.cleanup() #closes port for all NNotes!!!
        return
    
    def run(self):
        while self.running:
            self.getActivation()
        return

