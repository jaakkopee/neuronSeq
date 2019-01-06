import neuronSeq
import time

kick = neuronSeq.NNote(note = 36, velocity = 127, duration = 0.3, channel = 0)
snare = neuronSeq.NNote(note = 38, velocity = 100, duration = 0.3, channel = 0)
hihat = neuronSeq.NNote(note = 42, velocity = 83, duration = 0.3, channel = 0)

kick.setNNParams(0.0, 0.000013624, 1.0)
snare.setNNParams(0.5, 0.00000361213, 1.0)
hihat.setNNParams(0.1, 0.0000611331, 1.0)

drumConnection00 = neuronSeq.Connection(kick, snare, -0.0000012631, -0.0000011362)
drumConnection01 = neuronSeq.Connection(kick, hihat, -0.0000013,    -0.000001326)
drumConnection02 = neuronSeq.Connection(snare, hihat, -0.0000026,   -0.000002662)

bass01 = neuronSeq.NNote(note = 16, duration = 0.3, velocity = 100, channel = 1)
bass02 = neuronSeq.NNote(note = 18, duration = 0.3, velocity = 100, channel = 1)

bass01.setNNParams(0.0, 0.0000113, 1.0)
bass02.setNNParams(0.5, 0.0000113, 1.0)

bassConnection00 = neuronSeq.Connection(bass01, bass02, -0.0000001, -0.0000001)
bassConnection01 = neuronSeq.Connection(bass02, kick, 0.0000001, 0.0000001)
bassConnection02 = neuronSeq.Connection(bass01, kick, 0.00000002, 0.00000002)





drumConnection00.start()
drumConnection01.start()
drumConnection02.start()

bassConnection00.start()
bassConnection01.start()
bassConnection02.start()

time.sleep(60.0)

drumConnection00.stopSeq()
drumConnection01.stopSeq()
drumConnection02.stopSeq()

bassConnection00.stopSeq()
bassConnection01.stopSeq()
bassConnection02.stopSeq()

drumConnection00.join()
drumConnection01.join()
drumConnection02.join()

bassConnection00.join()
bassConnection01.join()
bassConnection02.join()

time.sleep(1)

drumConnection00.cleanup()
