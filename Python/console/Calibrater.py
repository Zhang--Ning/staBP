import wx

class Calibrater:
	def __init__(self, connection, doneCalibrating):
		self.k1 = 0
		self.k2 = 0
		self.connection = connection
		self.doneCalibrating = doneCalibrating
		self.raw_listener = None
		self.pressure_listener = None

		self.ac_window = []
		self.dc_window = []

		self.calibration_window = 400
		self.pressure_samples = 100
		self.ma_window = 20

	def Calibrate(self, pressures):
		self.systolic = pressures[0]
		self.diastolic = pressures[1]

		self.ac_window = []
		self.dc_window = []
		self.connection.SetACDCListener(self.AddToWindow)

		self.pressure_window = []
		self.systoles = []
		self.diastoles = []

	def AddToWindow(self, ac, dc):
		if len(self.ac_window) >= self.calibration_window:
			self.GetKS()
			self.doneCalibrating()
		else:
			self.ac_window.append(ac)
			self.dc_window.append(dc)

	def SetRawPressureListener(self, listener):
		self.raw_listener = listener

	def SetPressureListener(self, listener):
		self.pressure_listener = listener

	def StartRecording(self):
		self.connection.SetACDCListener(self.NewData)

	def NewData(self, ac, dc):
		if len(self.pressure_window) >= self.pressure_samples:			
			threshold = (max(self.pressure_window)-min(self.pressure_window))*0.7+min(self.pressure_window)
			[systoles, diastoles, systimes, diatimes] = self.ExtractSysDia(self.pressure_window, threshold)
			self.AddPressure(systoles, diastoles)
			self.pressure_window = []
		else:
			self.pressure_window.append(self.k1*ac+self.k2*dc)
		if(self.raw_listener != None):
			self.raw_listener(self.k1*ac+self.k2*dc)

	def AddPressure(self, systoles, diastoles):
		for systole in systoles:
			if len(self.systoles) >= self.ma_window:
				self.systoles.pop(0)
			self.systoles.append(systole)

		for diastole in diastoles:
			if len(self.diastoles) >= self.ma_window:
				self.diastoles.pop(0)
			self.diastoles.append(diastole)

		if(self.pressure_listener != None):
			self.pressure_listener(self.mean(self.systoles), self.mean(self.diastoles))

	def GetKS(self):
		threshold = (max(self.ac_window)-min(self.ac_window))*0.7+min(self.ac_window);
		[systoles, diastoles, systimes, diatimes] = self.ExtractSysDia(self.ac_window, threshold)

		average_systole = self.mean(systoles)
		average_diastole = self.mean(diastoles)
		average_window = self.mean(self.dc_window)

		if((average_systole-average_diastole) == 0):
				average_systole += 0.01

		self.k1 = (self.systolic - self.diastolic)/(average_systole-average_diastole)
		self.k2 = (self.systolic - (self.k1*average_systole))/average_window

	def mean(self, list):
		if(len(list) == 0):
			return 0
		return float(sum(list))/float(len(list))
	def ExtractSysDia(self, blood_pressure, threshold):
		return ([max(blood_pressure)], [min(blood_pressure)], 0, 0)
		# systoles = []
		# diastoles = []
		# systimes = []
		# diatimes = []
		# train = []
		# traintimes = []
		# find_sys = True

		# for i in range(len(blood_pressure)):
		# 	pressure = blood_pressure[i]
		# 	if find_sys:
		# 		if pressure > threshold:
		# 			train.append(pressure)
		# 			traintimes.append(i)
		# 		else:
		# 			if(len(train) > 0):
		# 				maxPressure = max(train)
		# 				maxTime = traintimes[train.index(maxPressure)]
		# 				systimes.append(maxTime)
		# 				systoles.append(maxPressure)
		# 				train = []
		# 				traintimes = []
		# 			findsys = False
		# 	else:
		# 		if pressure <= threshold:
		# 			train.append(pressure)
		# 			traintimes.append(i)
		# 		else:
		# 			if(len(train) > 0):
		# 				minPressure = min(train)
		# 				minTime = traintimes[train.index(minPressure)]
		# 				diatimes.append(minTime)
		# 				diastoles.append(minPressure)
		# 				train = []
		# 				traintimes = []
		# 			findsys = True

		# return (systoles, diastoles, systimes, diatimes)
