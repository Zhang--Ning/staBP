import wx

class ContinueButton(wx.StaticText):
  def __init__(self, parent, clickHandler):
    wx.StaticText.__init__(self, parent, label="Continue \xe2\x9e\x94")
    self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, faceName="Helvetica Neue")
    self.color_normal = wx.Colour(0, 209, 245)
    self.color_hover = wx.Colour(0, 167, 195)
    self.SetForegroundColour(self.color_normal)
    self.Bind(wx.EVT_LEFT_UP, self.Clicked)
    self.Bind(wx.EVT_ENTER_WINDOW, self.HoverOn)
    self.Bind(wx.EVT_LEAVE_WINDOW, self.HoverOff)

    cursor = wx.StockCursor(wx.CURSOR_HAND)
    self.SetCursor(cursor)

    self.clickHandler = clickHandler

  def HoverOff(self, event):
    self.SetForegroundColour(self.color_normal)

  def HoverOn(self, event):
    self.SetForegroundColour(self.color_hover)   

  def Clicked(self, event):
    self.clickHandler()

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

class Scale(wx.Panel):
    def __init__(self, parent, maxText, minText, align):
        wx.Panel.__init__(self, parent)

        scalefont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, faceName="Helvetica Neue")
        scalecolor = wx.Colour(80, 80, 80)

        self.onehundred = wx.StaticText(self, label=maxText)
        self.onehundred.SetFont(scalefont)
        self.onehundred.SetForegroundColour(scalecolor)

        self.seventyfive = wx.StaticText(self, label="-")
        self.seventyfive.SetFont(scalefont)
        self.seventyfive.SetForegroundColour(scalecolor)

        self.fifty = wx.StaticText(self, label="-")
        self.fifty.SetFont(scalefont)
        self.fifty.SetForegroundColour(scalecolor)

        self.twentyfive = wx.StaticText(self, label="-")
        self.twentyfive.SetFont(scalefont)
        self.twentyfive.SetForegroundColour(scalecolor)

        self.zero = wx.StaticText(self, label=minText)
        self.zero.SetFont(scalefont)
        self.zero.SetForegroundColour(scalecolor)

        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        self.sonehundred = wx.BoxSizer(wx.HORIZONTAL)
        self.sonehundred.Add(self.onehundred, 1, wx.ALIGN_TOP)
        self.sseventyfive = wx.BoxSizer(wx.HORIZONTAL)
        self.sseventyfive.Add(self.seventyfive, 1, wx.CENTER)
        self.sfifty = wx.BoxSizer(wx.HORIZONTAL)
        self.sfifty.Add(self.fifty, 1, wx.CENTER)
        self.stwentyfive = wx.BoxSizer(wx.HORIZONTAL)
        self.stwentyfive.Add(self.twentyfive, 1, wx.CENTER)
        self.szero = wx.BoxSizer(wx.HORIZONTAL)
        self.szero.Add(self.zero, 1, wx.ALIGN_BOTTOM)

        self.GetSizer().Add(self.sonehundred, 0, align)
        self.GetSizer().Add(self.sseventyfive, 1, align)
        self.GetSizer().Add(self.sfifty, 1, align)
        self.GetSizer().Add(self.stwentyfive, 1, align)
        self.GetSizer().Add(self.szero, 1, align)