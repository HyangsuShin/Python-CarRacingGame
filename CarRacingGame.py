import pygame
import random


class Car(pygame.sprite.Sprite):
    """The class represents the oncoming cars"""
    def __init__(self, colour, width, height):
        """car constructor which we pass in the color, width and height"""
        # call parent constructor of Sprite class
        pygame.sprite.Sprite.__init__(self)
        # create an image of the block and set its color
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        # fetch the rectangle object of the image
        self.rect = self.image.get_rect()
        # create the random speed between 1-3
        self.speed = random.randrange(1, 3)
        # create the boolean for check the key press
        self.isPressed = False

    def reset_pos(self):
        """reset position to the top of the screen."""
        # reset position of car
        self.rect.y = random.randrange(-300, -20)
        # reset speed of car
        self.speed = random.randrange(1, 3)
        # reset color of car
        while True:
            for i in range(3):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                colour = [r, g, b]
            if colour != GRAY:
                self.image.fill(colour)
                break

    def update(self):
        """ Called each frame. """
        # Move block down one pixel
        self.rect.y += self.speed


class Player(Car):
    """ The player class derives from Car, but overrides the 'update'
    functionality with new a movement function that will move the Player
    with the keyboard. """
    def update(self):
        """Manipulate car movement"""
        # Check if the key is pressed, the player's position changes once
        if not self.isPressed:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.x += 100
                self.isPressed = True
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.rect.x -= 100
                self.isPressed = True
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.rect.y -= 100
                self.isPressed = True
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.rect.y += 100
                self.isPressed = True
        # Check if the key is up and make the keypress work again
        if event.type == pygame.KEYUP:
            if pygame.key.name(event.key) == "right" or pygame.key.name(event.key) == "left"\
                    or pygame.key.name(event.key) == "up" or pygame.key.name(event.key) == "down":
                self.isPressed = False
        # Set the player be in lane and screen
        if self.rect.x >= 470:
            self.rect.x = 370
        elif self.rect.x < 70:
            self.rect.x = 70
        elif self.rect.y > 520:
            self.rect.y = 520
        elif self.rect.y < 0:
            self.rect.y = 0


# initialize the game engine
pygame.init()

# define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (125, 125, 125)

# set size of screen (height & width)
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car racing game")

# create the group of cars
oncomingCars = pygame.sprite.Group()
allCars = pygame.sprite.Group()

# Declare score
score = 0

# Create oncoming cars
car1 = Car(RED, 50, 80)
car1.rect.x = 70
car1.rect.y = 0

car2 = Car(BLUE, 50, 80)
car2.rect.x = 170
car2.rect.y = 0

car3 = Car(GREEN, 50, 80)
car3.rect.x = 270
car3.rect.y = 0

car4 = Car(WHITE, 50, 80)
car4.rect.x = 370
car4.rect.y = 0

# add the oncoming cars to group
oncomingCars.add(car1)
allCars.add(car1)
oncomingCars.add(car2)
allCars.add(car2)
oncomingCars.add(car3)
allCars.add(car3)
oncomingCars.add(car4)
allCars.add(car4)

# Create a player
player = Player(RED, 50, 80)
player.rect.x = 270
player.rect.y = 520
allCars.add(player)

# Loop until the user clicks the close button
done = False
clock = pygame.time.Clock()

# create the sound for background
# music reference (https://pixabay.com/sound-effects/city-ambience-9271/)
pygame.mixer.music.load('city-ambience-9271.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

while not done:
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # User clicked X on window
            done = True                 # flag that we are done so we can exit

    # fill the background color
    screen.fill(GREEN)

    # list of the player collides with
    cars_hit_list = pygame.sprite.spritecollide(player, oncomingCars, False)

    # check the collision list
    for car in cars_hit_list:
        # reset the car position back to the top
        car.reset_pos()
        # play the collision sound
        click_sound = pygame.mixer.Sound('HornHonk.wav')
        click_sound.play()
        # update the score
        score -= 3

    # check the list of the on coming cars reaches the bottom safely with no collision
    for car in oncomingCars:
        # check the car reaches to the bottom safely
        if car.rect.y > 610:
            # reset the car position back to the top
            car.reset_pos()
            # update the score
            score += 1

    # update all the game objects
    allCars.update()

    # All drawing code here
    # roadway
    pygame.draw.rect(screen, GRAY, [50, 0, 400, 600], 0)
    pygame.draw.line(screen, WHITE, [150, 0], [150, 600], 5)
    pygame.draw.line(screen, WHITE, [250, 0], [250, 600], 5)
    pygame.draw.line(screen, WHITE, [350, 0], [350, 600], 5)
    # all cars
    allCars.draw(screen)

    # Declare the text font
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Indicate score by text
    text = font.render("Score: " + str(score), True, BLACK)
    # Put the image of the text on screen
    screen.blit(text, [500, 50])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
