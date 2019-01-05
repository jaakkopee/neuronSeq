import neuronSeq
import time

#construct objects and assign midi notes to them.
#the note is played when the neuron fires
#(or bangs, as I like to call it)
kick = neuronSeq.NNote(note=52, duration = 0.05)
snare = neuronSeq.NNote(note=53, duration = 0.05)
snare2 = neuronSeq.NNote(note = 55, duration = 0.05, velocity = 127)
hihat = neuronSeq.NNote(note = 42, duration = 0.05, velocity = 64)

#set neural network parameters
#    being: starting activation, activation increase per iteration
#                            and threshold
#The smaller the activation increase (addToCounter) -value,
#the slower the oscillation.
kick.setNNParams(0.0, 0.00002199995, 1.0)
snare.setNNParams(0.0, 0.0000018999, 1.0)
snare2.setNNParams(0.5, 0.0000020295, 1.0)
hihat.setNNParams(0.0, 0.0000619, 1.0)

#two-way connections. +/- excites/inhibits
#+ results to simultaneous and - to alternating
conn1 = neuronSeq.Connection(kick, snare, -0.00000018, -0.000000186)
conn2 = neuronSeq.Connection(kick, snare2, -0.00000002, -0.000000199)
conn3 = neuronSeq.Connection(snare2, snare, 0.00000018, -0.00000023)

#one-way connections: set either weight to 0.0, other to >0.0
conn3_1 = neuronSeq.Connection(snare, snare2, 0.0000000001, 0.0)

#just playing with parameters
conn4 = neuronSeq.Connection(hihat, kick, 0.0018252, -0.0001) 

#free oscillation (adds to total oscillation)
conn5 = neuronSeq.Connection(hihat, snare, 0.0, 0.0)

#Bassline on a new channel (channels here are 0,...,15, so channel 1 here
# is channel 2 in most DAWs)
bass01 = neuronSeq.NNote(note = 16, duration = 0.3, velocity = 100, channel = 1)
bass02 = neuronSeq.NNote(note = 18, duration = 0.3, velocity = 100, channel = 1)

bass01.setNNParams(0.0, 0.0000082, 1.0)
bass02.setNNParams(0.5, 0.00001, 1.0)

connBass01 = neuronSeq.Connection(bass01, bass02, -0.0000093, -0.0000056)
connBass02 = neuronSeq.Connection(bass02, kick, 0.000018, 0.0000162)
connBass03 = neuronSeq.Connection(bass01, kick, 0.00000281, 0.00002969)

conn1.start()
conn2.start()
conn3.start()
conn4.start()
conn5.start()
connBass01.start()
connBass02.start()
connBass03.start()

time.sleep(60.0)#playing time in seconds

conn1.stopSeq()
conn2.stopSeq()
conn3.stopSeq()
conn4.stopSeq()
conn5.stopSeq()
connBass01.stopSeq()
connBass02.stopSeq()
connBass03.stopSeq()

conn1.join()
conn2.join()
conn3.join()
conn4.join()
conn5.join()
connBass01.join()
connBass02.join()
connBass03.join()

time.sleep(2)

conn1.cleanup() #closes midiport, global
