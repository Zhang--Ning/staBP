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
    wx.Frame.__init__(self, None, title="Blood Pressure Program", pos = (5,20), size=(768, 480), style=no_resize_style)
    self.SetBackgroundColour(wx.Colour(236, 236, 236))

    ## Set up menu
    filemenu = wx.Menu()
    exit = filemenu.Append(wx.ID_EXIT, "E&xit")
    recalibrate = filemenu.Append(wx.ID_RESET, "&Recalibrate")
    findihp = filemenu.Append(wx.ID_NEW, "&Relocate Ideal Hold-Down Pressure")
    menubar = wx.MenuBar()
    menubar.Append(filemenu, "&File")
    self.SetMenuBar(menubar)
    self.Bind(wx.EVT_MENU, self.Recalibrate, recalibrate)
    self.Bind(wx.EVT_MENU, self.FindIHP, findihp)
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
    self.connection = BPConnection(None, test=False)

    self.select_panel = SelectDevicePanel(self, self.connection, self.GoToPosition)

    self.position_panel = PositionPanel(self, self.GoToFIHP)
    self.fihp_panel = FIHPPanel(self, self.GoToCalibrate, test=False)
    self.calibrater = Calibrater(self.connection, self.GoToMonitor)
    self.calibrate_panel = CalibratePanel(self, self.calibrater.Calibrate)
    self.monitor_panel = MonitorPanel(self)
    self.driver = FIHPDriver(self.connection, self.fihp_panel.UpdateMotor, self.fihp_panel.AddNextPoint, self.fihp_panel.Done)

    self.ClearPanels()

    self.sizer.Add(self.select_panel, 3, flag=wx.EXPAND)
    self.select_panel.Show(True)

    # self.GoToPosition("")
    # time.sleep(0.5)
    # self.GoToFIHP()
    # time.sleep(0.5)
    # self.GoToCalibrate()
    # time.sleep(0.5)
    self.GoToMonitor()
    # time.sleep(0.5)

    self.Show(True)

  def ClearPanels(self):
    self.select_panel.Show(False)
    self.position_panel.Show(False)
    self.fihp_panel.Show(False)
    self.calibrate_panel.Show(False)
    self.monitor_panel.Show(False)
    self.sizer.Clear()
    self.sizer.Add(self.navigation_bar, 1, flag=wx.EXPAND)

  def SetConnectedText(self, port):
    self.status_bar.SetStatusText("Connected. (" + port + ", 19200-8N1)", 0)

  def GoToPosition(self, selected):
    self.ClearPanels()
    self.connection.Connect(selected) 
    self.SetConnectedText(selected)
    self.position_panel.ResetPanel()
    self.position_panel.Show(True)
    self.sizer.Add(self.position_panel, 3, flag=wx.EXPAND)
    self.navigation_bar.SelectItem(1)
    self.sizer.Layout()

  def GoToFIHP(self):
    self.ClearPanels()
    self.fihp_panel.ResetPanel()
    self.driver.Reset()
    self.fihp_panel.Show(True)
    self.sizer.Add(self.fihp_panel, 3, flag=wx.EXPAND)
    self.navigation_bar.SelectItem(2)
    self.sizer.Layout()

  def GoToCalibrate(self):
    self.ClearPanels()
    self.calibrater.Reset()
    self.calibrate_panel.ResetPanel()
    self.calibrate_panel.Show(True)
    self.sizer.Add(self.calibrate_panel, 3, flag=wx.EXPAND)
    self.navigation_bar.SelectItem(3)
    self.sizer.Layout()

  def GoToMonitor(self):
    self.ClearPanels()
    self.monitor_panel.ResetPanel()
    self.monitor_panel.Show(True)
    self.sizer.Add(self.monitor_panel, 3, flag=wx.EXPAND)
    self.navigation_bar.SelectItem(4)
    self.sizer.Layout()
    self.calibrater.SetRawPressureListener(self.monitor_panel.AddRawPressure)
    self.calibrater.SetPressureListener(self.monitor_panel.SetPressure)
    self.calibrater.StartRecording()

  def FindIHP(self, event):
    print "Find IHP"
    if not self.connection.IsConnected():
        return
    self.GoToFIHP()

  def Recalibrate(self, event):
    print "Recalibrate"
    if not self.connection.IsConnected():
        return
    self.GoToCalibrate()

  def MenuHighlighted(self, event):
    pass

  def Exit(self, event):
    self.connection.MotorDisable(None)
    self.connection.Disconnect()
    event.Skip()
