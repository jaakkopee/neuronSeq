import wx
import time
import neuronSeq

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

kick = neuronSeq.NNote(note = 36, duration = 0.03, channel = 1, velocity= 127)
snare = neuronSeq.NNote(note = 42, duration = 0.03, channel = 1, velocity = 127)
hihat = neuronSeq.NNote(note = 52, duration= 0.06, channel = 1, velocity=127)
syn01 = neuronSeq.NNote(note = 32, duration=0.6, channel=2,velocity=127)
tempokick = neuronSeq.NNote(note = 36, duration = 0.03, channel = 3, velocity=127)

kick.setNNParams(0.0, 0.0, 1.0)
snare.setNNParams(0.0, 0.0, 1.0)
hihat.setNNParams(0.0, 0.0, 1.0)
syn01.setNNParams(0.0, 0.0, 1.0)
tempokick.setNNParams(0.0, 0.0, 1.0)

conn01 = neuronSeq.Connection(kick, snare, -0.000001, -0.000001)
conn02 = neuronSeq.Connection(kick, hihat, -0.000001, -0.000001)
conn03 = neuronSeq.Connection(kick, syn01, -0.000001, -0.000001)
conn04 = neuronSeq.Connection(tempokick, kick, -0.000001, -0.000001)



class mainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: mainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.slider_1 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_2 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_3 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_4 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_5 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_6 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_7 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)
        self.slider_8 = wx.Slider(self, wx.ID_ANY, 0, 0, 1024, style=wx.SL_VERTICAL)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll01, self.slider_1)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll02, self.slider_2)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll03, self.slider_3)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll04, self.slider_4)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll05, self.slider_5)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll06, self.slider_6)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll07, self.slider_7)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.scroll08, self.slider_8)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: mainFrame.__set_properties
        self.SetTitle("Controller One")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: mainFrame.__do_layout
        grid_sizer_1 = wx.GridSizer(1, 8, 0, 0)
        grid_sizer_1.Add(self.slider_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_3, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_4, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_5, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_6, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_7, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.slider_8, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

    def scroll01(self, event):  # wxGlade: mainFrame.<event_handler>
        value = event.GetInt()/10000000.0
        print "slider 01: " + str(value)
        print "Changing addToCounter for bass drum"
        kick.addToCounter = value
        
        event.Skip()

    def scroll02(self, event):  # wxGlade: mainFrame.<event_handler>
        value = event.GetInt()/10000000.0
        print "slider 02: " + str(value)
        print "Changing addToCounter for snare drum"
        snare.addToCounter = value
        event.Skip()

    def scroll03(self, event):  # wxGlade: mainFrame.<event_handler>

        value = event.GetInt()/10000000.0
        print "slider 03: " + str(value)
        print "Changing addToCounter for hihat"
        hihat.addToCounter = value
        event.Skip()

    def scroll04(self, event):  # wxGlade: mainFrame.<event_handler>
        value = event.GetInt()/10000000.0
        print "slider 04: " + str(value)
        print "Changing addToCounter for synth bass"
        syn01.addToCounter = value
        event.Skip()

    def scroll05(self, event):  # wxGlade: mainFrame.<event_handler>
        value = event.GetInt()/10000000.0
        print "slider 05: " + str(value)
        print "Changing addToCounter for bass drum 2"
        tempokick.addToCounter = value
        event.Skip()

    def scroll06(self, event):  # wxGlade: mainFrame.<event_handler>
        print "slider 06: " + str(event.GetInt()/1000.0)
        event.Skip()

    def scroll07(self, event):  # wxGlade: mainFrame.<event_handler>
        print "slider 07: " + str(event.GetInt()/1000.0)
        event.Skip()

    def scroll08(self, event):  # wxGlade: mainFrame.<event_handler>
        print "slider 08: " + str(event.GetInt()/1000.0)
        event.Skip()

# end of class mainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = mainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

conn01.start()
conn02.start()
conn03.start()
conn04.start()

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

time.sleep(120.0)

conn01.stopSeq()
conn02.stopSeq()
conn03.stopSeq()
conn04.stopSeq()

conn01.join()
conn02.join()
conn03.join()
conn04.join()

time.sleep(2)

conn01.cleanup()


