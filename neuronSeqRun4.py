import neuronSeq
import time

kick = neuronSeq.NNote(note = 36, duration = 0.03, channel = 1, velocity= 127)
snare = neuronSeq.NNote(note = 42, duration = 0.03, channel = 1, velocity = 127)
hihat = neuronSeq.NNote(note = 52, duration= 0.06, channel = 1, velocity=127)
syn01 = neuronSeq.NNote(note = 32, duration=0.6, channel=2,velocity=127)
tempokick = neuronSeq.NNote(note = 36, duration = 0.03, channel = 3, velocity=127)

kick.setNNParams(0.0, 0.0000092, 1.0)
snare.setNNParams(0.0, 0.000024, 1.0)
hihat.setNNParams(0.0, 0.000008, 1.0)
syn01.setNNParams(0.0, 0.00000016, 1.0)
tempokick.setNNParams(0.0, 0.0000064, 1.0)

conn01 = neuronSeq.Connection(kick, snare, -0.00002, -0.00002)
conn02 = neuronSeq.Connection(kick, hihat, -0.0000008, -0.0000008)
conn03 = neuronSeq.Connection(kick, syn01, 0.000008,   0.00008)
conn04 = neuronSeq.Connection(tempokick, kick, 0.000002, 0.000002)

conn01.start()
conn02.start()
conn03.start()
conn04.start()

time.sleep(120.0)

conn01.stopSeq()
conn02.stopSeq()
conn03.stopSeq()
conn04.stopSeq()

conn01.join()
conn02.join()
conn03.join()
conn04.join()

time.sleep(2)

conn01.cleanup()


