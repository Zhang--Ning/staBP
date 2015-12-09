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
    self.items.append(TitlePanel(self, "CONNECT", "wifi.png", 1))
    self.items.append(TitlePanel(self, "POSITION", "head 2.png", 1))
    self.items.append(TitlePanel(self, "AUTOCOMPRESS", "head 2.png", 1))
    self.items.append(TitlePanel(self, "CALIBRATE", "cuff 2.png", 1))
    self.items.append(TitlePanel(self, "MONITOR", "head 2.png", 1))

    for item in self.items:
      item.Show(False)

    self.SelectItem(0)
    
  def SelectItem(self, item_no):
    self.sizer.Clear()
    for item_index in range(len(self.items)):
      if item_index == item_no:
        self.items[item_index].Show(True)
        self.sizer.Add(self.items[item_index], 1, flag=wx.ALIGN_CENTER_VERTICAL)
      else:
        self.items[item_index].Show(False)


class TitlePanel(wx.Panel):
    def __init__(self, parent, text, filename, scale):
        wx.Panel.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        self.head_panel = wx.Panel(self)
        head_panel_sizer_v = wx.BoxSizer(wx.VERTICAL)
        head_panel_sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        head_panel_sizer_v.Add(head_panel_sizer_h, 1, wx.CENTER)
        self.head_panel.SetSizer(head_panel_sizer_v)

        img_scalefactor = scale
        self.image = wx.Image(filename, wx.BITMAP_TYPE_PNG)
        self.image.Rescale(self.image.GetWidth()*img_scalefactor, self.image.GetHeight()*img_scalefactor)
        self.bitmap = wx.StaticBitmap(self.head_panel, wx.ID_ANY, wx.BitmapFromImage(self.image))
        head_panel_sizer_h.Add(self.bitmap, 1, flag=wx.CENTER)

        self.sizer.Add(self.head_panel, 0, border=10, flag=wx.EXPAND | wx.ALL)

        self.textPanel = wx.Panel(self)
        self.textPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.text = wx.StaticText(self.textPanel, label=text)
        self.text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, faceName="Helvetica Neue"))
        self.text.SetForegroundColour("white")
        self.textPanel.GetSizer().Add(self.text, 0, wx.ALIGN_CENTER)

        self.sizer.Add(self.textPanel, 1, border=10, flag=wx.EXPAND|wx.LEFT)

    def SetText(self, text):
        self.textPanel.SetLabel(text)
        self.sizer.Layout()