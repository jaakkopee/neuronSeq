import neuronSeq
import time
import rtmidi

#an alias for the sleep-function of module time                                                                                                                                   
playForSeconds = time.sleep

#The fundamental instruments (neurons eg. NNote-objects).                                                   
kick = neuronSeq.NNote(id = "Kick", note = 36, velocity = 127, duration = 0.3, channel = 1, activation = 0.09, addToCounter = 0.09, threshold = 1920.0)
snare01 = neuronSeq.NNote(id = "snare01", note = 42, velocity = 127, duration = 0.0000001, channel = 1, activation = 0.9, addToCounter = 0.000009, threshold = 1920.0)

drumConnection00 = neuronSeq.Connection(kick, snare01, -0.0000000061009, -0.00614120000009)

drumConnection00.start()

playForSeconds(10)

drumConnection00.stopSeq()
drumConnection00.join()

time.sleep(2)

drumConnection00.cleanup()

