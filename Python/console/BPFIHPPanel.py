import wx
from BPUtil import Scale
from BPPlotPanel import PlotPanel

class LoadingText(wx.StaticText):
    def __init__(self, parent, label):
        self.label = label
        wx.StaticText.__init__(self, parent, label=self.label)
        wx.CallLater(300, self.Advance)
        self.number = 1

    def Advance(self):
        dots = "."*(self.number)
        self.SetLabel(self.label + dots)
        self.number = (self.number + 1) % 4
        wx.CallLater(300, self.Advance)

class FIHPPanel(wx.Panel):
    def __init__(self, parent, doneFunc, test=False):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.title_panel = wx.Panel(self)
        self.sizer.Add(self.title_panel, 2, wx.EXPAND)
        self.title_text = LoadingText(self.title_panel, label="Identifying ideal hold-down pressure") 
        self.title_text.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
        self.title_text.SetForegroundColour(wx.Colour(83, 83, 83))
        hsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(self.title_text, 1, wx.ALIGN_CENTER)
        self.title_panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.title_panel.GetSizer().Add(hsizer, 1, wx.ALIGN_CENTER)

        self.plot_panel = wx.Panel(self)
        self.sizer.Add(self.plot_panel, 3, wx.EXPAND)
        self.motor = MotorProgress(self.plot_panel)
        self.plot_panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.plot_panel.GetSizer().Add(self.motor, 5, wx.EXPAND)
        self.plot_panel.GetSizer().AddStretchSpacer(1)
        self.peakpeakplot = PeakPlotPanel(self.plot_panel)
        self.plot_panel.GetSizer().Add(self.peakpeakplot, 25, wx.EXPAND)

        self.sizer.AddStretchSpacer(1)

        self.doneFunc = doneFunc
        self.test = test

        if self.test:
            self.time = 0
            wx.CallLater(1000, self.NextSim)

    def ResetPanel(self):
        self.motor.SetProgress(0)
        self.peakpeakplot.ClearPlot()

    def NextSim(self):
        self.time = (self.time + 0.063)
        if(self.time > 1):
            self.time = 0
            self.xdata = []
            self.ydata = []
            self.doneFunc()
        else:
            self.peakpeakplot.AddNextPeakPeak(self.time*100, 15*(0.25-((self.time-0.5)**2)))
            wx.CallLater(1000, self.NextSim)

    def AddNextPoint(self, motor_percentage, peaktopeak):
        self.peakpeakplot.AddNextPeakPeak(int(motor_percentage*100), peaktopeak)
        self.motor.SetProgress(int(motor_percentage*100))

    def Done(self):
        self.peakpeakplot.Disable()
        self.doneFunc()

class PeakPlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        self.plot = PlotPanel(self)
        self.plot.SetMaxSize((-1, -1))
        self.sizer.Add(self.plot, 20, wx.EXPAND)
        self.sizer.AddStretchSpacer(1)
        self.scale = Scale(self, "Volts", "", wx.ALIGN_LEFT, False)
        self.sizer.Add(self.scale, 0, wx.EXPAND)
        self.sizer.AddStretchSpacer(1)
        self.sizer.Layout()

        self.xdata = []
        self.ydata = []

        self.plot.StartPlot(self.xdata, self.ydata, (0,100), (0, None), 'ow')

    def ClearPlot(self):
        self.xdata = []
        self.ydata = []

        self.plot.StartPlot(self.xdata, self.ydata, (0,100), (0, None), 'ow')
        
    def AddNextPeakPeak(self, motorpos, peaktopeak):
        self.ydata.append(peaktopeak)
        self.xdata.append(motorpos)
        self.plot.UpdatePlot(self.xdata, self.ydata)

    def Disable(self):
        self.plot.Disable()

class MotorProgress(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)

    self.scale = Scale(self, "100%", "0%", wx.ALIGN_RIGHT)
    self.bar = wx.Panel(self)

    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.SetSizer(self.sizer)
    self.sizer.Add(self.scale, 3, wx.EXPAND)
    self.sizer.Add(self.bar, 1, wx.EXPAND)

    self.bar.SetBackgroundColour("black")

    self.progress = wx.Panel(self.bar)
    self.progress.SetBackgroundColour(wx.Colour(226, 71, 24))
    self.SetProgress(100)
    
    if False:
      wx.CallLater(150, self.Advance)
      self.progressPercentage = 0

  def Advance(self):
    self.progressPercentage = (self.progressPercentage + 1) % 100
    self.SetProgress(self.progressPercentage)
    wx.CallLater(150, self.Advance)

  def SetProgress(self, progressPercentage):
    self.vsizer = wx.BoxSizer(wx.VERTICAL)
    self.vsizer.AddStretchSpacer(105-progressPercentage)
    self.vsizer.Add(self.progress, progressPercentage, wx.EXPAND)
    self.vsizer.AddStretchSpacer(2)
    self.bar.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    self.bar.GetSizer().AddStretchSpacer(2)
    self.bar.GetSizer().Add(self.vsizer, 4, wx.EXPAND)
    self.bar.GetSizer().AddStretchSpacer(2)
    self.Layout()