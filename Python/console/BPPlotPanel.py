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

        self.render = False

        wx.CallLater(50, self.Render)

    def StartPlot(self, initial_x, initial_y, xlim, ylim, style):
        self.xdata = initial_x
        self.ydata = initial_y
        self.axes.clear()
        self.dataplot, = self.axes.plot(initial_x, initial_y, style, linewidth=3.0)
        if(xlim != -1):
            self.axes.set_xlim(xlim)
            self.autoscale_x = False
        else:
            self.autoscale_x = True
        if(ylim != -1):
            self.axes.set_ylim(ylim)
            self.autoscale_y = False
        else:
            self.autoscale_y = True
        self.axes.grid(True, color="w")
        self.render = True

    def UpdatePlot(self, new_x, new_y):
        self.xdata = new_x
        self.ydata = new_y
        self.dataplot.set_data(new_x, new_y)

    def Render(self):
        if self.render and len(self.xdata) > 0 and len(self.xdata) == len(self.ydata):   
            if(self.autoscale_x and len(self.xdata) > 1):
                self.axes.set_xlim((min(self.xdata), max(self.xdata)))
            if(self.autoscale_y and len(self.ydata) > 1):
                self.axes.set_ylim((min(self.ydata), max(self.ydata)))
            self.canvas.draw()
            self.canvas.Refresh()
        wx.CallLater(50, self.Render)

    def Disable(self):
        self.render = False