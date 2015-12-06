import wx
from BPUtil import InputText, ContinueButton

class CalibratePanel(wx.Panel):
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
    self.head_image = wx.Image("cuff.png", wx.BITMAP_TYPE_PNG)
    self.head_image.Rescale(self.head_image.GetWidth()*img_scalefactor, self.head_image.GetHeight()*img_scalefactor)
    self.head_bitmap = wx.StaticBitmap(self.head_panel, wx.ID_ANY, wx.BitmapFromImage(self.head_image))
    head_panel_sizer_h.Add(self.head_bitmap, 1, flag=wx.CENTER)
    self.sizer.Add(self.head_panel, 2, flag=wx.EXPAND)

    self.textPanel = wx.Panel(self)
    self.textPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.directionsText = wx.StaticText(self.textPanel, label="Measure your current blood pressure\nand enter it below.")
    self.directionsText.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.directionsText.SetForegroundColour(wx.Colour(83, 83, 83))

    self.bpInputPanel = wx.Panel(self.textPanel)
    self.bpInputPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

    self.bpInputLabelPanel = wx.Panel(self.bpInputPanel)
    self.bpInputLabelPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.bpInputLabelPanel.GetSizer().Add(InputText(self.bpInputLabelPanel, "Systolic", "(mmHg)"), 2)
    self.bpInputLabelPanel.GetSizer().AddStretchSpacer(3)
    self.bpInputLabelPanel.GetSizer().Add(InputText(self.bpInputLabelPanel, "Diastolic", "(mmHg)"), 2)

    self.bpInputFieldPanel = wx.Panel(self.bpInputPanel)

    self.systolicField = wx.TextCtrl(self.bpInputFieldPanel, value="125", size=(50, 30))
    self.systolicField.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.systolicField.SetForegroundColour(wx.Colour(83, 83, 83))
    self.diastolicField  = wx.TextCtrl(self.bpInputFieldPanel, value="79", size=(50, 30))
    self.diastolicField.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.diastolicField.SetForegroundColour(wx.Colour(83, 83, 83))

    self.systolicField.Bind(wx.EVT_CHAR, self.LimitToInt)
    self.diastolicField.Bind(wx.EVT_CHAR, self.LimitToInt)

    self.bpInputFieldPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
    self.bpInputFieldPanel.GetSizer().Add(self.systolicField, 2)
    self.bpInputFieldPanel.GetSizer().AddStretchSpacer(1)
    self.bpInputFieldPanel.GetSizer().Add(self.diastolicField, 2)

    self.bpInputPanel.GetSizer().Add(self.bpInputLabelPanel, 10)
    self.bpInputPanel.GetSizer().AddStretchSpacer(1)
    self.bpInputPanel.GetSizer().Add(self.bpInputFieldPanel, 4)

    self.continueText = ContinueButton(self.textPanel, doneFunc)

    self.textPanel.GetSizer().Add(self.directionsText, 2)
    self.textPanel.GetSizer().AddStretchSpacer(1)
    self.textPanel.GetSizer().Add(self.bpInputPanel, 4)
    self.textPanel.GetSizer().Add(self.continueText, 1)

    self.sizer.Add(self.textPanel, 3, flag=wx.CENTER)

  def LimitToInt(self, event):
    keycode = event.GetKeyCode()
    if keycode < 255:
      if chr(keycode).isdigit():
        event.Skip()

  def GetBP(self):
    return (int(self.systolicField.GetLineText(0)), int(self.diastolicField.GetLineText(0)))