# -------------------------- #
# - Class IMU File
# - Libreria de objeto de clase IMU
# -------------------------- #
import smbus
import time
import math
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
		self.Yaw0 = 0.0

		self.Pitch = 0.0
		self.Roll = 0.0
		self.Yaw = 0.0

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

		self.updateYaw()
		self.Yaw0 = self.Yaw
		
		

	def updatePitch(self):
		Pitchs = []
		for k in range(0,10):
			xAccl = self.getAcc_ax()
			yAccl = self.getAcc_ay()
			zAccl = self.getAcc_az()
			R = math.sqrt(xAccl*xAccl + yAccl*yAccl + zAccl*zAccl) + 0.000000001
			ThetaXR_Acc = 360/(2*math.pi)*math.acos(xAccl/R)
			Pitchs.append(ThetaXR_Acc - self.Pitch0)
		self.Pitch = sum(Pitchs)/len(Pitchs)

	def updateRoll(self):
		Rolls = []
		for k in range(0,10):
			xAccl = self.getAcc_ax()
			yAccl = self.getAcc_ay()
			zAccl = self.getAcc_az()
			R = math.sqrt(xAccl*xAccl + yAccl*yAccl + zAccl*zAccl) + 0.000000001
			ThetaYR_Acc = 360/(2*math.pi)*math.acos(yAccl/R)
			Rolls.append(-(ThetaYR_Acc + self.Roll0))
		self.Roll = sum(Rolls)/len(Rolls) 

	def updateYaw(self):
		Yaws = []
		for k in range(0,10):
			xMagn = self.getMagn_mx()
			yMagn = self.getMagn_my()
			zMagn = self.getMagn_mz()
			Roll = self.Roll
			Pitch = self.Pitch
			Bfy = zMagn*math.sin(Roll)  - yMagn*math.cos(Roll)
			Bfx = xMagn*math.cos(Pitch) + yMagn*math.sin(Pitch)*math.sin(Roll) + zMagn*math.sin(Pitch)*math.cos(Roll)
			Atan = 360*math.atan(-Bfy/Bfx)/(2*math.pi)
			yGyro = self.getGyro_gz()*(1.0/2000.0) 
			Yaws.append(yGyro  + self.Yaw)
		self.Yaw = sum(Yaws)/len(Yaws)



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
