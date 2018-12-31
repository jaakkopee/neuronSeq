import time
import mido
import threading
import nnmidiout #connection to rtmidi

midiout = nnmidiout.NNMidiOut()

class NNote (threading.Thread):
    def __init__(self, midinote, name):
        threading.Thread.__init__(self)

        self.name = name #for debugging mainly
        
        #MIDI settings
        #velocity and duration will be set by the NN eventually
        self.note_on = mido.Message('note_on', channel=0, note = midinote, velocity = 100).bytes()
        self.note_off = mido.Message('note_off', note = midinote).bytes()
        self.note_length = 0.5

        #NN settings
        self.activation = 0.0
        self.addToCounter = 0.1
        self.threshold = 66.6
        self.connections = []

        #Operational settings
        self.running = True
        
    def setNote(self, midinote, midivelocity, duration):
        self.note_on = mido.Message('note_on', channel=0, note = midinote, velocity = midivelocity).bytes()
        self.note_length = duration
        self.note_off = mido.Message('note_off', note = midinote).bytes()
        return
    
    def bang(self):
        midiout.send_message(self.note_on)
        time.sleep(self.note_length)
        midiout.send_message(self.note_off)
        self.activation = 0.0
        return
    
    def runSwitch(self, runner):
        self.running = runner
        return
    

    def addConnection(self, nnote, strength):
        self.connections += [[nnote, strength]]
        #print self.name +": "+ str(self.connections)
        return
    
    def setNNParams(self, activation, addToCounter, threshold):
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

        if self.activation >= self.threshold:
            self.bang()
        
        return self.activation
    
    def cleanup(self):
        midiout.cleanup()
        return
    
    def run(self):
        while self.running:
            self.getActivation()
        return

    def testing(self):
        print "YummiYammi"
        
