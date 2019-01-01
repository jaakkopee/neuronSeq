import neuronSeq
import time

#construct objects and assign midi notes to them.
#the note is played when the neuron fires
#(or bangs, as I like to call it)
nnote1 = neuronSeq.NNote(note=52)
nnote2 = neuronSeq.NNote(note=61)
nnote1_1 = neuronSeq.NNote(note=62)
nnote1_2 = neuronSeq.NNote(note=48)

#set neural network parameters
#    being: starting activation, activation increase per iteration
#                            and threshold
nnote1.setNNParams(0.0, 0.00001, 1.0)
nnote2.setNNParams(0.0, 0.00001, 1.0)
nnote1_1.setNNParams(0.5, 0.00001, 1.0)
nnote1_2.setNNParams(0.0, 0.00001, 1.0)

#subtle modulation is quite enough to get nice patterns
#positive values exhibit and neagtive values inhibit
#exhibition leads to simultaneous bangs and inhibition
#creates alternating patterns, as the connected neurons
#do not want to bang at the same time

#   parameters are: source NNote and connection strength
# vv-- target NNote is the caller
nnote1.addConnection(nnote2, 0.000001)
nnote1_1.addConnection(nnote2, -0.000001)
nnote1_2.addConnection(nnote1_1, 0.000001)
nnote1.addConnection(nnote1_2, -0.000001)

#starts the activation-threshold-bang-loops
nnote1.start()
nnote2.start()
nnote1_1.start()
nnote1_2.start()

time.sleep(120.0)#play for 2 minutes

#without stopSeq(), the loop goes on forever
nnote1.stopSeq()
nnote2.stopSeq()
nnote1_1.stopSeq()
nnote1_2.stopSeq()

#cleanup() closes the midiport for all NNotes
#so only one call is enough. It doesn't matter which neuron owns
#the called cleanup()
nnote1.cleanup()

