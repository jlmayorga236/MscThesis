# -------------------------- #
# -
# -
# -------------------------- #
import smbus
import math
import time
class IMU():

	def __init__(self,Name,Port,I2C_ADDR_ACC=0x6b,I2C_ADDR_GYR=0x6b,I2C_ADDR_MAG=0x1e):
		self.Name = Name
		self.Port = Port
		self.I2C_ADDR_ACC = I2C_ADDR_ACC
		self.I2C_ADDR_GYR = I2C_ADDR_GYR
		self.I2C_ADDR_MAG = I2C_ADDR_MAG
		self.I2C_CONN = smbus.SMBus(self.Port)

		self.Pitch0 = 0.0
		self.Roll0 = 0.0

	def Init(self):

		# Devices Power Mode Address
		# -- Accelerometer Power Mode
		self.Acc_Power_Addrs = 0x20 #CTRL_REG6_XL
		# -- Gyroscope     Power Mode
		self.AccGyro_Power_Addrs   = 0x10 #CTRL_REG1_G
		# -- Magnetometer  Power Mode
		self.Magn_Power_Addrs = 0x22 #CTRL_REG3_M

		self.I2C_CONN.write_byte_data(self.I2C_ADDR_ACC,0x1e,0x38)
		self.I2C_CONN.write_byte_data(self.I2C_ADDR_GYR,0x1f,0x38)
		self.I2C_CONN.write_byte_data(self.I2C_ADDR_ACC,0x10,0x40)
		self.I2C_CONN.write_byte_data(self.I2C_ADDR_MAG ,0x22,0x00)

		self.updatePitch()
		self.Pitch0 = self.Pitch

		self.updateRoll()
		self.Roll0 = self.Roll
		
		

	def updatePitch(self):
		xAccl = self.getAcc_ax()
		yAccl = self.getAcc_ay()
		zAccl = self.getAcc_az()
		R = math.sqrt(xAccl*xAccl + yAccl*yAccl + zAccl*zAccl) + 0.000000001
		ThetaXR_Acc = 360/(2*math.pi)*math.acos(xAccl/R)
		self.Pitch = ThetaXR_Acc - self.Pitch0

	def updateRoll(self):
		xAccl = self.getAcc_ax()
		yAccl = self.getAcc_ay()
		zAccl = self.getAcc_az()
		R = math.sqrt(xAccl*xAccl + yAccl*yAccl + zAccl*zAccl) + 0.000000001
		ThetaYR_Acc = 360/(2*math.pi)*math.acos(yAccl/R)
		self.Roll = - (ThetaYR_Acc + self.Roll0)

	def updateYaw(self):
		xAccl = self.getAcc_ax()
		yAccl = self.getAcc_ay()
		zAccl = self.getAcc_az()
		R = math.sqrt(xAccl*xAccl + yAccl*yAccl + zAccl*zAccl) + 0.000000001
		ThetaYR_Acc = 360/(2*math.pi)*math.acos(yAccl/R)
		self.Roll = - (ThetaYR_Acc + self.Roll0)

	def getRoll(self):
		return self.Roll

	def getYaw(self):
		return self.Yaw


	def getAcc_ax(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x28)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x29)
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536	
		return xAccl
	def getAcc_ay(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x2a)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x2b)
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536	
		return yAccl
	def getAcc_az(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x2c)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x2d)
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536	
		return zAccl

	def getGyro_gx(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x18)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x19)
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536	
		return xGyro
	def getGyro_gy(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x1a)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x1b)
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536	
		return yGyro
	def getGyro_gz(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x1c)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_ACC, 0x1d)
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536	
		return zGyro

	def getMagn_mx(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x28)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x29)
		xMag = data1 * 256 + data0
		if xMag > 32767 :
			xMag -= 65536	
		return xMag
	def getMagn_my(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x2a)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x2b)
		yMag = data1 * 256 + data0
		if yMag > 32767 :
			yMag -= 65536	
		return yMag				
	def getMagn_mz(self):
		data0 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x2c)
		data1 = self.I2C_CONN.read_byte_data(self.I2C_ADDR_MAG, 0x2d)
		zMag = data1 * 256 + data0
		if zMag > 32767 :
			zMag -= 65536	
		return zMag		




myimu = IMU('9DOF',1)
myimu.Init()
while True:
	myimu.updateRoll()
	print myimu.Roll
	time.sleep(0.01)
