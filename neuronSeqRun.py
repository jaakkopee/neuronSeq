import neuronSeq
import time

nnote1 = neuronSeq.NNote(note=52)
nnote2 = neuronSeq.NNote(note=61)
nnote1_1 = neuronSeq.NNote(note=62)
nnote1_2 = neuronSeq.NNote(note=48)

nnote1.setNNParams(0.0, 0.00001, 1.0)
nnote2.setNNParams(0.0, 0.00001, 1.0)
nnote1_1.setNNParams(0.5, 0.00001, 1.0)
nnote1_2.setNNParams(0.0, 0.00001, 1.0)

#subtle modulation is quite enough to get nice patterns
#positive values exhibit and neagtive values inhibit
#exhibition leads to simultaneous bangs and inhibition
#creates fluctuating patterns, as the connected neurons
#do not want to bang at the same time
nnote1.addConnection(nnote2, 0.000001)
nnote1_1.addConnection(nnote2, -0.000001)
nnote1_2.addConnection(nnote1_1, 0.000001)
nnote1.addConnection(nnote1_2, -0.000001)

nnote1.start()
nnote2.start()
nnote1_1.start()
nnote1_2.start()

time.sleep(120.0)

nnote1.stopSeq()
nnote2.stopSeq()
nnote1_1.stopSeq()
nnote1_2.stopSeq()



