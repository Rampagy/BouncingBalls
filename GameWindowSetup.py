import pygame
import random
import math

# create world parameters
gravity = (math.pi/2, 0.00007)
drag = 0.9999
number_of_particles = 10

# create window parameters
width, height = 1000, 800
background_color = (255, 255, 255)


def AddVectors(velocity1, velocity2):
    x = math.cos(velocity1[0])*velocity1[1] + math.cos(velocity2[0])*velocity2[1]
    y = math.sin(velocity1[0])*velocity1[1] + math.sin(velocity2[0])*velocity2[1]
    
    speed = math.hypot(x, y)
    angle = math.atan2(y, x)
    
    return (angle, speed)


def findParticle(particles, x, y):
    for particle in particles:
        if math.hypot(particle.x-x, particle.y-y) <= particle.size:
            return particle
    return None


def collide (p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy)
    if distance < p1.size + p2.size:
        angle = math.atan2(dy, dx) + math.pi/2
        total_mass = p1.mass + p2.mass
        
        (p1.angle, p1.speed) = AddVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p1.angle, p1.speed) = AddVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))

        overlap = 0.5*(p1.size + p2.size - distance + 1)
        p1.x += math.cos(angle)*overlap
        p1.y -= math.sin(angle)*overlap
        p2.x += math.cos(angle)*overlap
        p2.y -= math.sin(angle)*overlap


class Particle:
    def __init__(self, point, size):
        self.x = point[0]
        self.y = point[1]
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 3
        self.speed = random.uniform(0, 0.1)
        self.angle = random.uniform(0, 2*math.pi)
        self.mass = 2*math.pi * self.size**2

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        # compensate for world characterisitics
        (self.angle, self.speed) = AddVectors((self.angle, self.speed), gravity)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= drag
        
        # hit the right wall
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = math.pi-self.angle

        # hit the left wall
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = math.pi-self.angle

        # hit the bottom wall
        elif self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = -self.angle

        # hit the top wall
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = -self.angle


# create window for game
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Example Pygame')

# create screen objects
myParticles = []

for i in range(number_of_particles):
    size = random.randint(10, 20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)
    
    myParticles.append(Particle((x, y), size))

# run the game continuously
selected_particle = None
running = True
while running:
    # reset the screen (prevent smear)
    screen.fill(background_color)
    
    # watch for exit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = findParticle(myParticles, mouseX, mouseY)
            if selected_particle:
                selected_particle.color = (0, 255, 0)
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_particle:
                selected_particle.color = (0, 0, 255)
            selected_particle = None
            
    if selected_particle:
        mouseX, mouseY = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.01
    
    # display particles on screen
    for i, particle in enumerate(myParticles):
        particle.move()
        for particle2 in myParticles[i+1:]:
            collide(particle, particle2)
        particle.display()

    
    # update the screen
    pygame.display.flip()
















