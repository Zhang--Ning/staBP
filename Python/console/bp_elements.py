import wx

class NavItem(wx.Panel):
  def __init__(self, parent, number, title):
    wx.Panel.__init__(self, parent)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.sizer)

    self.number_label = wx.StaticText(self, style=wx.ALIGN_CENTER, label=str(number))
    self.number_label.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, faceName="Helvetica Neue"))
    self.name_label = wx.StaticText(self, style=wx.ALIGN_CENTER, label=title)
    self.name_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))

    self.sizer.Add(self.number_label, 1, flag=wx.EXPAND) 
    self.sizer.Add(self.name_label, 1, flag=wx.EXPAND)

    self.SetActive(False)

  def IsActive(self):
    return self.is_active

  def SetActive(self, is_active):
    self.is_active = is_active

    if(is_active):
      color = wx.Colour(234, 237, 237)
    else:
      color = wx.Colour(100, 100, 100)

    self.number_label.SetForegroundColour(color)
    self.name_label.SetForegroundColour(color)

class NavBar(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.SetBackgroundColour(wx.Colour(40, 40, 40))
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.SetSizer(self.sizer)

    self.items = []
    self.items.append(NavItem(self, 1, "Position"))
    self.items.append(NavItem(self, 2, "Calibrate"))
    self.items.append(NavItem(self, 3, "Monitor"))

    self.AddItems()

    self.SelectItem(0)

  def AddItems(self):
    for item in self.items:
      self.sizer.Add(item, 1, flag=wx.ALIGN_CENTER_VERTICAL)
    
  def SelectItem(self, item_no):
    for item_index in range(len(self.items)):
      if item_index == item_no:
        self.items[item_index].SetActive(True)
      else:
        self.items[item_index].SetActive(False)
  
class ContinueButton(wx.StaticText):
  def __init__(self, parent, clickHandler):
    wx.StaticText.__init__(self, parent, label="Continue \xe2\x9e\x94")
    self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, faceName="Helvetica Neue")
    self.color_normal = wx.Colour(0, 209, 245)
    self.color_hover = wx.Colour(0, 167, 195)
    self.SetForegroundColour(self.color_normal)
    self.Bind(wx.EVT_LEFT_UP, clickHandler)
    self.Bind(wx.EVT_ENTER_WINDOW, self.HoverOn)
    self.Bind(wx.EVT_LEAVE_WINDOW, self.HoverOff)

    cursor = wx.StockCursor(wx.CURSOR_HAND)
    self.SetCursor(cursor)

  def HoverOff(self, event):
    self.SetForegroundColour(self.color_normal)

  def HoverOn(self, event):
    self.SetForegroundColour(self.color_hover)     

class PositionPanel(wx.Panel):
  def __init__(self, parent, continueHandler):
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

    self.continueText = ContinueButton(self.textPanel, continueHandler)

    self.textPanel.GetSizer().Add(self.directionsText, 2)
    self.textPanel.GetSizer().AddStretchSpacer(1)
    self.textPanel.GetSizer().Add(self.continueText, 1)
    self.sizer.Add(self.textPanel, 3, flag=wx.CENTER)

class CalibratePanel(wx.Panel):
  def __init__(self, parent, continueHandler):
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

    self.continueText = ContinueButton(self.textPanel, continueHandler)

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

class InputText(wx.Panel):
  def __init__(self, parent, boldText, normalText):
    wx.Panel.__init__(self, parent) 
    self.boldText = wx.StaticText(self, label=boldText)
    self.boldText.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, faceName="Helvetica Neue"))
    self.boldText.SetForegroundColour(wx.Colour(83, 83, 83))
    self.normalText = wx.StaticText(self, label=normalText) 
    self.normalText.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue"))
    self.normalText.SetForegroundColour(wx.Colour(83, 83, 83))
    
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.sizer.Add(self.boldText, 0)
    self.sizer.Add(self.normalText, 0)

    self.SetSizer(self.sizer)


class MonitorPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
