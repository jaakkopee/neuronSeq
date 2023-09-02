import rtmidi

class NNMidiOut:
    def __init__(self):

        #Name of the MIDI port in use
        self.portName = "virmidi"

        self.midiout = None
        self.midiout = rtmidi.RtMidiOut()
        available_ports = self.midiout.getPortCount()

        if available_ports:
            self.midiout.openPort(0)
        else:
            self.midiout.openVirtualPort(self.portName)
                
        return
    
    def send_message(self, msg):
        self.midiout.sendMessage(msg)
        return
    
    def cleanup(self):
        del self.midiout
        return
