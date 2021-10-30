import pygame, random


screen_width = 800
screen_height = 600

cell_height_count = 12
cell_width_count = 16
cell_size = 50
clock = pygame.time.Clock()

cell_size = 50



def main():
    """Start game."""

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    blocks_x = screen_width // cell_size
    blocks_y = screen_height // cell_size
    map = [[0 for x in range(blocks_x)] for y in range(blocks_y)]

    # Up, down, left, right
    p1controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    p2controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    p1 = Snake(400, 300, controls=p1controls, color=(0, 0, 255))
    p2 = Snake(100, 100, controls=p2controls, color=(0, 255, 0))
    players = [p1, p2]
    fruit = Fruit()

    game_intro(screen)

    while handle_events(players):
        clock.tick(5)
        for p in players:
            p.move()
            p.draw(screen)

        fruit.drawFruit(screen)
        if(fruit.collision(p1.getX(), p1.getY())):
            p1.grow()
        if(fruit.collision(p2.getX(), p2.getY())):
            p2.grow()
        pygame.display.update()

def game_intro(screen):
    intro =True
    while (intro):
        myfont = pygame.font.SysFont("Britannic Bold", 40)
        myfont2 = pygame.font.SysFont("Britannic Bold", 30)
        title = myfont.render("Snake, but actually Tron", 1, (255, 0, 0))
        under = myfont2.render("Press Space to Begin", 1, (255, 0, 0))
        screen.blit(title,(30, 30))
        screen.blit(under,(30, 80))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    screen.fill((0,0,0))

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

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_width_count - 1)
        self.y = random.randint(0, cell_height_count - 1)

    def drawFruit(self, screen):
        fruit = pygame.Rect(self.x * cell_size, self.y * cell_size, 50, 50)
        pygame.draw.rect(screen ,(255, 0, 0), fruit)

    def collision(self, xPos, yPos):
        if self.x * cell_size == int(xPos) and self.y * cell_size == int(yPos):
            self.x = random.randint(0, cell_width_count - 1)
            self.y = random.randint(0, cell_height_count - 1)
            return True
        else:
            return False



class Snake:
    """A snake with its own length and position."""

    def __init__(self, X, Y, *, controls=None, color=(255, 255, 255)):
        """Create snake.

        Parameters
        ----------
        xy : [int, int]
            The xy coordinate of the head.
        up, down, left, right : pygame.event.key
            The controls for each movement.
        color : (int, int, int)
            The rgb color of the snake.
        """
        try:
            self.ch_dir = {
                controls[0]: self.up,
                controls[1]: self.down,
                controls[2]: self.left,
                controls[3]: self.right,
                pygame.K_g: self.grow
            }
        except TypeError:
            self.ch_dir = dict()

        self.X = X
        self.Y = Y
        self.dX = 1
        self.dY = 0
        self.tail = (0,0)
        self.color = color
        self.growing = False

        self.body = [(X, Y)]

    def grow(self):
        self.growing = True

    def move(self):
        """Move one position."""

        self.X = (self.X + self.dX * cell_size) % screen_width
        self.Y = (self.Y + self.dY * cell_size) % screen_height

        self.body.append((self.X, self.Y))

        if not (self.growing):
            self.tail = self.body.pop(0)
        else:
            self.growing = False


    def draw(self, screen):
        head = self.body[-1]
        tail = self.tail

        black = (0,0,0)

        # erase tail
        pygame.draw.rect(screen, black, (tail[0], tail[1], cell_size, cell_size))
        # draw new head
        pygame.draw.rect(screen, self.color, (head[0], head[1], cell_size-1, cell_size-1))
        # render
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

    def getX(self):
        return self.X

    def getY(self):
        return self.Y


# Random generation section


if __name__ == '__main__':
    if (screen_width % cell_size) or (screen_height % cell_size):
        raise Exception('screen_width and screen_height must be divisible by cell_size')

    pygame.init()

    main()
