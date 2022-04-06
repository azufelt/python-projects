"""
Student: Ashley Zufelt
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random
from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

TEXT_COLOR =arcade.color.WHITE
ROCK_START_SPOT = SCREEN_WIDTH / 5
# SHIP_LIVES = 3
"""
Flying Object
    -Point
    -Velocity
    -Draw
    -Advance
    -Angle

Ship
Bullet

Small(Flying Object)
Medium(Flying Object)
Large(Flying Object)

"""


class Point:
      """Contains starting point"""
      def __init__(self):
        self.x = 0
        self.y = 0

class Velocity:
        """Contains information for velocity"""
        def __init__(self):
          self.dx = 0
          self.dy = 0

class Flying_Objects(ABC):
        """Flying objects holds parent data for all objects that fly... point, velocity, angle"""
        def __init__(self,img):
          self.center = Point()
          self.velocity = Velocity()
          self.alive = True
          self.img = img
          self.texture = arcade.load_texture(self.img)
          self.width = self.texture.width
          self.height = self.texture.height
          self.scale = 1
          self.radius = 0
          self.angle = 0
          self.speed = 0
          self.direction = 0
          self.alpha = 255
          self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
          self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed


        def advance(self):
          """
          Information to allow objects to move around within game window
          """
          #Move objects across window
          self.wrap() #every time we call advance we also call the wrap 
          self.center.x += self.velocity.dx
          self.center.y += self.velocity.dy

        def wrap(self):
            """
            Check all sides and if object passes edge, let it wrap to other side of screen
            """
            if self.center.x > SCREEN_WIDTH:
                self.center.x -= SCREEN_WIDTH
            if self.center.x < 0:
                self.center.x += SCREEN_WIDTH
            if self.center.y > SCREEN_HEIGHT:
                self.center.y -= SCREEN_HEIGHT
            if self.center.y < 0: 
                self.center.y += SCREEN_HEIGHT

        def draw(self):
            """
            Draw rect texture for all sprite images
            """
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.scale * self.height, self.texture, self.angle, self.alpha)


class Large(Flying_Objects):
        """
        Attributes for LARGE asteroid
        """
        def __init__(self):
          super().__init__('week9/asteroids/images/meteorGrey_big1.png')

          
          #lets asteroids start in various random spot, but stay on left edge of window
          self.center.y = random.randint(1, SCREEN_HEIGHT)
          self.center.x = random.randint(1, int(ROCK_START_SPOT)) 
          self.direction = random.randint(1, 50)
          self.radius = BIG_ROCK_RADIUS
          self.speed = BIG_ROCK_SPEED
          self.scale = 1
          self.angle += BIG_ROCK_SPIN
          self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
          self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed

        def advance(self):
            """
            Advance asteroid rocks
            """
            super().advance()
            self.angle += BIG_ROCK_SPIN

        def split(self, asteroids):
            """
            Large asteroid splits into two medium asteroids
            """
            med1 = Medium()
            med1.center.x = self.center.x
            med1.center.y = self.center.y
            med1.velocity.dy = self.velocity.dy + 2

            med2 = Medium()
            med2.center.x = self.center.x
            med2.center.y = self.center.y
            med2.velocity.dy = self.velocity.dy - 2

            small = Small()
            small.center.x = self.center.x
            small.center.y = self.center.y
            small.velocity.dy = self.velocity.dy + 5

            asteroids.append(med1)
            asteroids.append(med2)
            asteroids.append(small)
            self.alive = False

class Medium(Flying_Objects):
        """
        Attributes for MEDIUM asteroid
        """
        def __init__(self):
            super().__init__("week9/asteroids/images/meteorGrey_med1.png")
            self.radius = MEDIUM_ROCK_RADIUS

        def advance(self):
            super().advance()
            self.angle += MEDIUM_ROCK_SPIN

        def split(self, asteroids):
            """
            Medium asteroid splits into two SMALL asteroids and one MEDIUM
            """
            small = Small()
            small.center.x = self.center.x
            small.center.y = self.center.y
            small.velocity.dx = self.velocity.dx + 1.5
            small.velocity.dy = self.velocity.dy + 1.5

            small2 = Small()
            small2.center.x = self.center.x
            small2.center.y = self.center.y
            small2.velocity.dx = self.velocity.dx - 1.5
            small2.velocity.dy = self.velocity.dy - 1.5

            asteroids.append(small)
            asteroids.append(small2)
            self.alive - False

class Small(Flying_Objects):
        """
        Attributes for SMALL asteroid
        """
        def __init__(self):
            super().__init__("week9/asteroids/images/meteorGrey_small1.png")
            self.radius = SMALL_ROCK_RADIUS

        def advance(self):
            super().advance()
            self.angle += SMALL_ROCK_SPIN

        def split(self, asteroids):
            self.alive = False

class Ship(Flying_Objects):
        """
        Attributes to initialize a ship
        """
        def __init__(self):
            super().__init__('week9/asteroids/images/playerShip1_orange.png')

            self.angle = SHIP_TURN_AMOUNT
            self.center.x = (SCREEN_WIDTH/2)
            self.center.y = (SCREEN_HEIGHT/2)
            self.radius = SHIP_RADIUS
            self.scale = 1
            self.speed = SHIP_THRUST_AMOUNT
            # self.lives = SHIP_LIVES

        def left(self):
            self.angle +=SHIP_TURN_AMOUNT

        def right(self):
            self.angle -= SHIP_TURN_AMOUNT

        def thrust(self):
            self.velocity.dx -= math.sin(math.radians(self.angle)) * self.speed
            self.velocity.dy += math.cos(math.radians(self.angle)) * self.speed

        def reverse(self): 
            self.velocity.dx += math.sin(math.radians(self.angle)) * self.speed
            self.velocity.dy -= math.cos(math.radians(self.angle)) * self.speed
        
        def checkLives(self):
            self.lives -= 1
            print("lives left: {}".format(self.lives))

class Bullet(Flying_Objects):
        """
        Contains attributes to create bullets
        """
        def __init__(self, ship_angle, ship_x, ship_y):
            super().__init__('week9/asteroids/images/laserBlue01.png')

            self.radius = BULLET_RADIUS
            self.speed = BULLET_SPEED
            self.life = BULLET_LIFE
            self.angle = ship_angle -90
            self.center.x = ship_x
            self.center.y = ship_y
            self.scale = .5

        def fire(self):
            self.velocity.dx -= math.sin(math.radians(self.angle+90)) * self.speed
            self.velocity.dy += math.cos(math.radians(self.angle+90)) * self.speed

        def advance(self):
            super().advance()
            self.life -= 1
            if (self.life <= 0): 
               self.alive = False

class Message():
    def __init__(self):
        self.message = 'Game Over. Press Enter to play again?'

    def draw(self):
        arcade.draw_text(self.message, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2, arcade.color.BLACK, 20)

    def restart(self):
        print("in the restart function")
        self.game_over = False
        # Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        # arcade.run()
        Game(SCREEN_WIDTH, SCREEN_HEIGHT).__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)


        self.game_over = False
        self.held_keys = set()
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.message = Message()
        #keep running game until lose, then change to true
        self.game_over = False

        for i in range(INITIAL_ROCK_COUNT):
            largeAsteroid = Large()
            self.asteroids.append(largeAsteroid)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        for bullet in self.bullets:
            bullet.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        # only draw ship while alive, else remove ship from window
        if self.ship.alive:
            self.ship.draw()
        if not self.ship.alive:
            self.message.draw()

    def remove_deadObjects (self):
        """
        Clear bullets, asteroids and ship when dead
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
        if not self.ship.alive:
            # if ship is not alive remove bullets & asteroids from list
            for bullet in self.bullets:
                self.bullets = []
            for asteroid in self.asteroids:
                self.asteroids = []

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

         # for each bullet/target in the list, initiate them moving across screen
        for asteroid in self.asteroids:
            asteroid.advance()

        for bullet in self.bullets:
            bullet.advance()

        self.remove_deadObjects()
        self.check_collisions()

        self.ship.advance()

    def check_collisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    distance_x = abs(asteroid.center.x - bullet.center.x)
                    distance_y = abs(asteroid.center.y - bullet.center.y)
                    hit_distance = asteroid.radius + bullet.radius
                    if ((distance_x < hit_distance) and (distance_y < hit_distance)):
                        #if true then we have a collision
                        bullet.alive = False
                        asteroid.split(self.asteroids)
                        asteroid.alive = False
                        #could add score here:
                        # self.score += asteroid.hit()[1]

        for asteroid in self.asteroids:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and asteroid.alive:
                distance_x = abs(asteroid.center.x - self.ship.center.x)
                distance_y = abs(asteroid.center.y - self.ship.center.y)
                hit_distance = asteroid.radius + self.ship.radius
                if ((distance_x < hit_distance) and (distance_y < hit_distance)):
                        self.ship.alive = False
                        asteroid.alive = False

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            # print("left arrow")
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            # self.ship.thrust(self.ship.angle)
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            # self.ship.thrust(False)
            self.ship.reverse()

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
                # print("rapid fire")
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
        # Enter to restart game
        if arcade.key.ENTER in self.held_keys:
            self.end_game()

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # Fire the bullet here!
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
        #else if ship is dead, listen for RETURN key
        elif not self.ship.alive:
            if key == arcade.key.RETURN:
                self.end_game()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

    def end_game(self):
        """
        If ship is dead
        display win message
        restart game
        """
        self.message.restart()


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()