import neuronSeq
import time

kick = neuronSeq.NNote(note = 36, duration = 0.03, channel = 1, velocity= 127)
snare = neuronSeq.NNote(note = 37, duration = 0.03, channel = 1, velocity = 100)
hihat = neuronSeq.NNote(note = 52, duration= 0.06, channel = 1, velocity=127)

kick.setNNParams(0.0, 0.0000026, 1.0)
snare.setNNParams(0.0, 0.0000021, 1.0)
hihat.setNNParams(0.0, 0.0000012, 1.0)

conn01 = neuronSeq.Connection(kick, snare, -0.0000001, -0.0000001)
conn02 = neuronSeq.Connection(kick, hihat, -0.0000003, -0.0000003)

conn01.start()
conn02.start()

time.sleep(20.0)

conn01.stopSeq()
conn02.stopSeq()

conn01.join()
conn02.join()

time.sleep(2)

conn01.cleanup()


