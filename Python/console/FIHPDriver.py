import wx

class FIHPDriver:
	def __init__(self, connection, dataPointFunc, completedFunc):
		self.completedFunc = completedFunc
		self.dataPointFunc = dataPointFunc
		self.connection = connection

		self.state = "RETRACT"
		self.motor_position = 0
		self.max_crest = 0
		self.max_crest_pos = 0
		self.window = []

	  	self.connection.MotorEnable(self.Update)

	  	self.samples_per_step = 300
	  	self.total_steps = 50

	def Update(self):
		print self.state
		if self.state == "RETRACT":
			self.state = "SWEEP"
			self.motor_position = 0
			self.connection.RetractMotor(self.Update, self.total_steps)
		elif self.state == "SWEEP":
			if self.motor_position >= self.total_steps:
				self.state = "RETRACT2"
				wx.CallLater(5, self.Update)
			else:
				self.motor_position += 5
				self.connection.AdvanceMotor(self.RecordWindow, 5)
		elif self.state == "RETRACT2":
			self.state = "FINDIHP"
			self.motor_position = 0
			self.connection.RetractMotor(self.Update, self.total_steps)
		elif self.state == "FINDIHP":
			self.motor_position = self.max_crest_pos
			self.state = "COMPLETE"
			self.connection.AdvanceMotor(self.Update, abs(self.max_crest_pos-5))
		elif self.state == "COMPLETE":
			self.completedFunc()
			self.connection.MotorDisable(None)
				
	def RecordWindow(self):
		self.connection.SetACDCListener(self.NewWindowData)

	def NewWindowData(self, ac, dc):
		self.window.append(ac)
		if(len(self.window) > self.samples_per_step):
			self.connection.SetACDCListener(None)
			self.CalculateWindowCrest()

	def CalculateWindowCrest(self):
		crest = max(self.window)-min(self.window)
		self.dataPointFunc(float(self.motor_position)/self.total_steps, 5.0*float(crest)/1024.0)
		if crest > self.max_crest:
			self.max_crest = crest
			self.max_crest_pos = self.motor_position
		self.window = []
		self.Update()
