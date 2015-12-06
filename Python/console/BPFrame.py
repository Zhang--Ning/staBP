import wx
import BPNav
import time

from BPPositionPanel import PositionPanel
from BPCalibratePanel import CalibratePanel
from BPFIHPPanel import FIHPPanel
from BPMonitorPanel import MonitorPanel

class BPFrame(wx.Frame):
  def __init__(self):
    no_resize_style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
    wx.Frame.__init__(self, None, title="Blood Pressure Program", pos = (5,20), size=(512, 320), style=no_resize_style)
    self.SetBackgroundColour(wx.Colour(236, 236, 236))

    ## Set up menu
    filemenu = wx.Menu()
    filemenu.Append(wx.ID_EXIT, "E&xit")
    recalibrate = filemenu.Append(wx.ID_RESET, "&Recalibrate")
    menubar = wx.MenuBar()
    menubar.Append(filemenu, "&File")
    self.SetMenuBar(menubar)
    self.Bind(wx.EVT_MENU, self.Recalibrate, recalibrate)
    self.Bind(wx.EVT_MENU_HIGHLIGHT, self.MenuHighlighted, menubar)

    ## Set up status bar
    status_bar = self.CreateStatusBar()
    status_bar.SetFieldsCount(1)
    status_bar.SetStatusText("Connected. (/dev/tty.Bluetooth-Modem, 9600-8N1)", 0)

    ## Set up box layout
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.sizer)

    ## Set up navigation bar
    self.navigation_bar = BPNav.NavBar(self)

    ## Set up main panel
    self.position_panel = PositionPanel(self, self.GoToFIHP)

    self.sizer.Add(self.navigation_bar, 1, flag=wx.EXPAND)
    self.sizer.Add(self.position_panel, 3, flag=wx.EXPAND)

    # self.GoToFIHP()
    # time.sleep(0.5)
    # self.GoToCalibrate()
    # time.sleep(0.5)
    # self.GoToMonitor()
    # time.sleep(0.5)
    
    self.Show(True)

  def GoToFIHP(self):
    self.position_panel.Show(False)
    self.fihp_panel = FIHPPanel(self, self.GoToCalibrate)
    self.sizer.Remove(self.position_panel)
    self.sizer.Add(self.fihp_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(1)

  def GoToCalibrate(self):
    self.fihp_panel.Show(False)
    self.calibrate_panel = CalibratePanel(self, self.GoToMonitor)
    self.sizer.Remove(self.fihp_panel)
    self.sizer.Add(self.calibrate_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(1)

  def GoToMonitor(self):
    self.monitor_panel = MonitorPanel(self)
    self.calibrate_panel.Show(False)
    self.sizer.Remove(self.calibrate_panel)
    self.sizer.Add(self.monitor_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(2)

  def Recalibrate(self, event):
    pass

  def MenuHighlighted(self, event):
    pass