#check the distance between each particle to see if they collide
def checkCollision (allParticles):

	for i in range(len(list(allParticles))):
		j = i + 1
		while j < len(list(allParticles)):
			ix = list(allParticles)[i].rect.center[0]
			iy = list(allParticles)[i].rect.center[1]
			jx = list(allParticles)[j].rect.center[0]
			jy = list(allParticles)[j].rect.center[1]
			if (ix-jx) == 0:
				phi = pi/2
			else:
				phi = atan((iy-jy)/(ix-jx))
#			print("phi = " + str(phi*180/pi))
			if sqrt((ix-jx)**2+(iy-jy)**2) < 30:
#			if abs(ix-jx) < 30 and abs(iy-jy) < 30:
				#prevent them from moving too close to each other
				if ix>jx:
					list(allParticles)[i].rect.move_ip(1,0)
					list(allParticles)[j].rect.move_ip(-1,0)
				else:
					list(allParticles)[i].rect.move_ip(-1,0)
					list(allParticles)[j].rect.move_ip(1,0)
				if iy>jy:
					list(allParticles)[i].rect.move_ip(0,1)
					list(allParticles)[j].rect.move_ip(0,-1)
				else:
					list(allParticles)[i].rect.move_ip(0,-1)
					list(allParticles)[j].rect.move_ip(0,1)
				#get the mass of each particle
				mi = list(allParticles)[i].m
				mj = list(allParticles)[j].m
				#get the velocity of each particle before collision
				vix = list(allParticles)[i].vx
				viy = list(allParticles)[i].vy
				vjx = list(allParticles)[j].vx
				vjy = list(allParticles)[j].vy
				vi = sqrt(vix**2 + viy**2)
				vj = sqrt(vjx**2 + vjy**2)
				if vix == 0:
					if viy < 0:
						viTheta = -pi/2
					else:
						viTheta = pi/2
				elif vix < 0:
					viTheta = pi+atan(viy/vix)
				else:
					viTheta = atan(viy/vix)

				if vjx == 0:
					if vjy < 0:
						vjTheta = -pi/2
					else:
						vjTheta = pi/2
				elif vjx < 0:
					vjTheta = pi+atan(vjy/vjx)
				else:
					vjTheta = atan(vjy/vjx)


				#2D collision equation
				viPerpendicular = (vi*(mi-mj)*cos(viTheta-phi)+2*mj*vj*cos(vjTheta-phi))/(mi+mj)
				viParallel = vi*sin(viTheta-phi)
				vjPerpendicular = (vj*(mj-mi)*cos(vjTheta-phi)+2*mi*vi*cos(viTheta-phi))/(mi+mj)
				vjParallel = vj*sin(vjTheta-phi)

				list(allParticles)[i].vx = viPerpendicular*cos(phi) - viParallel*sin(phi)
				list(allParticles)[i].vy = viPerpendicular*sin(phi) + viParallel*cos(phi)
				list(allParticles)[j].vx = vjPerpendicular*cos(phi) - vjParallel*sin(phi)
				list(allParticles)[j].vy = vjPerpendicular*sin(phi) + vjParallel*cos(phi)

#				#make red spread
#				if list(allParticles)[i].red or list(allParticles)[j].red:
#					list(allParticles)[i].red = True
#					list(allParticles)[j].red = True
#				sleep(0.1)
			j += 1

#get the total kinetic energy of all the particles
def getEnergy(allParticles,KE):
	KE = 0
	for i in range(len(list(allParticles))):
		KE = KE + sqrt(list(allParticles)[i].vx**2+list(allParticles)[i].vy**2)
#	print("energy: " + str(KE))

# Import pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
	RLEACCEL,
	KEYDOWN,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	K_n,
	QUIT)

#import random for random numbers
import random

#import trigonomic functions from math
from math import (sin, cos, atan, atan2, sqrt, pi, trunc)

#import ability to wait
from time import sleep

#initialize pygame
pygame.init()

#define a player object by extending pygame.sprites.Sprite
#the surface drawn on the screen is now an attribute of "player"
class Particle(pygame.sprite.Sprite):
	def __init__(self):
		super(Particle, self).__init__()
		self.surf = pygame.image.load("circle.png").convert()
		self.surf.set_colorkey((255,255,255),RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))
		)
		self.player = False
		self.red = False
		self.m = 1
		self.vx = 0
		self.vy = 0
	#method to define the reaction of the player to key strokes
	def update(self,pressed_keys):
		if self.player:
			#change the player's speed based on pressed keys
			if pressed_keys[K_LEFT]:
				self.vx -= 1
			if pressed_keys[K_RIGHT]:
				self.vx += 1
			if pressed_keys[K_UP]:
				self.vy -= 1
			if pressed_keys[K_DOWN]:
				self.vy += 1
#		if self.red:
#			self.surf.fill((255,0,255))
		#move based on velocity
		self.rect.move_ip(self.vx,self.vy)
		# reflect the particle once it hits a side
		if self.rect.left <= -1:
			self.rect.left = 0
			self.vx = -(self.vx)
		if self.rect.right >= SCREEN_WIDTH+1:
			self.rect.right = SCREEN_WIDTH
			self.vx = -(self.vx)
		if self.rect.top <= -1:
			self.rect.top = 0
			self.vy = -(self.vy)
		if self.rect.bottom >= SCREEN_HEIGHT+1:
			self.rect.bottom = SCREEN_HEIGHT
			self.vy = -(self.vy)

#set up clock to control framerate
clock = pygame.time.Clock()

#define screen constraints
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#create the screen object based off of the parameters defined
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#set the caption at the top of the window
pygame.display.set_caption("LITTLE PARTICLE")


#create a custom event for adding a new particle
ADDPARTICLE = pygame.USEREVENT + 1
#set it to occur 1 times per second?
#pygame.time.set_timer(ADDPARTICLE,1000)

#instantiate the player
player = Particle()
player.player = True
player.red = True
player.rect.center = (400,400)

#create groups to hold all the particles
allParticles = pygame.sprite.Group()
allParticles.add(player)

#variable to keep the main loop running
running = True

KE = 0


#main loop
while running:
	#look at every event in the queue
	for event in pygame.event.get():
		#press the x or hit escape to quit
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			running = False

		#add a new particle
		elif event.type == ADDPARTICLE or event.type == KEYDOWN and event.key == K_n:
			print("adding a particle")
			#create the new enemy and add it to the sprite groups
			newParticle = Particle()
			allParticles.add(newParticle)

	#get the set of keys pressed and check for user input
	pressed_keys = pygame.key.get_pressed()
	#check if any particles collide
	checkCollision(allParticles)

	getEnergy(allParticles,KE)

	#update each particle's movement each frame based off of colisions and keys pressed
	for entity in allParticles:
		entity.update(pressed_keys)

	#fill the scren
	screen.fill((0,0,0))
	#create a surface of defined width and height
	surf = pygame.Surface((10,10))
	#give the surface a color
	surf.fill((255,255,255))
	#what does this do?
	rect = surf.get_rect()

	for entity in allParticles:
			screen.blit(entity.surf,entity.rect)

	

#	if pygame.sprite.spritecollideany(player,allParticles):
#		player.kill()
#		running = False

	#refresh display to show updated screen
	pygame.display.flip()

	#ensure program maintains a rate of 30 frames per second
	clock.tick(20)




