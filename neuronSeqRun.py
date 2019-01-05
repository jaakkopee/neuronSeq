import neuronSeq
import time

#construct objects and assign midi notes to them.
#the note is played when the neuron fires
#(or bangs, as I like to call it)
kick = neuronSeq.NNote(note=52, duration = 0.05)
snare = neuronSeq.NNote(note=53, duration = 0.05)
snare2 = neuronSeq.NNote(note = 55, duration = 0.05)
hihat = neuronSeq.NNote(note = 42, duration = 0.05, velocity = 64)

#set neural network parameters
#    being: starting activation, activation increase per iteration
#                            and threshold
#The smaller the activation increase (addToCounter) -value,
#the slower the oscillation.
kick.setNNParams(0.0, 0.00000199995, 1.0)
snare.setNNParams(0.0, 0.0000008999, 1.0)
snare2.setNNParams(0.5, 0.0000020295, 1.0)
hihat.setNNParams(0.0, 0.0000619, 1.0)

conn1 = neuronSeq.Connection(kick, snare, -0.00000018, -0.000000186)
conn2 = neuronSeq.Connection(kick, snare2, -0.00000002, -0.000000199)
conn3 = neuronSeq.Connection(snare2, snare, 0.00000018, -0.00000023)
#one-way connection
conn4 = neuronSeq.Connection(hihat , kick, 0.0008252, 0.0) 
#free oscillation (adds to total oscillation)
conn5 = neuronSeq.Connection(hihat, snare, 0.0, 0.0)

conn1.start()
conn2.start()
conn3.start()
conn4.start()
conn5.start()

time.sleep(30.0)#playing time in seconds

conn1.stopSeq()
conn2.stopSeq()
conn3.stopSeq()
conn4.stopSeq()
conn5.stopSeq()

conn1.join()
conn2.join()
conn3.join()
conn4.join()
conn5.join()

time.sleep(2)

conn1.cleanup() #closes midiport, global
