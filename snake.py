import pygame


# While loop section
def main():
    """Start game."""
    global pygame

    screen = pygame.display.set_mode((800, 600))

    p1 = Snake((400, 300), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                p1.move[event.key]()

        pygame.display.update()


# Snake class section
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
        self.move = {
            up: self.up,
            down: self.down,
            left: self.left,
            right: self.right
        }

        self.xy = xy
        self.color = color

        self.body = [xy]


    def up(self):
        """Move up."""
        new_xy = (self.xy[0], self.xy[1] + 1)
        self.xy = new_xy
        self.body.append(new_xy)
        self.body.pop(0)
        print(self.body)

    def down(self):
        """Move down."""
        new_xy = (self.xy[0], self.xy[1] - 1)
        self.xy = new_xy
        self.body.append(new_xy)
        self.body.pop(0)
        print(self.body)

    def left(self):
        """Move left."""
        new_xy = (self.xy[0] - 1, self.xy[1])
        self.xy = new_xy
        self.body.append(new_xy)
        self.body.pop(0)
        print(self.body)

    def right(self):
        """Move right."""
        new_xy = (self.xy[0] + 1, self.xy[1])
        self.xy = new_xy
        self.body.append(new_xy)
        self.body.pop(0)
        print(self.body)



# Random generation section


if __name__ == '__main__':
    pygame.init()

    main()
