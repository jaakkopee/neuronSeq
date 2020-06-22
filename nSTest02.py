import neuronSeq
import time
import rtmidi

#an alias for the sleep-function of module time
playForSeconds = time.sleep

#The fundamental instruments (neurons eg. NNote-objects).
kick = neuronSeq.NNote(id = "Kick", note = 36, velocity = 127, duration = 0.3, channel = 1, activation = 0.99, addToCounter = 0.0000000000003, threshold = 10000.0)
snare = neuronSeq.NNote(id = "Snare", note = 38, velocity = 70, duration = 0.3, channel = 1, activation = 0.6, addToCounter = 0.00000000000000763, threshold = 10000.0)
hihat = neuronSeq.NNote(id = "Hihat", note = 42, velocity = 83, duration = 0.3, channel = 1, activation = 0.1, addToCounter = 0.000078, threshold = 10000.0)

#Kick and snare evade each other, the tend not to play at the same time because of the negative weights in connections
drumConnection00 = neuronSeq.Connection(kick, snare, -0.111, -0.111)

#Hihat does not react to kick at all (weight 0.0). Kick dodges the hihat.
drumConnection01 = neuronSeq.Connection(kick, hihat, 0.0, -0.0000911)

#Snare and hihat do not like to play at the same time.
drumConnection02 = neuronSeq.Connection(snare, hihat, -0.1, -0.00000111)

#Bassline instruments (neurons).
bass01 = neuronSeq.NNote(id = "Bass, note 1", note = 28, duration = 0.9933, velocity = 100, channel = 2, activation = 0.0, addToCounter = 0.00113, threshold = 1000.0)
bass02 = neuronSeq.NNote(id = "Bass, note 2", note = 32, duration = 1.689, velocity = 100, channel = 2, activation = 0.5, addToCounter = 0.00113, threshold = 10000.0)

#The two NNotes of the bassline do not tend to play at the same time.
bassConnection00 = neuronSeq.Connection(bass01, bass02, -0.000222, -0.00000222)
#Both bass NNotes like to play simultaneously with the kickdrum.
bassConnection01 = neuronSeq.Connection(bass02, kick, 0.00000222, 0.000003222)
bassConnection02 = neuronSeq.Connection(bass01, kick, 0.00000222, 0.000003222)

#Creating a neuron to keep the tempo for all NNotes. Notice that velocity = 1, so the note sounds just a bit.
#A MIDI message with velocity = 0 is equal to a note off -event, which would actually be ok here codewise, but it feels logical to have an "active" NNote.
#                                                                                                  init activation   activation increase               activation threshold
headOne = neuronSeq.NNote(id = "Metronome", note = 42, velocity = 1, duration = 0.01, channel = 3, activation = 0.0, addToCounter = 0.000000030303, threshold = 10000.0)

#have to create a dummy NNote, to get the metronome working, because Connection objects work only with pairs of neurons.
dummyPair = neuronSeq.NNote(id = "Dummy neuron", note= 42, velocity = 1, duration = 0.001, channel = 3, activation = 0.0, addToCounter = 0.0, threshold = 10000.0)

#to enable oscillation of object headOne, a Connection object is created
headConnection = neuronSeq.Connection(headOne, dummyPair, 0.0, 0.0)

#All the sounding NNotes are connected heavily to object headOne.
#The connection is from headOne to the instruments, the other direction is set to 0.0. headOne is master and instruments are slaves here.
headConnKick = neuronSeq.Connection(headOne, kick, 0.000121, 0.0)
headConnSnare = neuronSeq.Connection(headOne, snare, 0.000121, 0.0)
headConnHihat = neuronSeq.Connection(headOne, hihat, 0.000121, 0.0)
headConnBass01 = neuronSeq.Connection(headOne, bass01, 0.000121, 0.0)
headConnBass02 = neuronSeq.Connection(headOne, bass02, 0.000121, 0.0)


#some strings

strings1 = neuronSeq.NNote(id = "Strings, note 1", note = 69, velocity = 100, duration = 2.0, channel = 4, activation = 0.0, addToCounter = 0.0000008, threshold = 10000.0)
strings2 = neuronSeq.NNote(id = "Strings, note 2", note = 88, velocity = 100, duration = 1.5, channel = 4, activation = 0.0, addToCounter = 0.0000008, threshold = 10000.0)
strings3 = neuronSeq.NNote(id = "Strings, note 3", note = 56, velocity = 100, duration = 1.0, channel = 4, activation = 0.0, addToCounter = 0.0000008, threshold = 10000.0)

stringConnection1 = neuronSeq.Connection(strings1, strings2, -0.00008, -0.00008)
stringConnection2 = neuronSeq.Connection(strings2, strings3, -0.00008, -0.00008)
stringConnection3 = neuronSeq.Connection(strings1, strings3, -0.00008, -0.00008)
stringConnection4 = neuronSeq.Connection(strings3, strings1, -0.00008, -0.00008)

headConnStrings1 = neuronSeq.Connection(headOne, strings1, 0.00006, 0.00006)
headConnStrings2 = neuronSeq.Connection(headOne, strings2, 0.000009, 0.000009)
headConnStrings3 = neuronSeq.Connection(headOne, strings3, 0.000156, 0.000156)

#And now, at last we get to hear some sounds!
#Gentlemen, start your engines!
#The Connection objects request the NNotes for activation values via NNote's getActivation-function
#and this way the make the whole thing run as the NNotes calculate the activation in the function.
headConnection.start()

headConnKick.start()
headConnSnare.start()
headConnHihat.start()
headConnBass01.start()
headConnBass02.start()
headConnStrings1.start()
headConnStrings2.start()
headConnStrings3.start()

drumConnection00.start()
drumConnection01.start()
drumConnection02.start()

bassConnection00.start()
bassConnection01.start()
bassConnection02.start()

stringConnection1.start()
stringConnection2.start()
stringConnection3.start()
stringConnection4.start()




#The form of the piece of music is here, in three parts:
#play for one minute
playForSeconds(60.0)

#print("Changing parameters...\n")
#Changing some parameter values for variation:

#Neural Network Parameters:
#Object name
#and function call.
#    |         Initial
#    |         activation
#    |         value.
#    |            |    Activation     Activation
#    v            |    increase       threshold
kick.setNNParams(2.99, 0.000000000003, 10000.0)
snare.setNNParams(0.6889, 0.000000000000763, 10000.0)
hihat.setNNParams(0.121, 0.00000078, 10000.0)

#Bass note kill:
bass01.midiout.send_message(bass01.note_off)
#  neuronSeq utilizes threads in it's operation, so some messages can be left undelivered
#  It is sensible to kill the bass here, for in cases 7 out of 10 in test runs,
#  a bass note was left playing throughout the song and after it had ended. Killing it to be sure is a simple but effective hack.


#change bass note         values 0-127    dur in seconds
bass01.setNote(note = 40, velocity = 120, duration = 0.1, channel = 2)

#kill strings3
strings3.midiout.send_message(strings3.note_off)

#change string note
strings3.setNote(note = 39, velocity = 100, duration = 1.0, channel = 4)

#and play for another minute
playForSeconds(60.0)
#change parameters again
kick.setNNParams(0.006, 0.0000000000019, 10000.0)
snare.setNNParams(0.126689, 0.0000000000763, 10000.0)
hihat.setNNParams(0.008001, 0.00000700008, 10000.0)

#Kill Bass:
bass01.midiout.send_message(bass01.note_off)

#again, the bassline changes a bit
bass01.setNote(note = 32, velocity = 123, duration = 0.1, channel = 2)

#Kill Strings
strings1.midiout.send_message(strings1.note_off)

#... and so do the strings
strings1.setNote(note = 78, velocity = 100, duration = 2.0, channel = 4)

#set new weights for kickdrum. First connection from neuron 0 to 1, then connection 1 to 0
headConnKick.weight = [-0.8, 0.001023]
drumConnection00.weight = [-0.002, 0.00009]

#and play for 30 seconds
playForSeconds(30.0)


#stop sequencing
headConnection.stopSeq()

headConnKick.stopSeq()
headConnSnare.stopSeq()
headConnHihat.stopSeq()
headConnBass01.stopSeq()
headConnBass02.stopSeq()
headConnStrings1.stopSeq()
headConnStrings2.stopSeq()
headConnStrings3.stopSeq()

drumConnection00.stopSeq()
drumConnection01.stopSeq()
drumConnection02.stopSeq()

bassConnection00.stopSeq()
bassConnection01.stopSeq()
bassConnection02.stopSeq()

stringConnection1.stopSeq()
stringConnection2.stopSeq()
stringConnection3.stopSeq()
stringConnection4.stopSeq()


#wait for processes to end
headConnection.join()

headConnKick.join()
headConnSnare.join()
headConnHihat.join()
headConnBass01.join()
headConnBass02.join()
headConnStrings1.join()
headConnStrings2.join()
headConnStrings3.join()

drumConnection00.join()
drumConnection01.join()
drumConnection02.join()

bassConnection00.join()
bassConnection01.join()
bassConnection02.join()

stringConnection1.join()
stringConnection2.join()
stringConnection3.join()
stringConnection4.join()


#just in case, to not get a error message from python interpreter
time.sleep(2.5)

#close MIDI port. One call to any one of the Connection-objects is adequate.
drumConnection00.cleanup()
