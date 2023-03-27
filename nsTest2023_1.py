import neuronSeq as ns
import time

playForSeconds = time.sleep
#NNotes
bass1 = ns.NNote(id = "Bass 1", note = 36, velocity = 110, duration = 0.3, channel = 1, activation = 0.09, addToCounter = 0.0000009, threshold = 1920.0)
bass2 = ns.NNote(id = "Bass 2", note = 42, velocity = 110, duration = 0.2, channel = 1, activation = 0.01, addToCounter = 0.00000008, threshold = 2000.0)
drum1 = ns.NNote(id = "Drum 1", note = 47, velocity = 127, duration = 0.8, channel = 2, activation = 0.001, addToCounter = 0.000000038, threshold = 4800.0)
subdrum1 = ns.NNote(id = "Sub Drum 1", note = 42, velocity = 127, duration = 0.48, channel = 2, activation = 1000.0, addToCounter = 0.00000038, threshold = 4200.0)
subdrum2 = ns.NNote(id = "Sub Drum 2", note = 36, velocity = 127, duration = 0.020, channel = 2, activation = 600.0, addToCounter = 0.00000956, threshold = 4180.0)
slowerer1 = ns.NNote(id = "Deep Modulation", note = 42, velocity = 100, duration = 0.5, channel = 3, activation = 0.0, addToCounter = 0.000000093, threshold = 555.0)

#Connections
connBs1Bs2 = ns.Connection(bass1, bass2, 0.00000105060, -0.0000000606060)
connDr1Bs1 = ns.Connection(drum1, bass1, 0.000000500001, 0.0000008000000001)
connDr1Bs2 = ns.Connection(drum1, bass2, 0.00000020001, -0.00000000008001)
connDr1SubDr1 = ns.Connection(drum1, subdrum1, 0.000008, -0.0000000001)
connDr1SubDr2 = ns.Connection(drum1, subdrum2, 0.000008, -0.000000000001)
connSlowerer1Bs1 = ns.Connection(slowerer1, bass1, -0.00001, 0.000001)
connSlowerer1Bs2 = ns.Connection(slowerer1, bass2, -0.000001, 0.00001)
connSlowerer1Dr1 = ns.Connection(slowerer1, drum1, -0.00001, 0.000001)
connSlowerer1SubDrum1 = ns.Connection(slowerer1, subdrum1, -0.000001, 0.000001)
connSlowerer1SubDrum2 = ns.Connection(slowerer1, subdrum2, -0.000001, 0.000001)


#execute
connBs1Bs2.start()
connDr1Bs1.start()
connDr1Bs2.start()
connDr1SubDr1.start()
connDr1SubDr2.start()
connSlowerer1Bs1.start()
connSlowerer1Bs2.start()
connSlowerer1Dr1.start()
connSlowerer1SubDrum1.start()
connSlowerer1SubDrum2.start()


playForSeconds(360.0)


connBs1Bs2.stopSeq()
connDr1Bs1.stopSeq()
connDr1Bs2.stopSeq()
connDr1SubDr1.stopSeq()
connDr1SubDr2.stopSeq()
connSlowerer1Bs1.stopSeq()
connSlowerer1Bs2.stopSeq()
connSlowerer1Dr1.stopSeq()
connSlowerer1SubDrum1.stopSeq()
connSlowerer1SubDrum2.stopSeq()

time.sleep(2)

connBs1Bs2.cleanup()
connDr1Bs1.cleanup()
connDr1Bs2.cleanup()
connDr1SubDr1.cleanup()
connDr1SubDr2.cleanup()
connSlowerer1Bs1.cleanup()
connSlowerer1Bs2.cleanup()
connSlowerer1Dr1.cleanup()
connSlowerer1SubDrum1.cleanup()
connSlowerer1SubDrum2.cleanup()

