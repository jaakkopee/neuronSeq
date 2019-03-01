import neuronSeq
import time

#construct objects and assign midi notes to them.
#the note is played when the neuron fires
#(or bangs, as I like to call it)
kick = neuronSeq.NNote(note=52, duration = 0.03, channel = 1, velocity=127)
snare = neuronSeq.NNote(note=53, duration = 0.03, channel = 1)
snare2 = neuronSeq.NNote(note = 55, duration = 0.03, velocity = 127, channel = 1)
hihat = neuronSeq.NNote(note = 42, duration = 0.03, velocity = 64, channel = 1)

#set neural network parameters
#    being: starting activation, activation increase per iteration
#                            and threshold
#The smaller the activation increase (addToCounter) -value,
#the slower the oscillation.
kick.setNNParams(0.1, 0.0001 , 1.0)
snare.setNNParams(0.0, 0.0001 , 1.0)
snare2.setNNParams(0.5, 0.0002 , 1.8)
hihat.setNNParams(0.0, 0.0003, 1.9)

#two-way connections. +/- excites/inhibits
#+ results to simultaneous and - to alternating
conn1 = neuronSeq.Connection(kick, snare, 0.0000001, 0.0000001)
conn2 = neuronSeq.Connection(kick, snare2, 0.00000062, 0.000000199)
conn3 = neuronSeq.Connection(snare2, snare, 0.00000008, -0.00000023)

#one-way connections: set either weight to 0.0, other to >0.0
conn3_1 = neuronSeq.Connection(snare, snare2, 0.0000000001, 0.0)

#just playing with parameters
conn4 = neuronSeq.Connection(hihat, kick, -0.002, -0.001)
conn5 = neuronSeq.Connection(hihat, snare, 0.0002, -0.000001)

#Bassline on a new channel
bass01 = neuronSeq.NNote(note = 16, duration = 0.3, velocity = 100, channel = 2)
bass02 = neuronSeq.NNote(note = 18, duration = 0.3, velocity = 100, channel = 2)

bass01.setNNParams(0.0, 0.00001, 1.0)
bass02.setNNParams(0.5, 0.00001, 1.0)

connBass01 = neuronSeq.Connection(bass01, bass02, -0.000001, -0.000001)
connBass02 = neuronSeq.Connection(bass02, kick, 0.00001, 0.00001)
connBass03 = neuronSeq.Connection(bass01, kick, 0.000002, 0.000002)

noise01 = neuronSeq.NNote(note = 68, duration = 0.33, velocity = 100, channel = 3)
noise02 = neuronSeq.NNote(note = 26, duration = 0.33, velocity = 120, channel = 3)

connNoise01 = neuronSeq.Connection(noise01, noise02, 0.000001, -0.00002)
connNoise02 = neuronSeq.Connection(noise01, bass01, -0.00001, -0.000012)

conn1.start()
conn2.start()
conn3.start()
conn4.start()
conn5.start()
connBass01.start()
connBass02.start()
connBass03.start()
connNoise01.start()
connNoise02.start()

time.sleep(60.0)#playing time in seconds

conn1.stopSeq()
conn2.stopSeq()
conn3.stopSeq()
conn4.stopSeq()
conn5.stopSeq()
connBass01.stopSeq()
connBass02.stopSeq()
connBass03.stopSeq()
connNoise01.stopSeq()
connNoise02.stopSeq()

conn1.join()
conn2.join()
conn3.join()
conn4.join()
conn5.join()
connBass01.join()
connBass02.join()
connBass03.join()
connNoise01.join()
connNoise02.join()

time.sleep(2)

conn1.cleanup() #closes midiport, global

