import pygame

screen_width = 800
screen_height = 600

# While loop section
def main():
    """Start game."""
    global pygame
    global screen_size

    screen = pygame.display.set_mode((screen_width, screen_height))

    p1 = Snake(100,100)

    running = True
    while running:
        #handle_events(pygame.event.get())


        p1.move()

        pygame.display.update()




# Snake class section
class Snake:
    """A snake with its own length and position."""

    def __init__(self, X, Y, color=(0, 0, 255)):
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
        self.ch_dir = {
            "k_UP": self.up,
            "k_DOWN": self.down,
            "k_LEFT": self.left,
            "k_RIGHT": self.right
        }

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

        # new_x = (self.xy[0] + self.velocity[0]) % screen_size[0]
        # new_y = (self.xy[1] + self.velocity[1]) % screen_size[1]

        self.body.append(self.X, self.Y)
        self.tail = self.body.pop(0)

        # Draw new rectangle at self.xy
        # Delete old rectangle at old_xy

        print(self.body)

    def draw(self):
        head = self.body[len(self.body)]
        tail = self.body[0]

        black = (0,0,0)
        white = (255,255,255)

        # erase tail
        pygame.draw.rect(screen, black, (tail[0], tail[1], 50, 50))
        # draw new head
        pygame.draw.rect(screen, white, (head[0], head[1], 50, 50))


    def up(self):
        """Move up."""
        self.dX, self.dY = 0, -1

    def down(self):
        """Move down."""
        self.dX, self.dY = 0, 1

    def left(self):
        """Move left."""
        self.dX, self.dY = -1, 0

    def right(self):
        """Move right."""
        self.dX, self.dY = 1, 0


# Random generation section


if __name__ == '__main__':
    pygame.init()

    main()
