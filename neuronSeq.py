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
    def __init__(self, note=60, velocity=100, duration = 0.2, id = "NNote", channel = 1, activation = 0.0, addToCounter = 0.0001, threshold = 1.0):

        self.id = id
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
        self.infostr += "Activation entry level: "+ str(self.activation)+"\n"
        self.infostr += "Activation counter increase: "+ str(self.addToCounter)+"\n"
        self.infostr += "Activation threshold: " + str(self.threshold)+"\n\n\n"

        print ("Constructed a neuron: " + str(self))


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
        self.infostr += "Activation entry level: "+ str(self.activation)+"\n"
        self.infostr += "Activation counter increase: "+ str(self.addToCounter)+"\n"
        self.infostr += "Activation threshold: " + str(self.threshold)+"\n\n\n"

        print("Note data parameter change: "+ str(self))

        return

    def setNNParams(self, activation = 0.0, addToCounter = 0.0001, threshold=1.0):
        self.activation = activation
        self.addToCounter = addToCounter
        self.threshold = threshold

        self.infostr = self.id +" "+ str(self.note_on)+"\n"+str(self.note_off)
        self.infostr += "\n" + "Duration: "+str(self.note_length)
        self.infostr += "\n\n"+ "Neural Network Parameters:\n"
        self.infostr += "Activation entry level: "+ str(self.activation)+"\n"
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
