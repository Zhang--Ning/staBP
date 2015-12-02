#!/usr/bin/env python
import wx

class MyFrame(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(200,100))
    self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

    self.CreateStatusBar()
    filemenu = wx.Menu()
    aboutMenuItem = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
    filemenu.AppendSeparator()
    filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

    menubar = wx.MenuBar()
    menubar.Append(filemenu, "&File")
    self.SetMenuBar(menubar)

    self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)

    self.Show(True)
  def OnAbout(self, event):
    dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = MyFrame(None, "Small Editor") # A Frame is a top-level window.
app.MainLoop()
