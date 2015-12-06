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