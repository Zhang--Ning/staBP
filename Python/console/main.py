import wx
import bp_console
import wx.lib.inspection

app = wx.App(False)
frame = bp_console.BPFrame()
#wx.lib.inspection.InspectionTool().Show()
app.MainLoop()
