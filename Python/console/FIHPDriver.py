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
		self.retract_steps = 0
		self.window = []

	  	self.connection.MotorEnable(self.Update)

	  	self.samples_per_step = 100
	  	self.total_steps = 10

	def Update(self):
		print self.state
		if self.state == "RETRACT":
			if self.retract_steps >= self.total_steps:
				self.state = "SWEEP"
				self.motor_position = 0
				self.retract_steps = 0
				wx.CallLater(5, self.Update)
			else:
				self.connection.RetractMotor(self.Update, 5)
				self.retract_steps += 1
		elif self.state == "SWEEP":
			if self.motor_position >= self.total_steps:
				self.state = "RETRACT2"
				wx.CallLater(5, self.Update)
			else:
				self.motor_position += 1
				self.connection.AdvanceMotor(self.RecordWindow, 5)
		elif self.state == "RETRACT2":
			print str(self.retract_steps) + ">=" + str(self.total_steps) + "?"
			if self.retract_steps >= self.total_steps:
				print "Finished retract2"
				self.state = "FINDIHP"
				self.motor_position = 0
				self.retract_steps = 0
				wx.CallLater(5, self.Update)
			else:
				self.connection.RetractMotor(self.Update, 5)
				self.retract_steps += 1
		elif self.state == "FINDIHP":
			print str(self.motor_position) + "==" + str(self.max_crest_pos) + "?"
			if self.motor_position == self.max_crest_pos:
				print "Finished FINDIHP: " + str(self.completedFunc)
				self.completedFunc()
				self.connection.MotorDisable(None)
			else:
				self.connection.AdvanceMotor(self.Update, 5)
				self.motor_position += 1
				
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
