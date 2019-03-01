import rtmidi

class NNMidiOut:
    def __init__(self):
        self.out = rtmidi.RtMidiOut()
        self.out.openPort(1)
        return
    
    def send_message(self, msg):
        self.out.sendMessage(msg)
        return
    
    def cleanup(self):
        del self.out
        return
