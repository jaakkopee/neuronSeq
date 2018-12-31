import neuronSeq
import time

nnote1 = neuronSeq.NNote(36, "nnote1")
nnote2 = neuronSeq.NNote(62, "nnote2")
nnote2.setNote(62, 95, 0.15)
nnote2.setNNParams(0.0, 0.8, 120.78)

nnote1_1 = neuronSeq.NNote(53, "nnote1_1")
nnote1_1.setNote(53, 100, 0.1)
nnote1_1.setNNParams(0.0, 0.002, 200.78)

nnote1.addConnection(nnote1_1, 1.4)
nnote2.addConnection(nnote1_1, -0.008)

nnote1_2 = neuronSeq.NNote(43, "nnote1_2")
nnote1_2.setNote(49, 80, 0.15)
nnote1.addConnection(nnote1_2, 1.0)

nnote1.start()
nnote2.start()
nnote1_1.start()

time.sleep(20)

nnote1.runSwitch(False)
nnote2.runSwitch(False)
nnote1_1.runSwitch(False)
nnote1_2.runSwitch(False)



