import wx
from BPUtil import Button

class PositionPanel(wx.Panel):
  def __init__(self, parent, doneFunc):
    wx.Panel.__init__(self, parent)
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.SetSizer(self.sizer)

    self.head_panel = wx.Panel(self)
    head_panel_sizer_v = wx.BoxSizer(wx.VERTICAL)
    head_panel_sizer_h = wx.BoxSizer(wx.HORIZONTAL)
    head_panel_sizer_v.Add(head_panel_sizer_h, 1, wx.CENTER)
    self.head_panel.SetSizer(head_panel_sizer_v)

    img_scalefactor = 0.5
    self.head_image = wx.Image("head.png", wx.BITMAP_TYPE_PNG)
    self.head_image.Rescale(self.head_image.GetWidth()*img_scalefactor, self.head_image.GetHeight()*img_scalefactor)
    self.head_bitmap = wx.StaticBitmap(self.head_panel, wx.ID_ANY, wx.BitmapFromImage(self.head_image))
    head_panel_sizer_h.Add(self.head_bitmap, 1, flag=wx.CENTER)
    self.sizer.Add(self.head_panel, 2, flag=wx.EXPAND)

    self.textPanel = wx.Panel(self)
    self.textPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.directionsText = wx.StaticText(self.textPanel, label="Put the blood pressure headset\non your head.")
    self.directionsText.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.directionsText.SetForegroundColour(wx.Colour(83, 83, 83))

    self.continueText = Button(self.textPanel, doneFunc)

    self.textPanel.GetSizer().Add(self.directionsText, 2)
    self.textPanel.GetSizer().AddStretchSpacer(1)
    self.textPanel.GetSizer().Add(self.continueText, 1)
    self.sizer.Add(self.textPanel, 3, flag=wx.CENTER)