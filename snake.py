import pygame


screen_size = (800, 600)


def main():
    """Start game."""
    global pygame
    global screen_size

    screen = pygame.display.set_mode(screen_size)

    p1 = Snake((400, 300), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    players = [p1]

    while handle_events(players):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                p1.ch_dir[event.key]()

        p1.move()

        pygame.display.update()

def handle_events(players):
    """Iterate through events and send them to their proper handlers.

    Parameters
    ----------
    players : list
        List of snake players.
    """
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            for p in players:
                try:
                    p.ch_dir[event.key]()
                except KeyError:
                    pass

    return running


class Snake:
    """A snake with its own length and position."""

    def __init__(self, xy, up, down, left, right, color=(0, 0, 255)):
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
            up: self.up,
            down: self.down,
            left: self.left,
            right: self.right
        }

        self.xy = xy
        self.velocity = (1, 0)
        self.color = color

        self.body = [xy]


    def move(self):
        """Move one position."""
        global screen_size

        new_x = (self.xy[0] + self.velocity[0]) % screen_size[0]
        new_y = (self.xy[1] + self.velocity[1]) % screen_size[1]

        self.xy = (new_x, new_y)
        self.body.append(self.xy)
        old_xy = self.body.pop(0)

        # Draw new rectangle at self.xy
        # Delete old rectangle at old_xy

        print(self.body)


    def up(self):
        """Move up."""
        self.velocity = (0, 1)

    def down(self):
        """Move down."""
        self.velocity = (0, -1)

    def left(self):
        """Move left."""
        self.velocity = (-1, 0)

    def right(self):
        """Move right."""
        self.velocity = (1, 0)


# Random generation section


if __name__ == '__main__':
    pygame.init()

    main()
