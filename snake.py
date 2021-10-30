import random
import pygame

import constants


def main():
    """START GAME"""
    screen = pygame.display.set_mode((constants.screen_width, constants.screen_height))
    clock = pygame.time.Clock()

    try:
        settings = game_intro(screen)
        stats = game_loop(screen, clock, settings)
        return end_screen(screen, stats)
    except Exception as e:
        if str(e) == 'QUIT':
            return False
        else:
            raise e


def game_loop(screen, clock, settings):
        players, map, controllers = game_setup(settings)

        Fruit(screen, map)

        try:
            while True:
                clock.tick(constants.blocks_x / constants.speed)

                for cont in controllers:
                    cont.post_events(map)

                if not handle_events(players):
                    return []

                for player in players:
                    player.move(screen)
                    show_score(player.score_coords, player.score, screen)
                    player.draw(screen)

                #show_score(10, 10, p1.score, screen)
                #show_score(770, 10, p2.score, screen)

                pygame.display.update()

        except Exception as e:
                # When there is a snake collision, Exception('Game Over') is thrown.
            if str(e) == "Game Over":
                    # end_screen will return True if user restarts.
                return players
            else:
                raise e

        # need players, fruit

def game_setup(settings):

    Game_Mode = settings['Gamemode']
    difficulty = settings['Difficulty']
    constants.cell_size = 40
    constants.blocks_x = int(constants.screen_width / constants.cell_size)
    constants.blocks_y = int(constants.screen_height / constants.cell_size)

    map = Map(constants.blocks_x, constants.blocks_y)
    p1controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    p2controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    controllers = []

    if (Game_Mode == 0):
        player = Snake(7, 5, map, controls=p1controls, color=(1, 0, 0), score_coords=(10,10))
        players = [player]
    elif (Game_Mode == 1):
        player1 = Snake(7, 5, map, controls=p1controls, color=(1, 0, 0), score_coords=(10,10))
        player2 = Snake(1, 1, map, controls=p2controls, color=(0, 0, 1), score_coords=(770,10))
        players = [player1, player2]
    elif (Game_Mode == 2):
        player = Snake(7, 5, map, controls=p1controls, color=(1, 0, 0), score_coords=(10,10))

        npc1cont = EasyNPC(len(controllers))    # add easy, medium, hard
        controllers.append(npc1cont)
        playerNPC = npc1cont.bind_snake(8, 8, map)

        players = [player, playerNPC]

    return (players, map, controllers)


def handle_events(players):
    """Iterate through events and send them to their proper handlers.

    Parameters
    ----------
    players : list
        List of snake players.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception('QUIT')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise Exception('QUIT')
            for p in players:
                try:
                    p.ch_dir[event.key]()
                except KeyError:
                    pass
        elif event.type == NPCController.VIRT_EVENT:
            for p in players:
                try:
                    p.ch_dir[(event.n, event.dir)]()
                except KeyError:
                    pass

    return True

def game_intro(screen):
    """Starting screen. Displays the game's name, controls, and anything else needed."""
    settings = {"Gamemode": 0, "Difficulty": 0}
    big = pygame.font.SysFont("Britannic Bold", 40)
    small = pygame.font.SysFont("Britannic Bold", 30)

    title = big.render("Snake, but actually Tron", 1, (255, 0, 0))

    intro = True
    while intro:
        #Draws buttons, color changes if mouse is hovering over
        mouse = pygame.mouse.get_pos()
        if 30 <= mouse[0] <= 100 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(30, 90 , 70, 40))
            startT = small.render("Start", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(30, 90 , 70, 40))
            startT = small.render("Start", 1, (255, 0, 0))

        if 120 <= mouse[0] <= 220 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(120, 90 , 100, 40))
            settingsT = small.render("Options", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(120, 90 , 100, 40))
            settingsT = small.render("Options", 1, (255, 0, 0))

        if 240 <= mouse[0] <= 300 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(240, 90 , 60, 40))
            exitT = small.render("Exit", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(240, 90 , 60, 40))
            exitT = small.render("Exit", 1, (255, 0, 0))

        screen.blit(title, (30, 30))
        screen.blit(startT, (40, 100))
        screen.blit(settingsT, (130, 100))
        screen.blit(exitT, (250, 100))

        #Button events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception('QUIT')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Start
                if 30 <= mouse[0] <= 90 and 90 <= mouse[1] <= 130:
                    intro = False
                    screen.fill((0, 0, 0))
                    return settings
                #Options
                if 120 <= mouse[0] <= 220 and 90 <= mouse[1] <= 130:
                    settings = optionScreen(screen)
                #Exit
                if 240 <= mouse[0] <= 300 and 90 <= mouse[1] <= 130:
                    raise Exception('QUIT')

        pygame.display.update()

def optionScreen(screen):
    settings = {"Gamemode": 0, "Difficulty": 0}
    screen.fill((0, 0, 0))

    big = pygame.font.SysFont("Britannic Bold", 40)
    small = pygame.font.SysFont("Britannic Bold", 30)

    optionT = big.render("Options", 1, (255, 0, 0))
    diffSelction = small.render("Difficulty: Easy" , 1, (255,0,0))
    gameSelction = small.render("Gamemode: Snake" , 1, (255,0,0))


    while True:
        screen.fill((0,0,0))
        #Draws buttons, color changes if mouse is hovering over
        mouse = pygame.mouse.get_pos()
        if 30 <= mouse[0] <= 100 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(30, 90 , 70, 40))
            diff1 = small.render("Easy", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(30, 90 , 70, 40))
            diff1 = small.render("Easy", 1, (255, 0, 0))

        if 120 <= mouse[0] <= 220 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(120, 90 , 100, 40))
            diff2 = small.render("Medium", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(120, 90 , 100, 40))
            diff2 = small.render("Medium", 1, (255, 0, 0))

        if 240 <= mouse[0] <= 300 and 90 <= mouse[1] <= 130:
            pygame.draw.rect(screen,(255,0,0),(240, 90 , 60, 40))
            diff3 = small.render("Hard", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(240, 90 , 60, 40))
            diff3 = small.render("Hard", 1, (255, 0, 0))

        if 30 <= mouse[0] <= 100 and 150 <= mouse[1] <= 190:
            pygame.draw.rect(screen,(255,0,0),(30, 150 , 70, 40))
            game1 = small.render("Snake", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(30, 150 , 70, 40))
            game1 = small.render("Snake", 1, (255, 0, 0))

        if 120 <= mouse[0] <= 220 and 150 <= mouse[1] <= 190:
            pygame.draw.rect(screen,(255,0,0),(120, 150 , 100, 40))
            game2 = small.render("Multi", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(120, 150 , 100, 40))
            game2 = small.render("Multi", 1, (255, 0, 0))

        if 240 <= mouse[0] <= 300 and 150 <= mouse[1] <= 190:
            pygame.draw.rect(screen,(255,0,0),(240, 150 , 60, 40))
            game3 = small.render("CPU", 1, (255, 255, 255))
        else:
            pygame.draw.rect(screen,(255,255,255),(240, 150 , 60, 40))
            game3 = small.render("CPU", 1, (255, 0, 0))

        if 30 <= mouse[0] <= 100 and 250 <= mouse[1] <= 290:
            pygame.draw.rect(screen,(255,0,0),(30, 250 , 70, 40))
            exitT = small.render("Exit", 1, (255,255,255))
        else:
            pygame.draw.rect(screen,(255,255,255),(30, 250 , 70, 40))
            exitT = small.render("Exit", 1, (255,0,0))


        screen.blit(optionT, (30, 30))
        screen.blit(diff1, (40, 100))
        screen.blit(diff2, (130, 100))
        screen.blit(diff3, (250, 100))
        screen.blit(game1, (40, 160))
        screen.blit(game2, (130, 160))
        screen.blit(game3, (250, 160))
        screen.blit(diffSelction, (320, 100))
        screen.blit(gameSelction, (320, 160))
        screen.blit(exitT, (40, 260))

        #Button events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception('QUIT')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.fill((0,0,0))
                    return settings
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Easy
                if 30 <= mouse[0] <= 90 and 90 <= mouse[1] <= 130:
                    settings["Difficulty"] = 0
                    diffSelction = small.render(("Difficulty: Easy" ), 1, (255,0,0))
                #Medium
                if 120 <= mouse[0] <= 220 and 90 <= mouse[1] <= 130:
                    settings["Difficulty"] = 1
                    diffSelction = small.render(("Difficulty: Medium" ), 1, (255,0,0))
                #Hard
                if 240 <= mouse[0] <= 300 and 90 <= mouse[1] <= 130:
                    settings["Difficulty"] = 2
                    diffSelction = small.render(("Difficulty: Hard" ), 1, (255,0,0))

                #Snake gamemode
                if 30 <= mouse[0] <= 90 and 150 <= mouse[1] <= 190:
                    settings["Gamemode"] = 0
                    gameSelction = small.render(("Gamemode: Snake" ), 1, (255,0,0))
                #Tron/Multiplayer gamemode
                if 120 <= mouse[0] <= 220 and 150 <= mouse[1] <= 190:
                    settings["Gamemode"] = 1
                    gameSelction = small.render(("Gamemode: Multi" ), 1, (255,0,0))
                #CPU gamemode
                if 240 <= mouse[0] <= 300 and 150 <= mouse[1] <= 190:
                    settings["Gamemode"] = 2
                    gameSelction = small.render(("Gamemode: CPU" ), 1, (255,0,0))
                #Exit button
                if 30 <= mouse[0] <= 100 and 250 <= mouse[1] <= 290:
                    screen.fill((0,0,0))
                    return settings

        pygame.display.update()

def end_screen(screen, snakes):
    """Screen displayed upon Game Over. Displays winner, loser and the points scored. Returns True if user restarts."""
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    myfont2 = pygame.font.SysFont("Britannic Bold", 30)

    scoreboard = myfont.render("Scoreboard", 1, (255, 0,0))
    underline  = myfont.render("__________", 1, (255,0,0))

    try:
        snake1 = snakes[0]
        score1 = myfont2.render(f"Player 1: {str(len(snake1.body))}", 1, (255, 0, 0))
        screen.blit(score1, (30, 110))
    except IndexError:
        pass

    try:
        snake2 = snakes[1]
        score2 = myfont2.render(f"Player 1: {str(len(snake2.body))}", 1, (255,0,0))
        screen.blit(score2, (30, 110))
    except IndexError:
        pass

    if len(snakes) == 2:
        if snake1.loser and not snake2.loser:
            winner = myfont.render("Player 2 Wins!", 1, (255, 0, 0))
        elif snake2.loser and not snake1.loser:
            winner = myfont.render("Player 1 Wins!", 1, (255, 0, 0))
        else:
            winner = myfont.render("Tie", 1, (255, 0, 0))

        screen.blit(winner, (30, 30))

    screen.blit(scoreboard, (30, 60))
    screen.blit(underline, (30,80))
    pygame.display.flip()

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = False
                    return False
                else:
                    end = False
    # Automatically restart
    return True

def show_score(score_coords, score, screen):
    x, y = score_coords
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
        self.map = map
        self.screen = screen

        self.map.fruits.append(self)

        while True:
            self.x = random.randint(0, constants.blocks_x - 1)
            self.y = random.randint(0, constants.blocks_y - 1)
            if map[self.y][self.x] == 0:
                break

        map[self.y][self.x] = self

        # Render the fruit
        x, y = index_to_pixels(self.x, self.y)

        # fruit = pygame.Rect(x, y, constants.cell_size, constants.cell_size)
        # pygame.draw.rect(screen, (255, 0, 0), fruit)

        white = (255,255,255)
        n = constants.cell_size / 3
        pygame.draw.rect(screen, white, (x + n, y, n, n))
        pygame.draw.rect(screen, white, (x, y + n, n, n))
        pygame.draw.rect(screen, white, (x + 2*n, y + n, n, n))
        pygame.draw.rect(screen, white, (x + n, y + 2*n, n, n))

    def eat(self):
        """This fruit has been destroyed. Create a new Fruit."""
        self.map.fruits.remove(self)
        Fruit(self.screen, self.map)

class BigFruit(Fruit):
    """A bigger fruit that is easier to hit."""
    size = 3

    def __init__(self, screen, map):
        """Randomly place the fruit and update map to show it."""
        self.map = map
        self.screen = screen

        while True:
            try_again = False
            self.x = random.randint(0, constants.blocks_x - 1)
            self.y = random.randint(0, constants.blocks_y - 1)

            # Check those new positions
            for point in self.get_points():
                if map[point[1]][point[0]] != 0:
                    try_again = True
                    break
                elif point[0] // (constants.blocks_x-1):
                    # Goes over vertical edge
                    try_again = True
                    break
                elif point[1] // (constants.blocks_y-1):
                    # Goes over horizontal edge
                    try_again = True
                    break

            # If everything was fine
            if not try_again:
                break

        # Update map to show these new points
        for point in self.get_points():
            map[point[1]][point[0]] = self

        # Render the fruit
        # The upper left corner
        x, y = index_to_pixels(self.x, self.y)

        white = (255, 255, 255)
        n = (constants.cell_size * self.size) / 3
        pygame.draw.rect(screen, white, (x + n, y, n, n))
        pygame.draw.rect(screen, white, (x, y + n, n, n))
        pygame.draw.rect(screen, white, (x + 2*n, y + n, n, n))
        pygame.draw.rect(screen, white, (x + n, y + 2*n, n, n))

    def eat(self):
        """Destroy the fruit and create a new one."""
        for point in self.get_points():
            x, y = point
            if self.map[y][x] == self:
                self.map[y][x] = 0
                fruit_coord = index_to_pixels(x, y)
                pygame.draw.rect(self.screen, (0, 0, 0), (fruit_coord[0], fruit_coord[1], constants.cell_size, constants.cell_size))

        BigFruit(self.screen, self.map)

    def get_points(self):
        """Uses the size to generate a list of xy points that the fruit will use. Returns a list of xy tuples."""
        points = []
        for dy in range(self.size):
            for dx in range(self.size):
                x = (self.x + dx) % constants.blocks_x
                y = (self.y + dy) % constants.blocks_y
                points.append((x, y))
        return points

class Snake:
    """A snake. Moves forward every cycle and contains event handlers for turning."""

    def __init__(self, X, Y, map, *, controls=None, color=(255, 255, 255), score_coords=(10,10)):
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
        self.score_coords = score_coords

    def get_color(self):
        """Generate a color for the head by factoring in the x and y position."""
        x, y = index_to_pixels(self.X, self.Y)
        r = self.color[0] or 150 + 100 * (x / constants.screen_width)
        g = self.color[1] or 100 + 150 * (y / constants.screen_height)
        b = self.color[2] or 150 + 100 * (x / constants.screen_width)
        return (int(r), int(g), int(b))


    def move(self, screen):
        """Move forward one cell. Check the map for collisions with snakes or fruits."""
        # The new coord modulo the max coord. This means the snake will wrap back to the beginning.

        new_X = (self.X + self.dX) % constants.blocks_x
        new_Y = (self.Y + self.dY) % constants.blocks_y

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
        pygame.draw.rect(screen, black, (tail_coord[0], tail_coord[1], constants.cell_size, constants.cell_size))

        # Draw new head
        head_coord = index_to_pixels(head[0], head[1])
        # color = (100, 255 * (head_coord[0] / constants.screen_width), 255 * (head_coord[1] / constants.screen_height))
        color = self.get_color()
        pygame.draw.rect(screen, color, (head_coord[0], head_coord[1], constants.cell_size-1, constants.cell_size-1))

        pygame.display.update()

    def collision_detect(self, obstacle, screen):
        """Detect collisions. If fruit, eat it and grow. If snake, raise Exception('Game Over')."""
        if obstacle == 1:
            # Snake Collision
            self.loser = True
            raise Exception("Game Over")
        elif isinstance(obstacle, Fruit):
            # Fruit Collision
            obstacle.eat()    # Basically the Fruit's deconstructor
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

class NPCController:
    """Generates virtual events for npc snakes and defines the algorithm for when those events will be raised."""

    VIRT_EVENT = pygame.USEREVENT + 1

    def __init__(self, n=1):
        """Create vitrual event types for up, down, left, right."""
        self.n = n

    def bind_snake(self, *args, **kwargs):
        """Bind a snake to this controller."""
        controls = self.get_virtual_events()
        kwargs['controls'] = controls
        self.snake = Snake(*args, **kwargs)

        return self.snake

    def get_virtual_events(self):
        """Returns a tuple of the virtual events in the order of up, down, left right. This is meant to be passed along to the controls parameter of a snake."""
        controls = []
        for control in ('up', 'down', 'left', 'right'):
            controls.append((self.n, control))
        return controls

    def post_events(self, *args, **kwargs):
        """This is the method that will raise the virtual events. It calls on move_algorithm to decide which event to raise."""
        movement = self.move_algorithm(*args, **kwargs)
        if not (movement is None):
            pygame.event.post(pygame.event.Event(self.VIRT_EVENT, n=self.n, dir=movement))

    def move_algorithm(self):
        """Defines when which event will be raised. This is the function to be overwritten in inheritance. Should return 'up', 'down', 'left', 'right', or None.

        This default algorithm randomly decides to turn based on a constant percent chance."""
        # Percent chance of a turn
        turn_chance = 0.10

        n = random.random()

        # Of the 4 turns, only 2 will have an effect.
        if n < (turn_chance * (1/4)):
            return 'up'
        elif n < (turn_chance * (1/2)):
            return 'down'
        elif n < (turn_chance * (3/4)):
            return 'left'
        elif n < turn_chance:
            return 'right'

class EasyNPC(NPCController):
    def move_algorithm(self, map, *args, **kwargs):
        dX = map.fruits[0].x - self.snake.X
        dY = map.fruits[0].y - self.snake.Y

        if (dX + dY) == 0:
            return None
        probRight = (dX / (dX + dY))
        probUp = (dY / (dY + dX))

        if (abs(probRight * random.random()) > abs(probUp * random.random())):
            if probRight > 0:
                return 'right'
            else:
                return 'left'
        else:
            if probUp > 0:
                return 'up'
            else:
                return 'down'

class Map(list):
    """The map containing all fruits and snakes."""

    def __init__(self, x, y):
        """Create matrix."""
        list.__init__(self)

        for iy in range(y):
            row = []
            for ix in range(x):
                row.append(0)
            self.append(row)

        self.fruits = []



def NPC_algo(fruit, snake):
    dX = fruit.x - snake.X
    dY = fruit.y - snake.Y

    probRight = (dX / (dX + dY))
    probUp = (dY / (dY + dX))

    if (abs(probRight * random.random()) > abs(probUp * random.random())):
        if probRight > 0:
            return 'right'
        else:
            return 'left'
    else:
        if probUp > 0:
            return 'up'
        else:
            return 'down'


def index_to_pixels(x, y):
    """Convert the index coordinates to pixel coordinates. Returns (x, y) in pixels."""
    new_x = x * constants.cell_size
    new_y = y * constants.cell_size
    return new_x, new_y


if __name__ == '__main__':
    if (constants.screen_width % constants.cell_size) or (constants.screen_height % constants.cell_size):
        raise Exception('constants.screen_width and constants.screen_height must be divisible by constants.cell_size')

    pygame.init()
    pygame.display.set_caption("Tron Snake")
    icon = pygame.image.load("snake-2.png")
    pygame.display.set_icon(icon)

    # Loop allows restarting
    while main():
        pass
