import rtmidi

class NNMidiOut:
    def __init__(self):
        self.out = rtmidi.MidiOut()
        self.out.open_port(0)
        return
    
    def send_message(self, msg):
        self.out.send_message(msg)
        return
    
    def cleanup(self):
        del self.out
        return
