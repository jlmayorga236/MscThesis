# ---------------------------------------------------- # 
# ------- LSM9DS1 Sparkfun IMU 9DOF I2C -------------- #
# ------- A Python Script for Debian    -------------- #
# ------- on BeagleBone Black           -------------- #
# ---------------------------------------------------- #
# ------- Author: Jorge Luis Mayorga    -------------- #
# ------- Update: 17/12/16              -------------- #
# ---------------------------------------------------- #

# ---------------------------------------------------- #
# ---- Import Packages (smbus is the most important)
# ---------------------------------------------------- #
import time
import math
import IMU
# ---------------------------------------------------- #


# ---------------------------------------------------- #
# ---- Variables & Constants 
# ---------------------------------------------------- #

# ---------------------------------------------------- #


# ---------------------------------------------------- #
# ---- Init IMU Object 
# ---------------------------------------------------- #
SparkFunIMU = IMU.IMU('9DOF',1)
SparkFunIMU.Init()
# ---------------------------------------------------- #



# ---------------------------------------------------- #
# ---- Data Adquisition Loop 
# ---------------------------------------------------- #
StopFlag = True
while StopFlag:

	SparkFunIMU.updatePitch()
	SparkFunIMU.updateRoll()
	SparkFunIMU.updateYaw()

	strPitch = str(SparkFunIMU.Pitch)
	strRoll = str(SparkFunIMU.Roll)
	strYaw = str(SparkFunIMU.Yaw - SparkFunIMU.Yaw0)

	print "Pitch : [" + strPitch +  "] " + "Roll: [" + strRoll + "] " + " Yaw : [" +  strYaw + "] "
	time.sleep(0.05)
