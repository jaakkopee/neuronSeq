import rtmidi

class NNMidiOut:
    def __init__(self):

        #Name of the MIDI port in use
        self.portName = "virtual1"


        self.out = rtmidi.RtMidiOut()
        portCount = self.out.getPortCount()
        print ("number of available MIDI  ports: "+str(portCount))
        print ("using port" + self.portName)
        
        #Using virtual ports by default
        self.out.openVirtualPort(self.portName)
        
        return
    
    def send_message(self, msg):
        self.out.sendMessage(msg)
        return
    
    def cleanup(self):
        del self.out
        return
