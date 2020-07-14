# File: fallingsand.py
# Author: Chongliang Tao
# A Falling Sand game.

import pygame
import random

# Constants that control the sizes and speeds of things.
WINDOW_WIDTH = 80
WINDOW_HEIGHT = 80
DRAW_WIDTH = 10
DRAW_HEIGHT = 10
INITIAL_SPEED = 19

# Raduis that control the BOMB(additional particle).
RADIUS = 5

# Types of substances that can exist in the world.
BLANK = 0
METAL = 1
SAND = 2
WATER = 3
ACID = 4
GAS = 5
BOMB = 6

# A list of tuples that stores the colors of different substances.
color = [
    (255, 255, 255),  # BLANK
    (128, 128, 128),  # METAL
    (200, 200, 0),    # SAND
    (0, 0, 200),      # WATER
    (0, 200, 0),      # ACID
    (192, 192, 192),  # GAS
    (255, 0, 0)       # BOMB
]


def clear_picture(picture):
    '''
    Function: clear_picture
        Removes everything from the screen and sets every position
        back to BLANK.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
    Returns:
        None
    '''
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            picture[y][x] = BLANK


def draw_screen(picture, screen):
    '''
    Function: draw_screen
        Draws the current picture onto the screen.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
        screen  -- The pygame screen onto which we can draw.
    Returns:
        None
    '''
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            location = (x * DRAW_WIDTH, y * DRAW_HEIGHT,
                        DRAW_WIDTH, DRAW_HEIGHT)
            pygame.draw.rect(screen, color[picture[y][x]], location)


def count2d(picture, thing):
    '''
    Function: count2d
        Counts how many times something appears in a nested list.
        This might be useful in debugging.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
        thing   -- Something that might appear in the list.
    Returns:
        The number of thing that appears within picture.
    '''
    counter = 0
    for row in picture:
        counter += row.count(thing)
    return counter


def move_sand(picture, y, x):
    '''
    Function: move_sand
        call helper function called vertical_motion to realize the falling 
        motion of SAND.
        If the particle directly below it is blank, the two particles swap.
        If the particle is in the bottom of the window, it's replaced by a blank.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the sand particle in the list.
              x -- The x coordinate of the location of the sand particle in the list.
    Returns:
        None
    '''
    y_update = vertical_motion(picture, y, x, SAND)
    # If the particle has reached the bottom of the screen, it should be BLANK.
    if y_update == WINDOW_HEIGHT - 1:
        picture[y_update][x] = BLANK


def move_water(picture, y, x):
    '''
    Function: move_water
        It allows vertical gravity and sideways motions.
        Vertical motion:
        If the particle directly below it is blank, the two particles swap.
        If the particle is in the bottom of the window, it's replaced by a blank.
        Sideway motion:
        Whenever a water particle cannot fall downward,randomly
        choose a direction: left or right.
        Then if there is a blank in that direction the water will swap positions with it.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the water particle in the list.
              x -- The x coordinate of the location of the water particle in the list.
    Returns:
        None
    '''
    # call helper function to realize the falling motion of WATER.
    y_update = vertical_motion(picture, y, x, WATER)
    # If the particle has reached the bottom of the screen, it should be BLANK.
    if y_update == WINDOW_HEIGHT - 1:
        picture[y_update][x] = BLANK
        return
    # We only move one step at a time. Only if y == y_update means it has reach the
    # very bottom it can reach. Then we can consider its sideways motion.
    if y != y_update:
        return

    # Add sideways motion.
    sideway_motion(picture, y, x, WATER)


def vertical_motion(picture, y, x, particle):
    '''
    Function: vertical_motion
        It allows vertical gravity and sideways motions.
        Vertical motion:
        If the particle directly below it is blank, the two particles swap.
        If the particle is in the bottom of the window, it's replaced by a blank.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the particle in the list.
              x -- The x coordinate of the location of the particle in the list.
       particle -- The type of particle that uses.
    Returns:
              y -- A integer, indicating the updated y cooridinate of the particle.
    '''
    # If the particle is at the bottom, it can't fall any further.
    if y == WINDOW_HEIGHT - 1:
        return y
    # Create a list of the particle that can fall into water.
    particle_list = [SAND, ACID]
    # If the particle below it is blank, we should swap the two particles.
    if picture[y + 1][x] == BLANK:
        picture[y][x] = BLANK
        picture[y + 1][x] = particle
        y += 1
    # If it's SAND or ACID, it can swap with water.
    elif particle in particle_list and picture[y + 1][x] == WATER:
        picture[y][x] = WATER
        picture[y + 1][x] = particle
        y += 1
    return y


def sideway_motion(picture, y, x, particle):
    '''
    Function: sideway_motion
        Sideway motion as follows:
        Whenever a water particle cannot fall downward,randomly
        choose a direction: left or right.
        Then if there is a blank in that direction the water will swap positions with it.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the particle in the list.
              x -- The x coordinate of the location of the particle in the list.
       particle -- The type of particle that uses.
    Returns:
        None
    '''

    direction = random.randrange(2)
    # If the direction is left, x coordinate should decrease by 1.
    if direction == 0:
        dx = -1
    # If the direction is left, x coordinate should increase by 1.
    else:
        dx = 1
    if x + dx >= 0 and x + dx <= WINDOW_WIDTH - 1:
        # If that nearby location is not blank, then it won't move.
        if picture[y][x + dx] != BLANK:
            return
        picture[y][x] = BLANK
        picture[y][x + dx] = particle
    else:
        # The particle has move outside the canvas.
        picture[y][x] = BLANK


def move_acid(picture, y, x):
    '''
    Function: move_acid
        Vertical motion:
        If the particle directly below it is blank, the two particles swap.
        If the particle is in the bottom of the window, it's replaced by a blank.
        When it cannot fall downward, it has of the three behaviors:
        1. 80% of the time, it does the same thing water would do.
        2. 15% of the time, it randomly chooses one of the four cardinal 
           directions around it,
           if that location is filled with water it swaps positions with the water.
        3. 5% of the time, if it has metal or sand below it,
           it dissolves that metal or sand (converting it to blank).
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the acid particle in the list.
              x -  The x coordinate of the location of the acid particle in the list.
    Returns:
        None
    '''
    # Call helper function to realize the falling motion of WATER.
    y_update = vertical_motion(picture, y, x, ACID)
    # If the particle has reached the bottom of the screen, it should be BLANK.
    if y_update == WINDOW_HEIGHT - 1:
        picture[y_update][x] = BLANK
        return
    # We only move one step at a time. Only if y == y_update means it has reach the
    # very bottom it can reach. Then we can consider its sideways motion.
    if y != y_update:
        return

    # Create a random variable to choose the following motion
    choice = random.randrange(100)
    if choice < 80:
        # Behave like water.
        sideway_motion(picture, y, x, ACID)
    elif choice < 95:
        direction = random.randrange(4)
        # Use dx, dy to indicate the change of coordinate.
        dx = 0
        dy = 0
        if direction == 0:
            dx = -1
        elif direction == 1:
            dx = 1
        elif direction == 2:
            dy = -1
        else:
            dy = 1
        # If it moves outside the canvas, update it with BLANK.
        if x + dx < 0 or x + dx > WINDOW_WIDTH - 1:
            picture[y][x] = BLANK
            return
        elif y + dy < 0 or y + dy > WINDOW_HEIGHT - 1:
            picture[y][x] = BLANK
            return
        else:
            # Swap with water in that position.
            if picture[y + dy][x + dx] == WATER:
                picture[y][x] = WATER
                picture[y + dy][x + dx] = ACID
    else:
        if y < WINDOW_HEIGHT - 1:
            # Dissolve the metal or sand.
            if picture[y + 1][x] == METAL or picture[y + 1][x] == SAND:
                picture[y + 1][x] = BLANK


def move_gas(picture, y, x):
    '''
    Function: move_gas
        gas moves up.
        "bubble up" through water and water by swapping position with them.
        20% of the time it moves randomly to the right or left.   
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the gas particle in the list.
              x -  The x coordinate of the location of the gas particle in the list.
    Returns:
        None
    '''
    random_number = random.randrange(100)
    # Use dx, dy to indicate the change of coordinate.
    dx = 0
    dy = 0
    # 20% the time it moves left or right.
    if random_number < 20:
        direction = random.randrange(2)
        if direction == 0:
            dx = -1
        else:
            dx = 1
    # At other times it moves upwards.
    else:
        dy = -1
    # If it moves outside the canvas, update it with BLANK.
    if x + dx < 0 or x + dx > WINDOW_WIDTH - 1:
        picture[y][x] = BLANK
        return
    elif y + dy < 0 or y + dy > WINDOW_HEIGHT - 1:
        picture[y][x] = BLANK
        return
    # Swap with blank when it can.
    if picture[y + dy][x + dx] == BLANK:
        picture[y + dy][x + dx] = GAS
        picture[y][x] = BLANK
    # Swap with water when it can.
    elif picture[y + dy][x + dx] == WATER:
        picture[y + dy][x + dx] = GAS
        picture[y][x] = WATER


def check_bomb(picture, y, x):
    '''
    Function: check_bomb
        This special particle - BOMB has following properties:
        1. It should first fall down if the particle under it is BLANK
        2. If it's next to an ACID(in any of the four directions,
        it will destroy everything(including itself) in a radius of square.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the particle in the list.
              x -- The x coordinate of the location of the particle in the list.
    Returns:
        None
    '''
    # Call helper function to realize the falling motion of BOMB.
    y_update = vertical_motion(picture, y, x, BOMB)
    # If the particle has reached the bottom of the screen, it should be BLANK.
    if y_update == WINDOW_HEIGHT - 1:
        picture[y_update][x] = BLANK
        return
    # We only move one step at a time. Only if y == y_update means it has reach the
    # very bottom it can reach. Then we can consider its sideways motion.
    if y != y_update:
        return

    # Check if the bomb is next to an acid.
    if next_to_acid(picture, y, x):
        # Find the upper-left corner of the square in which things
        # will be destroyed by the bomb.
        upper_left_x = x
        upper_left_y = y
        for i in range(RADIUS):
            # Check if this location is inside the canvas.
            if upper_left_x - 1 >= 0:
                upper_left_x -= 1
            if upper_left_y - 1 >= 0:
                upper_left_y -= 1
        # Destroy everything inside the square defined by the square.
        destroy(picture, upper_left_x, upper_left_y)


def destroy(picture, upper_left_x, upper_left_y):
    '''
    Function: destroy
        This fucntion is designed for the BOMB particle:
        If it's next to an ACID(in any of the four directions,
        it will destroy everything(including itself) in a radius of square.
    Arguments:
        picture      -- A nested list containing what type of substance
                        is at each position in the picture.
        upper_left_y -- The y coordinate of the upper_left corner of the square that
                        everything will be destroyed.
        upper_left_x -- The x coordinate of the upper_left corner of the square that
                        everything will be destroyed.
    Returns:
        None
    '''
    # Nested loop to destroy everthing into BLANK in the sqaure.
    for i in range(2 * RADIUS):
        for j in range(2 * RADIUS):
            # Found the location of the object to be destroyed.
            x_coordinate = upper_left_x + j
            y_coordinate = upper_left_y + i
            # Check if this location is outside the canvas.
            if x_coordinate > WINDOW_WIDTH - 1:
                continue
            # Check if this location is outside the canvas.
            if y_coordinate > WINDOW_HEIGHT - 1:
                continue
            picture[y_coordinate][x_coordinate] = BLANK


def next_to_acid(picture, y, x):
    '''
    Function: next_to_acid
        Check if at four possible nearby location(up, right, down, left)
        exists an acid.
    Arguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
              y -- The y coordinate of the location of the particle in the list.
              x -- The x coordinate of the location of the particle in the list.
    Returns:
        boolean -- Whether there's an acid at four cardinal directions.
    '''
    # Create a list to find the x and y coordinate of the four cardinal directions。
    x_shift = [0, 1, 0, -1]
    y_shift = [-1, 0, 1, 0]
    for i in range(4):
        # Update the x and y coordinate.
        x_coordinate = x + x_shift[i]
        y_coordinate = y + y_shift[i]
        # Check if this location is outside the canvas.
        if x_coordinate < 0 or x_coordinate > WINDOW_WIDTH - 1:
            continue
        if y_coordinate < 0 or y_coordinate > WINDOW_HEIGHT - 1:
            continue
        # Check if an acid exists.
        if picture[y_coordinate][x_coordinate] == ACID:
            return True
    return False


def update_picture(picture, speed):
    '''
    Function: update_picture
        Moves some particles to new locations.
    Aguments:
        picture -- A nested list containing what type of substance
                   is at each position in the picture.
        speed   -- The likelihood of each particle moving (1-100).
    Returns:
        None
    '''
    for y in range(WINDOW_HEIGHT - 1, -1, -1):
        for x in range(WINDOW_WIDTH - 1, -1, -1):
            if random.randrange(100) < speed:
                if picture[y][x] == SAND:
                    move_sand(picture, y, x)
                elif picture[y][x] == WATER:
                    move_water(picture, y, x)
                elif picture[y][x] == ACID:
                    move_acid(picture, y, x)
                elif picture[y][x] == GAS:
                    move_gas(picture, y, x)
                elif picture[y][x] == BOMB:
                    check_bomb(picture, y, x)


def main():
    # Sets up the screen for us.
    pygame.init()
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH * DRAW_WIDTH, WINDOW_HEIGHT * DRAW_HEIGHT))
    pygame.display.set_caption("Falling Sand Game")
    screen.fill(color[BLANK])
    pygame.display.update()

    # Sets up the picture for us.
    picture = []
    for y in range(WINDOW_HEIGHT):
        row = []
        for x in range(WINDOW_WIDTH):
            row.append(BLANK)
        picture.append(row)

    # Initializes some other variables for us.
    current_type = METAL
    speed = INITIAL_SPEED
    did_quit = False
    paused = False

    # A big loop that runs until we close the window.
    while not did_quit:
        # Process events.
        for event in pygame.event.get():
            # If the user closed the window, we should quit.
            if event.type == pygame.QUIT:
                did_quit = True
            # If a key was pressed, we should do something.
            elif event.type == pygame.KEYDOWN:
                the_key = event.unicode.lower()
                if the_key == 'b':
                    current_type = BLANK
                elif the_key == 'm':
                    current_type = METAL
                elif the_key == 's':
                    current_type = SAND
                elif the_key == 'w':
                    current_type = WATER
                elif the_key == 'a':
                    current_type = ACID
                elif the_key == 'g':
                    current_type = GAS
                elif the_key == 'v':
                    current_type = BOMB
                # Clear picture.
                elif the_key == 'c':
                    clear_picture(picture)
                # Pauses (if it was not paused), or unpauses (if it was paused).
                elif the_key == 'p':
                    paused = not paused
                # Increase speed.
                elif the_key == 'u':
                    if speed < 100:
                        # Make sure speed does not exceed 100
                        # even though we don't have to.
                        if speed * 3 < 100:
                            speed *= 3
                        else:
                            speed = 100
                # Increase speed.
                elif the_key == 'd':
                    if speed > 1:
                        speed = speed // 3
                    # Handle the sitution when speed was at 2, and then change to 0.
                    # We can then update speed to 1. I want to make sure speed is in [1,100].
                    if speed == 0:
                        speed = 1

        # If the mouse button is pressed down, we are drawing someething.
        if pygame.mouse.get_pressed()[0]:
            (x, y) = pygame.mouse.get_pos()
            # This finds the upper-left corner of the square we clicked in.
            picture[y // DRAW_HEIGHT][x // DRAW_WIDTH] = current_type

        # Update the picture, then re-draw it.
        if not paused:
            update_picture(picture, speed)
        draw_screen(picture, screen)
        pygame.display.update()

    # Quit the game after the user has closed the window.
    pygame.quit()


if __name__ == '__main__':
    main()
