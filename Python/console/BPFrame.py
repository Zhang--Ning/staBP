import wx
import BPNav
import time

from BPSelectDevice import SelectDevicePanel
from BPPositionPanel import PositionPanel
from BPCalibratePanel import CalibratePanel
from BPFIHPPanel import FIHPPanel
from BPMonitorPanel import MonitorPanel
from BPConnection import BPConnection
from FIHPDriver import FIHPDriver
from Calibrater import Calibrater

class BPFrame(wx.Frame):
  def __init__(self):
    no_resize_style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
    wx.Frame.__init__(self, None, title="Blood Pressure Program", pos = (5,20), size=(512, 320), style=no_resize_style)
    self.SetBackgroundColour(wx.Colour(236, 236, 236))

    ## Set up menu
    filemenu = wx.Menu()
    exit = filemenu.Append(wx.ID_EXIT, "E&xit")
    recalibrate = filemenu.Append(wx.ID_RESET, "&Recalibrate")
    menubar = wx.MenuBar()
    menubar.Append(filemenu, "&File")
    self.SetMenuBar(menubar)
    self.Bind(wx.EVT_MENU, self.Recalibrate, recalibrate)
    self.Bind(wx.EVT_MENU_HIGHLIGHT, self.MenuHighlighted, menubar)
    self.Bind(wx.EVT_MENU, self.Exit, exit)

    ## Set up status bar
    self.status_bar = self.CreateStatusBar()
    self.status_bar.SetFieldsCount(1)
    self.status_bar.SetStatusText("Not Connected.", 0)

    ## Set up box layout
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.sizer)

    ## Set up navigation bar
    self.navigation_bar = BPNav.NavBar(self)

    ## Set up main panel
    self.connection = BPConnection(None)

    self.select_panel = SelectDevicePanel(self, self.connection, self.GoToPosition)

    self.sizer.Add(self.navigation_bar, 1, flag=wx.EXPAND)
    self.sizer.Add(self.select_panel, 3, flag=wx.EXPAND)

    # self.GoToPosition("")
    # time.sleep(0.5)
    # self.GoToFIHP()
    # time.sleep(0.5)
    # self.GoToCalibrate()
    # time.sleep(0.5)
    # self.GoToMonitor()
    # time.sleep(0.5)

    self.Show(True)

  def SetConnectedText(self, port):
    self.status_bar.SetStatusText("Connected. (" + port + ", 19200-8N1)", 0)

  def GoToPosition(self, selected):
    self.connection.Connect(selected) 
    self.SetConnectedText(selected)
    self.select_panel.Show(False)
    self.position_panel = PositionPanel(self, self.GoToFIHP)
    self.sizer.Remove(self.select_panel)
    self.sizer.Add(self.position_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(1)

  def GoToFIHP(self):
    self.position_panel.Show(False)
    self.fihp_panel = FIHPPanel(self, self.GoToCalibrate, test=False)
    self.sizer.Remove(self.position_panel)
    self.sizer.Add(self.fihp_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(1)
    self.driver = FIHPDriver(self.connection, self.fihp_panel.AddNextPoint, self.fihp_panel.Done)

  def GoToCalibrate(self):
    self.fihp_panel.Show(False)
    self.calibrater = Calibrater(self.connection, self.GoToMonitor)
    self.calibrate_panel = CalibratePanel(self, self.calibrater.Calibrate)
    self.sizer.Remove(self.fihp_panel)
    self.sizer.Add(self.calibrate_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(1)

  def GoToMonitor(self):
    print "Go To Monitor"
    self.monitor_panel = MonitorPanel(self)
    self.calibrate_panel.Show(False)
    self.sizer.Remove(self.calibrate_panel)
    self.sizer.Add(self.monitor_panel, 3, flag=wx.EXPAND)
    self.sizer.Layout()
    self.navigation_bar.SelectItem(2)
    self.calibrater.SetRawPressureListener(self.monitor_panel.AddRawPressure)
    self.calibrater.SetPressureListener(self.monitor_panel.SetPressure)
    self.calibrater.StartRecording()

  def Recalibrate(self, event):
    pass

  def MenuHighlighted(self, event):
    pass

  def Exit(self, event):
    self.connection.Disconnect()
    event.Skip()
