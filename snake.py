import pygame

screen_width = 800
screen_height = 600
clock = pygame.time.Clock()

def main():
    """Start game."""
    global pygame

    screen = pygame.display.set_mode((screen_width, screen_height))

    # Up, down, left, right
    p1controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    p2controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    p1 = Snake(400, 300, controls=p1controls, color=(0, 0, 255))
    p2 = Snake(100, 100, controls=p2controls, color=(0, 255, 0))
    players = [p1, p2]

    while handle_events(players):
        clock.tick(5)
        for p in players:
            p.move()
            p.draw(screen)

        pygame.display.update()
        
def game_intro(screen):
    intro =True
    while (intro):
        myfont = pygame.font.SysFont("Britannic Bold", 40)
        nlabel = myfont.render("Welcome ", 1, (255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
        screen.blit(nlabel,(200,200))
        pygame.display.flip()       

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
            for p in players:
                try:
                    p.ch_dir[event.key]()
                except KeyError:
                    pass

    return True


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
                controls[3]: self.right
            }
        except TypeError:
            self.ch_dir = dict()

        self.X = X
        self.Y = Y
        self.dX = 1
        self.dY = 0
        self.tail = (0,0)
        self.color = color

        self.body = [(X, Y)]


    def move(self):
        """Move one position."""
        global screen_size

        self.X = (self.X + self.dX * 50) % screen_width
        self.Y = (self.Y + self.dY * 50) % screen_height

        self.body.append((self.X, self.Y))
        self.tail = self.body.pop(0)

    def draw(self, screen):
        head = self.body[-1]
        tail = self.tail

        black = (0,0,0)

        # erase tail
        pygame.draw.rect(screen, black, (tail[0], tail[1], 50, 50))
        # draw new head
        pygame.draw.rect(screen, self.color, (head[0], head[1], 50, 50))


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


# Random generation section


if __name__ == '__main__':
    pygame.init()

    main()
