import wx
import BPFrame
import wx.lib.inspection

app = wx.App(False)
frame = BPFrame.BPFrame()
#wx.lib.inspection.InspectionTool().Show()
app.MainLoop()
