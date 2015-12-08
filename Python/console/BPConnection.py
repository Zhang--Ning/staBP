import serial
import time
import sys
import glob
import wx

from datetime import datetime
from collections import deque

from numpy import sin, pi

class BPConnection:
  def __init__(self, connectedFunc, test=False):
    self.acdcFunc = None
    self.cmdlistener = None
    self.connectedFunc = connectedFunc

    self.is_connected = False

    self.currentData = ""

    self.last_command = 0

    self.acdc = deque([])
    self.lastacdc = 0
    self.commandwait = 0
    self.test = test
    if(test):
      self.testt = 0
      wx.CallLater(5,self.RunTest)

  def RunTest(self):
    self.testt = (self.testt + 0.063) % 1
    if(self.acdcFunc != None):
      self.acdcFunc(40*sin(2*pi*self.testt)+100, 5)
    wx.CallLater(5, self.RunTest)

  def SetACDCListener(self, acdcFunc):
    self.acdcFunc = acdcFunc

  def IsConnected(self):
    return self.is_connected

  def Connect(self, port):
    if(port == ""):
      return
    self.connection = serial.Serial(port, baudrate=19200)
    time.sleep(1)
    wx.CallLater(5, self.CheckForData)
    wx.CallLater(5, self.DistributeACDC)
    self.is_connected = True
    if(self.connectedFunc != None):
      self.connectedFunc()

  def Disconnect(self):
    if self.is_connected:
      self.connection.close()
      self.is_connected = False

  def CheckForData(self):
    if not self.is_connected:
      return
    num_waiting = self.connection.inWaiting()
    if(num_waiting):
      char = self.connection.read(num_waiting)
      if char.find("\r") != -1:
        if(self.cmdlistener != None):
          self.commandwait -= 1
          if(self.commandwait <= 0):
            self.commandwait = 0
            self.cmdlistener()
      else:
        self.currentData += char
        self.ParseData()
    wx.CallLater(5, self.CheckForData)

  def ParseData(self):
    index = self.currentData.find("\n")
    while index != -1:
      data = self.currentData[:index]
      self.currentData = self.currentData[index+1:]
      tokens = data.split(',')
      if len(tokens) == 2:
        try:
          ac = int(tokens[0])
          dc = int(tokens[1])
          self.acdc.append((ac, dc))
        except ValueError:
          pass
      index = self.currentData.find("\n")

  def DistributeACDC(self):
    current = time.time()*1000
    if len(self.acdc) > 0: 
      self.lastacdc = current
      [ac1, dc1] = self.acdc.popleft()
      if(self.acdcFunc != None):
        self.acdcFunc(ac1-512, dc1)

    if len(self.acdc) > 20:
      self.acdc.clear()

    wx.CallLater(1, self.DistributeACDC)

  def AdvanceMotor(self, listener, steps):
    if not self.is_connected:
      return
    print "Advance"
    self.commandwait = steps
    self.cmdlistener = listener
    self.connection.write("f"*steps)

  def RetractMotor(self, listener, steps):
    if not self.is_connected:
      return
    print "Retract"
    self.commandwait = steps
    self.cmdlistener = listener
    self.connection.write("r"*steps)

  def MotorEnable(self, listener):
    if not self.is_connected:
      return
    print "====ENABLE MOTOR====="
    self.commandwait = 1
    self.cmdlistener = listener
    self.connection.write('e')

  def MotorDisable(self, listener):
    if not self.is_connected:
      return
    print "====DISABLE MOTOR====="
    self.commandwait = 1
    self.cmdlistener = listener
    self.connection.write('d')

  def GetAvailablePorts(self):
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    return ports
