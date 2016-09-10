# Spencer Amarantides (sta7ey), Ian Linville (Il3k3)

import pygame
import gamebox
import random


CAMERA_HEIGHT = 600
CAMERA_WIDTH = 800
camera = gamebox.Camera(CAMERA_WIDTH,CAMERA_HEIGHT)
TICKS_PER_SECOND = 30
my_font = pygame.font.SysFont("monospace",24)
TIMER = 60
COUNTER = 0
soundfx = gamebox.load_sound("LFO+16.wav")

# Create players and lives
# Player one loses live when started to create intro screen
player1 = gamebox.from_image(400, 75, "hokie.png")
P1_LIVES = 11
P1_SCORE = 0
player2 = gamebox.from_image(300, 75, "cavalier.png")
P2_LIVES = 10
P2_SCORE = 0
reward = gamebox.from_image(random.randint(100, CAMERA_WIDTH -100), CAMERA_HEIGHT - 40, "reward.png")
# Default coin
coin = gamebox.from_color(-100, -100, "green", 0, 0)

# Safe Areas
row1 = gamebox.from_color(-100,50, "dark green", 3000, 150)
row2 = gamebox.from_color(-100,300, "dark green", 3000, 60)
row3 = gamebox.from_color(-100,550, "dark green", 3000, 150)

# Boundaries
left_wall = gamebox.from_color(-1,0, "black", 20, 3000)
right_wall = gamebox.from_color(CAMERA_WIDTH + 1, 0, "black", 20, 3000)
top_wall = gamebox.from_color(0, -1, "black", 3000, 20)
bottom_wall = gamebox.from_color(0, CAMERA_HEIGHT + 1, "black", 3000, 20)
wall_list = [left_wall,right_wall,top_wall,bottom_wall]

#Intro
black_screen = gamebox.from_color(-100,-100, "black", 3000,3000)

# Cars
car_speed = 7
car_row = []


# Set enemy cars randomly
def set_enemy_cars():
    number_of_enemies = 0
    while number_of_enemies <= 18:
        y = random.randint(1,6)
        if y == 1:
            car_row.append(gamebox.from_color(random.randint(1,799), 150,
                            "Yellow", random.randint(75,150),40))
        elif y == 2:
            car_row.append(gamebox.from_color(random.randint(1,799), 200,
                            "Red", random.randint(75,150),40))
        elif y == 3:
            car_row.append(gamebox.from_color(random.randint(1,799), 250,
                            "White", random.randint(75,150),40))
        elif y == 4:
            car_row.append(gamebox.from_color(random.randint(1,799), 350,
                            "Black", random.randint(75,150),40))
        elif y == 5:
            car_row.append(gamebox.from_color(random.randint(1,799), 400,
                            "Orange", random.randint(75,150),40))
        else:
            car_row.append(gamebox.from_color(random.randint(1,799), 450,
                            "Pink", random.randint(75,150),40))
        number_of_enemies += 1

# Scoring
def scoring():
    global P1_SCORE, P2_SCORE, coin
    if player1.touches(reward):
        soundfx.play()
        P1_SCORE += 5
        player1.x = 300
        player1.y = 75
        reward.x = random.randint(100,CAMERA_WIDTH - 100)
    if player2.touches(reward):
        soundfx.play()
        P2_SCORE += 5
        player2.x = 300
        player2.y = 75
        reward.x = random.randint(100,CAMERA_WIDTH - 100)

    # Coin scoring
    if COUNTER % (TICKS_PER_SECOND * 10) == 0:
        coin = coins()
    if player1.touches(coin):
        P1_SCORE += 1
        coin.y = 1000
    if player2.touches(coin):
        P2_SCORE += 1
        coin.y = 1000

def coins():
    xStart = random.randint(100,700)
    yStart = random.randint(150,500)
    coin = gamebox.from_color(xStart,yStart,"gold",20,20)
    return coin


def handle_collisions():
    global P1_LIVES, P2_LIVES
    # Player-car collisions
    for car in car_row:
        if car.touches(player1):
            player1.y = 75
            player1.x = 300
            P1_LIVES -= 1
        if car.touches(player2):
            player2.y = 75
            player2.x = 400
            P2_LIVES -= 1

    # remove from board when lives run out
    if P1_LIVES == 0:
        player1.x = -500
    if P2_LIVES == 0:
        player2.x = -500

    # Player-player collisions
    # Give advantage to Cavaliers (Player 2)
    if player1.left_touches(player2):
        player1.xspeed = 10
        player1.x += player1.xspeed
    elif player1.right_touches(player2):
        player1.xspeed = -10
        player1.x += player1.xspeed
    elif player1.top_touches(player2):
        player1.yspeed = 10
        player1.y += player1.yspeed
    elif player1.bottom_touches(player2):
        player1.yspeed = -10
        player1.y += player1.yspeed

    # Player-boundary collisions
    for wall in wall_list:
        if player1.touches(wall):
            player1.move_to_stop_overlapping(wall)
        if player2.touches(wall):
            player2.move_to_stop_overlapping(wall)


#play game
def tick(keys):
    global P1_LIVES, COUNTER, TIMER

    # Labels
    lives_label = my_font.render("Lives Hokies: " + str(P1_LIVES) + " Cavaliers: " +
                             str(P2_LIVES), 1, (255,255,255))
    score_label = my_font.render("Score Hokies: " + str(P1_SCORE) + " Cavaliers: " +
                             str(P2_SCORE), 1, (255,255,255))
    timer_label = my_font.render("Timer: " + str(TIMER), 1, (255,255,255))

    # Introduction
    if P1_LIVES ==11:
        introLabel = my_font.render("CAVALIER-HOKIE FROGGER", 1, (255,255,255))
        promptUser = my_font.render( "Press Space Bar to start the Game",1, (255,255,255))
        camera.draw(introLabel, (CAMERA_WIDTH//2,300))
        camera.draw(promptUser, (CAMERA_WIDTH//2,325))
        if pygame.K_SPACE in keys:
            P1_LIVES = 10
    # Closing
    elif P1_LIVES == 0 and P2_LIVES ==0 or TIMER == 0:
        closeLabel = my_font.render("GAME OVER", 1, (255,255,255))
        camera.draw(black_screen)
        camera.draw(closeLabel, (CAMERA_WIDTH//2,300))
        camera.draw(score_label, (CAMERA_WIDTH//2,325))
        winning_label = ""
        if P1_SCORE > P2_SCORE:
            winning_label = my_font.render("Hokies win...", 1, (255,255,255))
        elif P2_SCORE > P1_SCORE:
            winning_label = my_font.render("CAVALIERS WINS!", 1, (255,255,255))
        else:
            winning_label = my_font.render("Tie", 1, (255,255,255))
        camera.draw(winning_label, (CAMERA_WIDTH//2,350))

    # Game
    else:
        #set timer
        COUNTER += 1
        if COUNTER % TICKS_PER_SECOND == 0:
            TIMER -= 1

        # 2 player movement
        if pygame.K_d in keys:
            player1.x += 7
        if pygame.K_a in keys:
            player1.x -= 7
        if pygame.K_w in keys:
            player1.y -= 7
        if pygame.K_s in keys:
            player1.y += 7
        if pygame.K_RIGHT in keys:
            player2.x += 7
        if pygame.K_LEFT in keys:
            player2.x -= 7
        if pygame.K_UP in keys:
            player2.y -= 7
        if pygame.K_DOWN in keys:
            player2.y += 7

        handle_collisions()
        scoring()

        camera.clear("grey")
        camera.draw(row1)
        camera.draw(row2)
        camera.draw(row3)
        camera.draw(player1)
        camera.draw(player2)
        camera.draw(reward)
        camera.draw(coin)

        # Draw Cars
        for car in car_row:
            camera.draw(car)
            if car.y == 150 or car.y == 250 or car.y == 400:
                car.xspeed = -1 * car_speed
                car.x += car.xspeed
            else:
                car.xspeed = car_speed
                car.x += car.xspeed

        # Wrap
        for car in car_row:
            if car.right <= 0:
                car.left = CAMERA_WIDTH -1
            elif car.left >= CAMERA_WIDTH:
                car.right = 1

        # Draw labels
        camera.draw(lives_label, (225,10))
        camera.draw(score_label, (210,35))
        camera.draw(timer_label, (725,10))

    camera.display()

set_enemy_cars()
gamebox.timer_loop(TICKS_PER_SECOND, tick)