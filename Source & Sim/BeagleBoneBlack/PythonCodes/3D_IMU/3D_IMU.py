# ----------------------------------------------------- # 
# --- Visualizacion 3D con OpenGL de la IMU DSLM091
# --- Author: Jorge Luis Mayorga Taborda
# --- Update: 22 Dec 2016
# ----------------------------------------------------- # 

 
# ----------------------------------------------------- # 
# --- Import Packages                              ---- #
# ----------------------------------------------------- # 
import httplib2
import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# ----------------------------------------------------- # 


# ----------------------------------------------------- # 
# --- Initial Settings & Figures                   ---- #
# ----------------------------------------------------- # 
vertices= (
    (0.5, -0.1, -1),
    (0.5, 0.1, -1),
    (-0.5, 0.1, -1),
    (-0.5, -0.1, -1),
    (0.5, -0.1, 1),
    (0.5, 0.1, 1),
    (-0.5, -0.1,1),
    (-0.5, 0.1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )
surfaces = (
  (0,1,2,3),
  (3,2,7,6),
  (6,7,5,4),
  (4,5,1,0),
  (1,5,7,2),
  (4,0,3,6),
 )
           
colors = (
    (1,1,1),
    (1,1,1),
    (1,1,1),
    (0,1,0),
    (0,1,0),
    (0,1,0),
    (0,0,1),
    (0,0,1),
    (0,0,1),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    )
# ----------------------------------------------------- # 



# ----------------------------------------------------- #
# --- Functions & Class Definitions                 --- #
# ----------------------------------------------------- #
def Cube():
	glBegin(GL_QUADS)
	for surface in surfaces:
		x = 0
		for vertex in surface:
			x+=1
			glColor3fv(colors[x])
			glVertex3fv(vertices[vertex])
	glEnd()

	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()


def main():
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

	glTranslatef(0.0,0.0, -5)

	OldPitch = 0.0
	OldRoll = 0.0 
	OldYaw = 0.0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		res,content = httplib2.Http().request("http://192.168.7.2:88/")

		DataList =  content.split(" ")

		Pitch = float(DataList[0])*(-1)
		Roll = float(DataList[1])*(1)
		Yaw = float(DataList[2])*(1)

		DeltaPitch = Pitch - OldPitch
		DeltaRoll = Roll - OldRoll
		DeltaYaw = Yaw - OldYaw

		OldPitch = Pitch
		OldRoll = Roll
		OldYaw = Yaw

		glRotate(DeltaRoll, 0,0,1)
		glRotate(DeltaYaw, 0,1,0)
		glRotate(DeltaPitch, 1,0,0)

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Cube()
		pygame.display.flip()
		pygame.time.wait(10)


main()
# ----------------------------------------------------- # 



'''
while True:
	res,content = httplib2.Http().request("http://192.168.7.2:88/")
	DataList =  content.split(" ")
	Pitch = float(DataList[0])
	Roll = float(DataList[1])
	Yaw = float(DataList[2])

	strPitch = str(Pitch)
	strRoll = str(Roll)
	strYaw = str(Yaw)

	print "Pitch : [" + strPitch +  "] " + "Roll: [" + strRoll + "] " + " Yaw : [" +  strYaw + "] " 
'''
