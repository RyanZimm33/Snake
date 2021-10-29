import pygame


# While loop section
def main():
    """Start game."""
    global pygame

    screen = pygame.display.set_mode((800, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


# Snake class section


# Random generation section


if __name__ == '__main__':
    pygame.init()

    main()
