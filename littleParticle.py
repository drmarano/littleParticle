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
	K_b,
	K_n,
	K_m,
	QUIT)
#import random for random numbers
import random
#import trigonomic functions from math
from math import (sin, cos, atan, sqrt, pi)
#import ability to wait
from time import sleep

#initialize pygame
pygame.init()

def applyGravity(allParticles):
	for i in range(len(list(allParticles))):
		list(allParticles)[i].vy = list(allParticles)[i].vy + gravity


#check the distance between each particle to see if they collide
def checkInteraction(allParticles):
	for i in range(len(list(allParticles))):
		j = i + 1
		while j < len(list(allParticles)):
			ix = list(allParticles)[i].x
			iy = list(allParticles)[i].y
			jx = list(allParticles)[j].x
			jy = list(allParticles)[j].y
			ir = list(allParticles)[i].r
			jr = list(allParticles)[j].r
			#define angle between particles
			if (ix-jx) == 0: phi = pi/2
			else: phi = atan((iy-jy)/(ix-jx))
			#a collision occurs when particles get closer than 30 px away
			if sqrt((ix-jx)**2+(iy-jy)**2) <= (ir+jr/2):
				#prevent them from moving too close to each other
				if ix>jx:
					list(allParticles)[i].x = list(allParticles)[i].x + 1
					list(allParticles)[j].x = list(allParticles)[j].x - 1
				else:
					list(allParticles)[i].x = list(allParticles)[i].x - 1
					list(allParticles)[j].x = list(allParticles)[j].x + 1
				if iy>jy:
					list(allParticles)[i].y = list(allParticles)[i].y + 1
					list(allParticles)[j].y = list(allParticles)[j].y - 1
				else:
					list(allParticles)[i].y = list(allParticles)[i].y - 1
					list(allParticles)[j].y = list(allParticles)[j].y + 1
				#get the mass of each particle
				mi = list(allParticles)[i].m
				mj = list(allParticles)[j].m
				#get the velocity of each particle before collision
				vix = list(allParticles)[i].vx
				viy = list(allParticles)[i].vy
				vjx = list(allParticles)[j].vx
				vjy = list(allParticles)[j].vy
				#get the angle of each particle's velocity, atan only goes from -pi to pi so we need to adjust it
				if vix == 0:
					if viy < 0: viTheta = -pi/2
					else: viTheta = pi/2
				elif vix < 0: viTheta = pi+atan(viy/vix)
				else: viTheta = atan(viy/vix)
				if vjx == 0:
					if vjy < 0: vjTheta = -pi/2
					else: vjTheta = pi/2
				elif vjx < 0: vjTheta = pi+atan(vjy/vjx)
				else: vjTheta = atan(vjy/vjx)
				#get the speed of each particle
				vi = sqrt(vix**2 + viy**2)
				vj = sqrt(vjx**2 + vjy**2)
				#perform 2D collision equation
				viPerpendicular = (vi*(mi-mj)*cos(viTheta-phi)+2*mj*vj*cos(vjTheta-phi))/(mi+mj)
				viParallel = vi*sin(viTheta-phi)
				vjPerpendicular = (vj*(mj-mi)*cos(vjTheta-phi)+2*mi*vi*cos(viTheta-phi))/(mi+mj)
				vjParallel = vj*sin(vjTheta-phi)
				list(allParticles)[i].vx = (viPerpendicular*cos(phi) - viParallel*sin(phi)) * damping
				list(allParticles)[i].vy = (viPerpendicular*sin(phi) + viParallel*cos(phi)) * damping
				list(allParticles)[j].vx = (vjPerpendicular*cos(phi) - vjParallel*sin(phi)) * damping
				list(allParticles)[j].vy = (vjPerpendicular*sin(phi) + vjParallel*cos(phi)) * damping
			#perform electric force equation if neither of the charges are 0
			elif list(allParticles)[i].q != 0 and list(allParticles)[j].q != 0:
				ai = list(allParticles)[i].q*list(allParticles)[j].q/(list(allParticles)[i].m*((ix-jx)**2+(iy-jy)**2))
				aj = list(allParticles)[i].q*list(allParticles)[j].q/(list(allParticles)[j].m*((ix-jx)**2+(iy-jy)**2))
				#resolve direction of each acceleration
				if ix>jx:
					aix = ai*cos(phi)
					aiy = ai*sin(phi)
					ajx = -aj*cos(phi)
					ajy = -aj*sin(phi)
				else:
					aix = -ai*cos(phi)
					aiy = -ai*sin(phi)
					ajx = aj*cos(phi)
					ajy = aj*sin(phi)
				list(allParticles)[i].vx = list(allParticles)[i].vx + aix
				list(allParticles)[i].vy = list(allParticles)[i].vy + aiy
				list(allParticles)[j].vx = list(allParticles)[j].vx + ajx
				list(allParticles)[j].vy = list(allParticles)[j].vy + ajy
			j += 1

#get the total kinetic and potential energy of all the particles
def getEnergy(allParticles,KE,PE,E):
	KE = 0
	PE = 0
	E = 0
	for i in range(len(list(allParticles))):
		KE = KE + (list(allParticles)[i].m * (list(allParticles)[i].vx**2 + list(allParticles)[i].vy**2))/2
		PE = PE + list(allParticles)[i].m * gravity * (SCREEN_HEIGHT - list(allParticles)[i].y - list(allParticles)[i].r)
		E = KE + PE
	print(int(E))

#define a player object by extending pygame.sprites.Sprite
#the surface drawn on the screen is now an attribute of "player"
class Particle(pygame.sprite.Sprite):
	def __init__(self):
		super(Particle, self).__init__()
		#self.image = pygame.image.load("circleGreen.png").convert()
		#self.image.set_colorkey((0,0,0),RLEACCEL)
		#self.rect = self.image.get_rect(center=(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)))
		self.player = False
#		self.x = random.randint(0,SCREEN_WIDTH)
#		self.y = random.randint(0,SCREEN_HEIGHT)
		self.x = random.randint(SCREEN_WIDTH/2-SCREEN_WIDTH/10,SCREEN_WIDTH/2+SCREEN_WIDTH/10)
		self.y = random.randint(SCREEN_HEIGHT/2-SCREEN_HEIGHT/10,SCREEN_HEIGHT/2+SCREEN_HEIGHT/10)
		self.vx = 0
		self.vy = 0
		self.r = 10
		self.m = 1
		self.q = 0
		self.color = GREEN
	#define the reaction of the player to key strokes
	def update(self,pressed_keys):
		if self.player:
			#change the player's speed based on pressed keys
			if pressed_keys[K_LEFT]:
				self.vx -= .5
			if pressed_keys[K_RIGHT]:
				self.vx += .5
			if pressed_keys[K_UP]:
				self.vy -= .5
			if pressed_keys[K_DOWN]:
				self.vy += .5
#		if self.red:
#			self.surf.fill((255,0,255))
		#move based on velocity
#		self.rect.move_ip(self.vx,self.vy)
		self.x = self.x + self.vx
		self.y = self.y + self.vy
		# reflect the particle once it hits a side
		if self.x < self.r:
			self.x = self.r
			self.vx = -(self.vx)
		if self.x > SCREEN_WIDTH - self.r:
			self.x = SCREEN_WIDTH - self.r
			self.vx = -(self.vx)
		if self.y < self.r:
			self.y = self.r
			self.vy = -(self.vy)
		if self.y > SCREEN_HEIGHT - self.r:
			self.y = SCREEN_HEIGHT - self.r
			self.vy = -(self.vy)

#set the caption at the top of the window
pygame.display.set_caption("LITTLE PARTICLE")
#set up clock to control framerate
clock = pygame.time.Clock()
#define screen constraints
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#create the screen object based off of the parameters defined
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#define some useful colors
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,225,0)
BLUE=(0,0,225)
MAGENTA=(255,0,255)

#create a custom event for adding a new particle and set it to occur once a second
#ADDPARTICLE = pygame.USEREVENT + 1
#pygame.time.set_timer(ADDPARTICLE,1000)

#instantiate the player
player = Particle()
player.player = True
player.q = 10
player.color = RED

#create groups to hold all the particles
allParticles = pygame.sprite.Group()
allParticles.add(player)

#variable to keep the main loop running
running = True

#define other features
KE = 0
PE = 0
E = 0
gravity = 0
damping = 0.9

#main loop
while running:

	#Make the background of the screen black
	screen.fill(BLACK)

	#look at every event in the queue
	for event in pygame.event.get():
		#press the x or hit escape to quit
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			running = False

		#add a new particle
		elif event.type == KEYDOWN and event.key == K_n:
			print("adding a neutral particle")
			#create the new enemy and add it to the sprite groups
			newParticle = Particle()
			allParticles.add(newParticle)
		elif event.type == KEYDOWN and event.key == K_m:
			print("adding a positive particle")
			#create the new enemy and add it to the sprite groups
			newParticle = Particle()
			newParticle.q = 25
			newParticle.color = RED
			allParticles.add(newParticle)
		elif event.type == KEYDOWN and event.key == K_b:
			print("adding a positive particle")
			#create the new enemy and add it to the sprite groups
			newParticle = Particle()
			newParticle.q = -25
			newParticle.color = BLUE
			allParticles.add(newParticle)


	
	#get the set of keys pressed and check for user input
	pressed_keys = pygame.key.get_pressed()
	#apply gravity to each particle
#	applyGravity(allParticles)
	#apply electric force between each particle
#	applyElectricForce(allParticles)
	#check if any particles collide
	checkInteraction(allParticles)
	#measure the total kinetic energy
#	getEnergy(allParticles,KE,PE,E)

	#update each particle's movement each frame based off of colisions and keys pressed
	for item in allParticles:
		item.update(pressed_keys)

	#update the screen
	for item in allParticles:
#		screen.blit(item.image,item.rect)
		pygame.draw.circle(screen, item.color, (int(item.x), int(item.y)), int(item.r))

	#refresh display to show updated screen
	pygame.display.flip()

	#ensure program maintains a rate of 60 frames per second
	clock.tick(60)




