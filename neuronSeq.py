import time
import mido
import threading
import nnmidiout #connection to rtmidi
import math

midiout = nnmidiout.NNMidiOut()
print "neuronSeq by Jaakko Prattala 2019. Use freely."

class NNote (threading.Thread):
    def __init__(self, note=60, velocity=100, duration = 0.2, notename="midinote", transferFunction="linear"):
        threading.Thread.__init__(self)

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
        self.connections = [] #connections from and weights

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
        #implementation buggy and incomplete, use "linear"
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
        #first, activation is set 0.0 (in getActivation())
        #second, a MIDI note is played (here)
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
    
    def addConnection(self, nnote, inConnWeight, outConnWeight = 0.0):
        self.connections += [[nnote, inConnWeight, outConnWeight]]
        #print self.name +": "+ str(self.connections)
        return

    def setConnectionWeight(self, connectionIndex, newInConnWeight, newOutConnWeight = 0.0):
        self.connections[connectionIndex][1] = newInConnWeight
        self.connections[connectionIndex][2] = newOutConnWeight
        return
    
    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold
        return

    def setActivation(self, newActivation):
        self.activation = newActivation
        return
    
    def getActivation(self):
        #print self.name + " getActivation()"

        #first the activation is increased internally
        self.activation += self.addToCounter

        #then from connected NNotes comes their weighed activation
        if self.connections:
            for i in self.connections:
                self.activation += i[0].getActivation() * i[1]

                #set outward connection's activation (A bubblegum fix... don't know if this is valid)
                if (i[2]):
                    i[0].setActivation(i[0].addToCounter + i[2] * i[0].activation)
                    outputValueA = i[0].transferFunction()
                    if (outputValueA >= i[0].threshold):
                        i[0].setActivation(0.0)
                        num_threads = threading.activeCount()
                        if num_threads < 2000:
                            t0 = threading.Thread(target = i[0].bang)
                            t0.start()            

                if (i[1]):
                    #activation is fed to a transfer function
                    outputValue = self.transferFunction() #transfer functions do not work atm. use "linear".
            
                    if outputValue >= self.threshold: #check if neuron is supposed to fire
                        #activation is set to zero here instead of in  bang()
                        #so that a new check for threshold doesn't happen before this.
                        self.activation = 0.0 #FIRE! part 1
            
                        num_threads = threading.activeCount()
            
                        #set max threads here. can be used to filter out overflowing bangs with smaller values
                        #like 10 or so for example. also helps
                        #if the operating systems maximum threads per process is reached
                        if num_threads < 2000:
                            #bang is in a new thread so that calculating activation continues
                            t1 = threading.Thread(target = self.bang)
                            t1.start() #FIRE! part 2
                            

        if not self.connections:           
            outputValue = self.transferFunction()
            
            if outputValue >= self.threshold:               
                self.activation = 0.0            
                num_threads = threading.activeCount()
                if num_threads < 2000:        
                    t1 = threading.Thread(target = self.bang)
                    t1.start() 

        return self.activation
    
    def cleanup(self):
        midiout.cleanup() #closes port for all NNotes!!!
        return

    #overrides threading.Thread 's method run()
    def run(self):
        while self.running:
            self.getActivation()
        return

