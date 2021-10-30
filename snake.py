import random
import pygame


screen_width = 800
screen_height = 600
cell_size = 50

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

    p1 = Snake(7, 5, map, controls=p1controls, color=(0, 0, 255))
    p2 = Snake(1, 1, map, controls=p2controls, color=(0, 255, 0))
    players = [p1, p2]

    Fruit(screen, map)

    while handle_events(players):
        clock.tick(5)
        for p in players:
            p.move(screen)
            p.draw(screen)

        pygame.display.update()

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


class Fruit:
    """Object to be eaten by snakes. Allows snakes to grow."""

    def __init__(self, screen, map):
        """Randomly place the fruit and update map to show it."""
        self.x = random.randint(0, blocks_x - 1)
        self.y = random.randint(0, blocks_y - 1)
        map[self.y][self.x] = 2

        # Render the fruit
        x, y = index_to_pixels(self.x, self.y)
        fruit = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), fruit)

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
                controls[3]: self.right,
                pygame.K_g: self.grow    # Debug
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


    def move(self, screen):
        """Move forward one cell. Check the map for collisions with snakes or fruits."""
        # The new coord modulo the max coord. This means the snake will wrap back to the beginning.
        new_X = (self.X + self.dX) % blocks_x
        new_Y = (self.Y + self.dY) % blocks_y

        obstacle = self.map[new_Y][new_X]
        if obstacle == 1:
            # Snake Collision
            return None
        elif obstacle == 2:
            # Apple Collision
            Fruit(screen, self.map)
            self.growing = True

        self.X = new_X
        self.Y = new_Y
        self.body.append((self.X, self.Y))
        self.map[self.Y][self.X] = 1

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
        pygame.draw.rect(screen, self.color, (head_coord[0], head_coord[1], cell_size, cell_size))

        pygame.display.update()


    def up(self):
        """Change direction to up."""
        if not (self.dY == 1):
            self.dX, self.dY = 0, -1

    def down(self):
        """Change direction to down."""
        if not (self.dY == -1):
            self.dX, self.dY = 0, 1

    def left(self):
        """Change direction to left."""
        if not (self.dX == 1):
            self.dX, self.dY = -1, 0

    def right(self):
        """Change direction to right."""
        if not (self.dX == -1):
            self.dX, self.dY = 1, 0


def index_to_pixels(x, y):
    """Convert the index coordinates to pixel coordinates. Returns (x, y) in pixels."""
    new_x = x * cell_size
    new_y = y * cell_size
    return new_x, new_y


if __name__ == '__main__':
    if (screen_width % cell_size) or (screen_height % cell_size):
        raise Exception('screen_width and screen_height must be divisible by cell_size')

    pygame.init()

    main()
