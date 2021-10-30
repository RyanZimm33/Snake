# Space Snakes

This is a project created for Missouri S&T's 2021 PickleHack. Us four concieved, designed, and created this take on the classice snake game in 24 hours.

There are three main sections to our code, all of which are called from the main function. The first section calls game_intro, which displays our welcoming screen as well as allowing users to change options. The next section is the game_loop. Here an event loop is run to take in keyboard inputs and our snakes are moved forward every so many seconds. Each snake checks for collisions with either other snakes or fruits, which makes it grow. Once a snake has collided with another (or itself), end_screen is ran. In end_screen, we display all of the game statistics and allow the users to restart on any keypress.

This project uses pygame 2.0.2 and python 3.10.
