"""
Student: Ashley Zufelt
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others

This program implements an awesome version of skeet.
"""
import arcade
import math
import random
from abc import ABC
from abc import abstractmethod

 

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 5
BULLET_COLOR = arcade.color.WHITE
BULLET_SPEED = 15

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SCORE = 1

STRONG_TARGET_RADIUS = 20
STRONG_TARGET_COLOR = arcade.color.RADICAL_RED
STRONG_TARGET_COLOR = arcade.color.RADICAL_RED
STRONG_TARGET_SCORE = 7

SAFE_TARGET_RADIUS = 15
SAFE_TARGET_COLOR = arcade.color.GREEN
SAFE_TARGET_SCORE = -10

TEXT_COLOR =arcade.color.WHITE

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
    def __init__(self):
      self.center = Point()
      self.velocity = Velocity()
      self.alive = True
      self.radius = 0

    @abstractmethod
    def draw(self):
        pass

    def advance(self):
      #Move objects across window
      self.center.x += self.velocity.dx
      self.center.y += self.velocity.dy

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
      #Check if flying object is on/off screen
      if(self.center.x > SCREEN_WIDTH or self.center.y > SCREEN_HEIGHT):
          return True
      else:
          return False

class Bullet(Flying_Objects):
    """
    Contains attributes to create bullets
    """
#     """Add to parent class -Flying_Objects as needed for specific bullet"""
    def __init__(self):
      super().__init__()
      self.radius = BULLET_RADIUS
      self.color = BULLET_COLOR

    def draw(self):
      #draw circle for bullets
      arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)

    def fire(self, angle):
      #use calculation to fire bullet, matching Rifle angle
      self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
      self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED 


class Target(Flying_Objects, ABC):
    """
     3 levels of target, standard, strong, safe
    """
    def __init__(self):
      super().__init__()
      self.center.y = random.uniform(SCREEN_HEIGHT/2, SCREEN_HEIGHT)
      self.velocity.dx = random.uniform(1,5)
      self.velocity.dy = random.uniform(-2,2)
      self.radius = TARGET_RADIUS
      self.color = TARGET_COLOR
      self.name = 'unknown'

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def hit(self):
        pass
 
class Standard(Target):
    """
    Contains attributes for the Standard target
    """
    def __init__(self):
      super().__init__()
      self.score = TARGET_SCORE
      self.name = 'standard'
      self.scale = .5

    def draw(self):
      # use arcade load texture to display custom sprite
      texture = arcade.load_texture("week7/skeet/meteor.png")
      arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture)
      # REPLACED standard circle with a sprite
      #  arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)

    def hit(self):
        self.alive = False
        return self.score


class Strong(Target):
    """
    Contains attributes for the Strong target
    first 2 hits give 1 point score
    final hit gives 5 additional points
    """
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,2)
        self.radius = STRONG_TARGET_RADIUS
        self.color = STRONG_TARGET_COLOR
        self.lives = 3
        self.score = STRONG_TARGET_SCORE
        self.scale = .8
        
    def draw(self):
    
      # use arcade load texture to display custom sprite
      texture = arcade.load_texture("week7/skeet/invader.png") 
      
      arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture)

      # REPLACED strong target with a sprite
      # arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, arcade.color.ORANGE_PEEL)
      #   text_x = self.center.x - (self.radius / 2)
      #   text_y = self.center.y - (self.radius / 2)
      #   arcade.draw_text(repr(self.lives), text_x, text_y, arcade.color.BLACK, font_size=40)

    def hit(self):
        self.lives -= 1
        if self.lives > 0:
            self.scale = .4
            return self.score
        else:
            self.score = 5
            self.alive = False
            self.scale = 0
            return self.score
            
class Boss(Target):
    """
    Contains attributes for a Boss target
    takes 4 hits to kill
    gives 20 points to score
    """
    def __init__(self):
        super().__init__()
        self.velocity.dx = 2
        self.velocity.dy = -1
        self.radius = STRONG_TARGET_RADIUS
        self.color = STRONG_TARGET_COLOR
        self.lives = 4
        self.score = STRONG_TARGET_SCORE
        self.scale = .8
        
    def draw(self):
        # use arcade load texture to display custom sprite
        texture = arcade.load_texture("week7/skeet/boss.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture)

    def hit(self):
        self.lives -= 1
        if self.lives > 0:
            self.scale -= .2
            return self.score
        else:
            self.score = 20
            self.alive = False
            self.scale = 0
            return self.score
            

class Safe(Target):
    """
    Contains attributes for the Safe target
    """
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,3)
        self.color = SAFE_TARGET_COLOR
        self.width = SAFE_TARGET_RADIUS
        self.height = SAFE_TARGET_RADIUS
        self.name = 'safe'

    def draw(self):
      # use arcade load texture to display custom sprite
      texture = arcade.load_texture("week7/skeet/satellite.png")
      scale = .7
      arcade.draw_texture_rectangle(self.center.x, self.center.y, scale * texture.width, scale * texture.height, texture)

      #REPLACED safe target with sprite
      # arcade.draw_rectangle_filled(self.center.x, self.center.y, self.width, self.height, self.color)

    def hit(self):
        self.score = SAFE_TARGET_SCORE
        self.alive = False
        return self.score

class Rifle:
    """
    Defines attributes needed for the rifle
    """
    def __init__(self):
        self.center = Point()
        self.angle = 45

    def draw(self):
      # use arcade load texture to display custom sprite
      texture = arcade.load_texture("week7/skeet/rocket.png")
      scale = 1.5
      arcade.draw_texture_rectangle(self.center.x, self.center.y, scale * texture.width, scale * texture.height, texture, self.angle - 90)

      #REPLACED rifle with sprite
      # arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360-self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []
        self.targets = []
        #keep running game until lose, then change to true
        self.game_over = False

        # Background image stored here
        self.background = None

        arcade.set_background_color(arcade.color.WHITE)
        self.setup()
       

    def setup(self):
        """Background image"""
        self.background = arcade.load_texture('week7/skeet/space-sky.jpg')

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        
        # clear the screen to begin drawing
        arcade.start_render()
        #draw size of background image
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()
        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=TEXT_COLOR)
        
        if self.score >= 10: 
            self.end_game()


    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        # get a random number between 1 and 50, and check if value is 1
        # if value is 1, then create a target
        if random.randint(1, 50) == 1:
            self.create_target()

        # for each bullet/target in the list, initiate them moving across screen
        for bullet in self.bullets:
            bullet.advance()
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        # get a set of random numbers, and assign each number to a type of target
        # check random number to see what type target and then add it to list of targets
        # after specific score add a Boss target to the list of targets
        
        if random.randint(1, 6) == 1 or random.randint(1, 6) == 2 or random.randint(1, 6) == 3:
            target = Standard()
            self.targets.append(target)
        if random.randint(1, 6) == 4 or random.randint(1, 6) == 5:
            target = Strong()
            self.targets.append(target)
        if random.randint(1, 6) == 6 :
            target = Safe()
            self.targets.append(target)
        if self.score > 15:
          if random.randint(1, 5) == 1:
              target = Boss()
              self.targets.append(target)

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.

        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def end_game(self):
        """
        Checks the score to see if player has won
        stop all flying objects
        display win message
        """
        if self.score >= 100:
            
            arcade.draw_text("You Won!",
                         SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, TEXT_COLOR, 40)
            for bullet in self.bullets:
                self.bullets = []
            for target in self.targets:
                self.targets=[]
            self.game_over = True

        if self.score <= -30:
            arcade.draw_text("You Lost.",
                         SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, TEXT_COLOR, 40)
            for bullet in self.bullets:
                self.bullets = []
            for target in self.targets:
                self.targets = []
            self.game_over = True

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
