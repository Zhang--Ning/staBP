import wx
from BPPlotPanel import PlotPanel
from BPUtil import Scale

from numpy import arange, sin, pi

class MonitorPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)

    self.sizervert = wx.BoxSizer(wx.VERTICAL)
    self.sizervert.AddStretchSpacer(2)
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.sizervert.Add(self.sizer, 15, wx.EXPAND)
    self.sizervert.AddStretchSpacer(2)
    self.SetSizer(self.sizervert)

    self.reading_panel = wx.Panel(self)

    self.plot_panel = MonitorPlotPanel(self)

    self.sizer.Add(self.reading_panel, 80, wx.EXPAND)
    self.vborder = wx.Panel(self)
    self.vborder.SetBackgroundColour(wx.Colour(60, 60, 60))
    self.vborder.SetMinSize((1,-1))
    self.vborder.SetMaxSize((1,-1))
    self.sizer.Add(self.vborder, 1, wx.EXPAND)
    self.sizer.Add(self.plot_panel, 120, wx.EXPAND)

    self.diastolic_panel = PressureReadingPanel(self.reading_panel, "DIA")
    self.systolic_panel = PressureReadingPanel(self.reading_panel, "SYS")
   
    self.systolic_panel.SetPressure(0)
    self.diastolic_panel.SetPressure(0)
    self.reading_panel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.reading_panel.GetSizer().AddStretchSpacer(5)
    self.reading_panel.GetSizer().Add(self.systolic_panel, 50, wx.EXPAND)
    self.reading_panel.GetSizer().Add(self.diastolic_panel, 50, wx.EXPAND)

  def ResetPanel(self):
    self.SetPressure(0, 0)
    self.plot_panel.ClearPlot()

  def AddRawPressure(self, pressure):
    self.plot_panel.AddNextBP(pressure)

  def SetPressure(self, systolic, diastolic):
    self.systolic_panel.SetPressure(int(systolic))
    self.diastolic_panel.SetPressure(int(diastolic))

class PressureReadingPanel(wx.Panel):
  def __init__(self, parent, label):
    wx.Panel.__init__(self, parent)
    self.labelPanel = wx.Panel(self)
    self.pressureText = wx.StaticText(self, label="120", style=wx.ALIGN_RIGHT)
    self.pressureText.SetForegroundColour(wx.Colour(226, 71, 24))
    self.pressureText.SetFont(wx.Font(80, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, faceName="Helvetica Neue"))
    self.labelText = wx.StaticText(self.labelPanel, label=label)
    self.labelText.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, faceName="Helvetica Neue"))
    self.unitsText = wx.StaticText(self.labelPanel, label="mmHg")
    self.unitsText.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.labelText.SetForegroundColour(wx.Colour(226, 71, 24))
    self.unitsText.SetForegroundColour(wx.Colour(226, 71, 24))
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.sizer.Add(self.pressureText, 7, wx.EXPAND)
    self.sizer.AddStretchSpacer(1)
    self.sizer.Add(self.labelPanel, 3, wx.EXPAND)
    self.SetSizer(self.sizer)

    self.labelPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.labelPanel.GetSizer().Add(self.labelText, 0, border=18, flag=wx.EXPAND | wx.TOP)
    self.labelPanel.GetSizer().Add(self.unitsText, 0, wx.EXPAND)
    self.labelPanel.GetSizer().AddStretchSpacer(3)

  def SetPressure(self, pressure):
    self.pressureText.SetLabel(str(pressure))
    self.Layout()


class MonitorPlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        self.plot = PlotPanel(self)
        self.plot.SetMaxSize((-1, -1))
        self.sizer.Add(self.plot, 20, wx.EXPAND)
        self.sizer.AddStretchSpacer(1)
        self.scale = Scale(self, "200 mmHg", "40 mmHg", wx.ALIGN_LEFT)
        self.sizer.Add(self.scale, 0, wx.EXPAND)
        self.sizer.AddStretchSpacer(1)
        self.sizer.Layout()

        self.xdata = range(100)
        self.ydata = [80]*100

        self.bpindex = 0

        if False:
            self.time = 0
            wx.CallLater(10, self.NextSim)

    def ClearPlot(self):
        self.xdata = range(100)
        self.ydata = [80]*100

        self.bpindex = 0

        self.plot.StartPlot(self.xdata, self.ydata, (0,99), (40,200), '-w')

    def NextSim(self):
        self.time = (self.time + 0.063) % 1
        self.AddNextBP(40*sin(2*pi*self.time)+100)
        wx.CallLater(10, self.NextSim)

    def AddNextBP(self, pressure):
        self.ydata.pop(0)
        self.ydata.append(pressure)
        self.plot.UpdatePlot(self.xdata, self.ydata)