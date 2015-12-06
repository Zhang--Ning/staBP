from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

import wx
import wx.lib.inspection

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure(facecolor="black")
        self.axes = self.figure.add_axes((0, 0, 1, 1))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        self.axes.set_axis_bgcolor('black')
        self.delta = 0
        
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * (t))
        self.datatoplot, = self.axes.plot(t, s, 'w', linewidth=3.0)
        self.axes.set_ylim((-10,10))
        self.axes.grid(True, color="w")
        
    def draw(self):
        self.delta = (self.delta + 0.05) % 1
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * (t-self.delta))
        self.datatoplot.set_ydata(s)
        
        wx.CallLater(10, self.draw)
        self.canvas.draw()
        self.canvas.Refresh()

app = wx.App(False)
frame = wx.Frame(None)
canvas = CanvasPanel(frame)
canvas.draw()
frame.Show()
wx.lib.inspection.InspectionTool().Show()
app.MainLoop()

