import neuronSeq
import time
import rtmidi

#an alias for the sleep-function of module time                                                                                                                                   
playForSeconds = time.sleep

#The fundamental instruments (neurons eg. NNote-objects).                                                   
kick = neuronSeq.NNote(id = "Kick", note = 36, velocity = 127, duration = 0.3, channel = 1, activation = 0.09, addToCounter = 0.09, threshold = 1920.0)
snare01 = neuronSeq.NNote(id = "snare01", note = 42, velocity = 127, duration = 0.0000001, channel = 1, activation = 0.9, addToCounter = 0.0009, threshold = 19210.0)

hidastaja = neuronSeq.NNote(id = "hidastaja", note = 52, velocity = 127, duration = 0.8, channel = 2, activation = 0.2, addToCounter = 0.00000000006666, threshold = 93000.0)


somedrum = neuronSeq.NNote(id = "somedrum", note = 39, velocity = 127, duration = 0.03, channel = 1, activation = 0.0009, addToCounter = 0.00000009, threshold = 14825.0)


drumConnection00 = neuronSeq.Connection(kick, snare01, -0.0000000061009, -0.000614120000009)

drumConnection01 = neuronSeq.Connection(somedrum, snare01, 1.0, -0.00614120000009)

drumConnection02 = neuronSeq.Connection(somedrum, kick, -0.000061009, -0.000614120000009)

hidastusConn00 = neuronSeq.Connection(hidastaja, kick, -0.05, -0.06)
hidastusConn01 = neuronSeq.Connection(hidastaja, snare01, -0.008, -0.012)

drumConnection00.start()
drumConnection01.start()
drumConnection02.start()

hidastusConn00.start()
hidastusConn01.start()



playForSeconds(10)



drumConnection00.stopSeq()
drumConnection01.stopSeq()
drumConnection02.stopSeq()

hidastusConn00.stopSeq()
hidastusConn01.stopSeq()

drumConnection00.join()
drumConnection01.join()
drumConnection02.join()

hidastusConn00.join()
hidastusConn01.join()

time.sleep(2)



drumConnection00.cleanup()

