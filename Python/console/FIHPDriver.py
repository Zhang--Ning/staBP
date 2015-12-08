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

		self.crests = []
		self.positions = []

	  	self.connection.MotorEnable(self.Update)

	  	self.samples_per_step = 300
	  	self.total_steps = 50

	def Update(self):
		if self.state == "RETRACT":
			self.state = "SWEEP"
			self.motor_position = 0
			self.crests = []
			self.max_crest = 0
			self.max_crest_pos = 0
			self.positions = []
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
			self.state = "COMPLETE"
			self.connection.AdvanceMotor(self.Update, self.GetIHP())
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
		self.crests.append(crest)
		self.positions.append(self.motor_position)
		self.dataPointFunc(float(self.motor_position)/self.total_steps, 5.0*float(crest)/1024.0)
		self.window = []
		self.Update()

	def GetIHP(self):
		new_crests = []
		crest_positions = []
		for i in range(len(self.crests)):
			crest = self.crests[i]
			print "Crest " + str(i) + ": " + str(crest)
			if len(new_crests) > 0:
				last_crest = new_crests[-1]
			else:
				last_crest = 10
			if(float(crest)/last_crest > 10):
				print "Throwing out point " + str(i) + ". Point 1: " + str(crest) + ". Last point: " + str(last_crest)
			else:
				new_crests.append(crest)
				crest_positions.append(self.positions[i])

		maxCrest = max(new_crests)
		maxCrestI = new_crests.index(maxCrest)
		return crest_positions[maxCrestI]