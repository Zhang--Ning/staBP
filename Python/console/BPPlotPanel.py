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
        if(ylim != -1):
            self.axes.set_ylim(ylim)

        self.xlim = xlim
        self.ylim = ylim
        self.axes.grid(True, color="w")
        self.render = True

    def UpdatePlot(self, new_x, new_y):
        self.xdata = new_x
        self.ydata = new_y
        self.dataplot.set_data(new_x, new_y)

    def Render(self):
        if self.render and len(self.xdata) > 0 and len(self.xdata) == len(self.ydata):
            xlim = list(self.xlim)
            ylim = list(self.ylim)
            if(self.xlim[0] == None):
                xlim[0] = min(self.xdata)-1
            if(self.xlim[1] == None):
                xlim[1] = max(self.xdata)+1
            if(self.ylim[0] == None):
                ylim[0] = min(self.ydata)-1
            if(self.ylim[1] == None):
                ylim[1] = max(self.ydata)+1
            self.axes.set_xlim(xlim)
            self.axes.set_ylim(ylim)
            self.canvas.draw()
            self.canvas.Refresh()
        wx.CallLater(50, self.Render)

    def Disable(self):
        self.render = False