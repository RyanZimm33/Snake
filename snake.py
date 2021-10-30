import random
import pygame

screen_width = 800
screen_height = 600
cell_size = 50
# Number of seconds for a snake to cross the screen
speed = 2

blocks_x = screen_width // cell_size
blocks_y = screen_height // cell_size


def main():
    """Start game."""
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game_intro(screen)

    map = [[0 for x in range(blocks_x)] for y in range(blocks_y)]

    # Control keys in order of up, down, left, right
    p1controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    p2controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    p1 = Snake(7, 5, map, controls=p1controls, color=(1, 0, 0))
    p2 = Snake(1, 1, map, controls=p2controls, color=(0, 0, 1))
    pNPC = SnakeNPC(8, 8, map)
    players = [p1, p2, pNPC]

    Fruit(screen, map)

    try:
        while handle_events(players):
            clock.tick(blocks_x / speed)
            for p in players:
                if type(p) == SnakeNPC:
                    p.random_ch_dir()
                p.move(screen)
                p.draw(screen)

            show_score(10, 10, p1.score, screen)
            show_score(770, 10, p2.score, screen)

            pygame.display.update()
    except Exception as e:
        # When there is a snake collision, Exception('Game Over') is thrown.
        if str(e) == "Game Over":
            # end_screen will return True if user restarts.
            return end_screen(screen, p1, p2)

def handle_events(players):
    """Iterate through events and send them to their proper handlers.

    Parameters
    ----------
    players : list
        List of snake players.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            for p in players:
                try:
                    p.ch_dir[event.key]()
                except KeyError:
                    pass

    return True


def game_intro(screen):
    """Starting screen. Displays the game's name, controls, and anything else needed."""
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    myfont2 = pygame.font.SysFont("Britannic Bold", 30)

    title = myfont.render("Snake, but actually Tron", 1, (255, 0, 0))
    under = myfont2.render("Press Space to Begin", 1, (255, 0, 0))

    screen.blit(title, (30, 30))
    screen.blit(under, (30, 80))
    pygame.display.flip()

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    screen.fill((0, 0, 0))

def end_screen(screen, snake1, snake2):
    """Screen displayed upon Game Over. Displays winner, loser and the points scored. Returns True if user restarts."""
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    myfont2 = pygame.font.SysFont("Britannic Bold", 30)

    if snake1.loser and not snake2.loser:
        winner = myfont.render("Player 2 Wins!", 1, (255, 0,0))
    elif snake2.loser and not snake1.loser:
        winner = myfont.render("Player 1 Wins!", 1, (255, 0,0))
    else:
        winner = myfont.render("Tie", 1, (255, 0,0))

    scoreboard = myfont.render("Scoreboard", 1, (255, 0,0))
    underline  = myfont.render("__________", 1, (255,0,0))

    score1 = myfont2.render("Player 1: " + str(len(snake1.body)), 1, (255,0,0))
    score2 = myfont2.render("Player 2: " + str(len(snake2.body)), 1, (255,0,0))

    screen.blit(winner, (30, 30))
    screen.blit(scoreboard, (30, 60))
    screen.blit(underline, (30,80))
    screen.blit(score1, (30, 110))
    screen.blit(score2, (30, 140))
    pygame.display.flip()

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end = False
                elif event.key == pygame.K_ESCAPE:
                    end = False
                elif event.key == pygame.K_r:
                    return True

def show_score(x, y, score, screen):
    """Display score to the corners of the screen."""
    blocker = pygame.Rect(x, y, 60, 60)
    pygame.draw.rect(screen, (0, 0, 0), blocker)
    font = pygame.font.SysFont("Britannic Bold", 60)
    score_view = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_view, (x, y))


class Fruit:
    """Object to be eaten by snakes. Allows snakes to grow."""

    def __init__(self, screen, map):
        """Randomly place the fruit and update map to show it."""
        while True:
            self.x = random.randint(0, blocks_x - 1)
            self.y = random.randint(0, blocks_y - 1)
            if map[self.y][self.x] == 0:
                break

        map[self.y][self.x] = 2

        # Render the fruit
        x, y = index_to_pixels(self.x, self.y)

        # fruit = pygame.Rect(x, y, cell_size, cell_size)
        # pygame.draw.rect(screen, (255, 0, 0), fruit)

        white = (255,255,255)
        n = cell_size / 3
        pygame.draw.rect(screen, white, (x + n, y, n, n))
        pygame.draw.rect(screen, white, (x, y + n, n, n))
        pygame.draw.rect(screen, white, (x + 2*n, y + n, n, n))
        pygame.draw.rect(screen, white, (x + n, y + 2*n, n, n))

class Snake:
    """A snake. Moves forward every cycle and contains event handlers for turning."""

    def __init__(self, X, Y, map, *, controls=None, color=(255, 255, 255)):
        """Create a snake at x, y. Update the map to include it's position. Use controls and color if given.

        Parameters
        ----------
        X, Y : int
            The x and y index of the snake's head in the map.
        map : int matrix
            The map of the game containing values for current positions.
        controls : list
            The controls for each movement (in up, down, left, right order).
        color : tuple
            The rgb color of the snake. Default is white for debugging.
        """
        # handle_events will call the method that matches the event (control) key.
        try:
            self.ch_dir = {
                controls[0]: self.up,
                controls[1]: self.down,
                controls[2]: self.left,
                controls[3]: self.right
            }
        except TypeError:
            # No controls were given.
            self.ch_dir = dict()

        self.X = X
        self.Y = Y
        self.dX = 1
        self.dY = 0

        self.body = [(X, Y)]
        self.tail = (0, 0)

        map[Y][X] = 1
        self.map = map

        self.color = color
        self.growing = False
        self.already_turned = False
        self.loser = False
        self.score = 1

    def get_color(self):
        """Generate a color for the head by factoring in the x and y position."""
        x, y = index_to_pixels(self.X, self.Y)
        r = self.color[0] or 150 + 100 * (x / screen_width)
        g = self.color[1] or 100 + 150 * (y / screen_height)
        b = self.color[2] or 150 + 100 * (x / screen_width)
        return (int(r), int(g), int(b))


    def move(self, screen):
        """Move forward one cell. Check the map for collisions with snakes or fruits."""
        # The new coord modulo the max coord. This means the snake will wrap back to the beginning.
        new_X = (self.X + self.dX) % blocks_x
        new_Y = (self.Y + self.dY) % blocks_y

        obstacle = self.map[new_Y][new_X]
        self.collision_detect(obstacle, screen)

        self.X = new_X
        self.Y = new_Y
        self.body.append((self.X, self.Y))
        self.map[self.Y][self.X] = 1

        self.already_turned = False

        if self.growing:
            # Do NOT remove the tail
            self.growing = False
        else:
            # DO remove the tail
            self.tail = self.body.pop(0)
            self.map[self.tail[1]][self.tail[0]] = 0

    def draw(self, screen):
        """Render the snake by drawing a new body cell, and covering the last body cell."""
        head = self.body[-1]
        tail = self.tail

        black = (0, 0, 0)

        # Erase tail
        tail_coord = index_to_pixels(tail[0], tail[1])
        pygame.draw.rect(screen, black, (tail_coord[0], tail_coord[1], cell_size, cell_size))

        # Draw new head
        head_coord = index_to_pixels(head[0], head[1])
        # color = (100, 255 * (head_coord[0] / screen_width), 255 * (head_coord[1] / screen_height))
        color = self.get_color()
        pygame.draw.rect(screen, color, (head_coord[0], head_coord[1], cell_size-1, cell_size-1))

        pygame.display.update()

    def collision_detect(self, obstacle, screen):
        """Detect collisions. If apple, grow. If snake, raise Exception('Game Over')."""
        if obstacle == 1:
            self.loser = True
            raise Exception("Game Over")
        elif obstacle == 2:
            # Apple Collision
            Fruit(screen, self.map)
            self.growing = True
            self.score += 1


    def up(self):
        """Change direction to up."""
        if not self.already_turned:
            if not (self.dY == 1):
                self.dX, self.dY = 0, -1
                self.already_turned = True

    def down(self):
        """Change direction to down."""
        if not self.already_turned:
            if not (self.dY == -1):
                self.dX, self.dY = 0, 1
                self.already_turned = True

    def left(self):
        """Change direction to left."""
        if not self.already_turned:
            if not (self.dX == 1):
                self.dX, self.dY = -1, 0
                self.already_turned = True

    def right(self):
        """Change direction to right."""
        if not self.already_turned:
            if not (self.dX == -1):
                self.dX, self.dY = 1, 0
                self.already_turned = True

class SnakeNPC(Snake):
    """An snake with no controls and changes direction randomly."""

    def random_ch_dir(self):
        """Use a weighted probability to decide if the snake should turn."""
        # Percent chance of a turn
        turn_chance = 0.10

        n = random.random()

        # Of the 4 turns, only 2 will have an effect.
        if n < (turn_chance * (1/4)):
            self.up()
        elif n < (turn_chance * (1/2)):
            self.down()
        elif n < (turn_chance * (3/4)):
            self.left()
        elif n < turn_chance:
            self.right()

    def collision_detect(self, obstacle, screen):
        """Detect collisions. If apple, grow. If snake, raise Exception('Game Over')."""
        if obstacle == 1:
            # Destroy this snake
            print('NPC Snake loses.')
        elif obstacle == 2:
            # Apple Collision
            Fruit(screen, self.map)
            self.growing = True
            self.score += 1


def index_to_pixels(x, y):
    """Convert the index coordinates to pixel coordinates. Returns (x, y) in pixels."""
    new_x = x * cell_size
    new_y = y * cell_size
    return new_x, new_y


if __name__ == '__main__':
    if (screen_width % cell_size) or (screen_height % cell_size):
        raise Exception('screen_width and screen_height must be divisible by cell_size')

    pygame.init()
    pygame.display.set_caption("Tron Snake")
    icon = pygame.image.load("snake-2.png")
    pygame.display.set_icon(icon)

    # Loop allows restarting
    while main():
        pass
