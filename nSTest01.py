import neuronSeq
import time

kick = neuronSeq.NNote(note = 36, velocity = 127, duration = 0.3, channel = 0)
snare = neuronSeq.NNote(note = 38, velocity = 100, duration = 0.3, channel = 0)
hihat = neuronSeq.NNote(note = 42, velocity = 83, duration = 0.3, channel = 0)

kick.setNNParams(0.99, 0.000000003, 1.0)
snare.setNNParams(0.6, 0.00003, 1.0)
hihat.setNNParams(0.1, 0.000068, 1.0)

drumConnection00 = neuronSeq.Connection(kick, snare, -0.0000111, -0.00000111)
drumConnection01 = neuronSeq.Connection(kick, hihat, -0.00000111, -0.000000000111)
drumConnection02 = neuronSeq.Connection(snare, hihat,-0.0000000111, -0.0000000111)

bass01 = neuronSeq.NNote(note = 16, duration = 0.6933, velocity = 100, channel = 1)
bass02 = neuronSeq.NNote(note = 12, duration = 0.689, velocity = 100, channel = 1)

bass01.setNNParams(0.0, 0.0000113, 1.0)
bass02.setNNParams(0.5, 0.0000113, 1.0)

bassConnection00 = neuronSeq.Connection(bass01, bass02, -0.00000222, 0.00000222)
bassConnection01 = neuronSeq.Connection(bass02, kick, 0.0000000222, 0.0000000222)
bassConnection02 = neuronSeq.Connection(bass01, kick, 0.0000000222, 0.0000000222)

headOne = neuronSeq.NNote(note = 42, velocity = 0, duration = 0.001, channel = 2)
dummyPair = neuronSeq.NNote(note= 42, velocity = 0,duration = 0.001, channel = 2)

headOne.setNNParams(0.0, 0.0000000030303, 1.0)
dummyPair.setNNParams(0.0, 0.0, 1.0)

headConnection = neuronSeq.Connection(headOne, dummyPair, 0.0, 0.0)

headConnKick = neuronSeq.Connection(headOne, kick, 0.0,  0.000121)
headConnSnare = neuronSeq.Connection(headOne, snare, 0.0, 0.000121)
headConnHihat = neuronSeq.Connection(headOne, hihat, 0.0, 0.000121)
headConnBass01 = neuronSeq.Connection(headOne, bass01, 0.0, 0.000121)
HeadConnBass02 = neuronSeq.Connection(headOne, bass02, 0.0, 0.000121)

headConnection.start()

headConnKick.start()
headConnSnare.start()
headConnHihat.start()
headConnBass01.start()
HeadConnBass02.start()

drumConnection00.start()
drumConnection01.start()
drumConnection02.start()

bassConnection00.start()
bassConnection01.start()
bassConnection02.start()

time.sleep(120.0)

headConnection.stopSeq()

headConnKick.stopSeq()
headConnSnare.stopSeq()
headConnHihat.stopSeq()
headConnBass01.stopSeq()
HeadConnBass02.stopSeq()

drumConnection00.stopSeq()
drumConnection01.stopSeq()
drumConnection02.stopSeq()

bassConnection00.stopSeq()
bassConnection01.stopSeq()
bassConnection02.stopSeq()

headConnection.join()

headConnKick.join()
headConnSnare.join()
headConnHihat.join()
headConnBass01.join()
HeadConnBass02.join()

drumConnection00.join()
drumConnection01.join()
drumConnection02.join()

bassConnection00.join()
bassConnection01.join()
bassConnection02.join()

time.sleep(1)

drumConnection00.cleanup()
