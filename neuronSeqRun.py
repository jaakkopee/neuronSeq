import neuronSeq
import time

nnote1 = neuronSeq.NNote(note=52)
nnote2 = neuronSeq.NNote(note=61)
nnote1_1 = neuronSeq.NNote(note=62)
nnote1_2 = neuronSeq.NNote(note=48)

nnote1.setNNParams(0.0, 0.08, 10000.00)
nnote2.setNNParams(0.0, 0.01, 10000.00)
nnote1_1.setNNParams(5000.00, 0.0008, 10000.00)
nnote1_2.setNNParams(0.0, 0.006, 10000.00)

nnote1.addConnection(nnote2, -0.00000001)
nnote1_1.addConnection(nnote2, 1.0)
nnote1_2.addConnection(nnote1_1, 0.00000046)

nnote1.setTransferFunction('heaviside')
nnote2.setTransferFunction('heaviside')
nnote1_1.setTransferFunction('heaviside')
nnote1_2.setTransferFunction('heaviside')


nnote1.start()
nnote2.start()
nnote1_1.start()
nnote1_2.start()

time.sleep(120.0)

nnote1.stopSeq()
nnote2.stopSeq()
nnote1_1.stopSeq()
nnote1_2.stopSeq()



