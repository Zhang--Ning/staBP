import wx
from BPUtil import Button

class SelectDevicePanel(wx.Panel):
	def __init__(self, parent, connection, selectedFunc):
		wx.Panel.__init__(self, parent)

		self.connection = connection
		self.selectedFunc = selectedFunc

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)

		self.directionsText = wx.StaticText(self, label="Select a device:")
		self.directionsText.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
		self.directionsText.SetForegroundColour(wx.Colour(83, 83, 83))

		self.portsList = wx.Panel(self)
		self.portsList.SetSizer(wx.BoxSizer(wx.VERTICAL))

		self.sizer.AddStretchSpacer(1)
		self.sizer.Add(self.directionsText, 0, wx.EXPAND | wx.LEFT, border=10)
		self.sizer.AddStretchSpacer(1)
		self.sizer.Add(self.portsList, 8, wx.EXPAND)

		self.check = True
		self.portsList.SetBackgroundColour("white")
		wx.CallLater(2000, self.CheckConnections)

	def CheckConnections(self):
		devices = self.connection.GetAvailablePorts()

		self.portsList.GetSizer().Clear()
		for device in devices:
			self.portsList.GetSizer().Add(Button(self.portsList, lambda: self.PortSelected(device), device), 0, wx.EXPAND | wx.LEFT | wx.TOP, border=10)

		self.portsList.GetSizer().Layout()


		if self.check:
			wx.CallLater(2000, self.CheckConnections)

	def PortSelected(self, port):
		self.check = False
		self.selectedFunc(port)