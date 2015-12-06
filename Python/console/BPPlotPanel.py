import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure  

class PlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure(facecolor="black", figsize=(0, 0))
        self.axes = self.figure.add_axes((0, 0, 1, 1))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.axes.set_axis_bgcolor('black')

    def StartPlot(self, initial_x, initial_y, xlim, ylim, style):
        self.axes.clear()
        self.dataplot, = self.axes.plot(initial_x, initial_y, style, linewidth=3.0)
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)
        self.axes.grid(True, color="w")

    def UpdatePlot(self, new_x, new_y):
        self.dataplot.set_data(new_x, new_y)
        self.canvas.draw()
        self.canvas.Refresh()