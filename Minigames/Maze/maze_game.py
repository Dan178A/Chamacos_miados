import pygame
import random
from maze_generation import hunt_n_kill

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (400 , 400)  # Adjusted for smaller cells
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Variable Grid")

# Set up the game clock
clock = pygame.time.Clock()

# Sprites
Wall_Sprite=pygame.image.load('images/Wall.png').convert()
Path_Sprite=pygame.image.load('images/Path.png').convert()

Player_Sprite=pygame.image.load('images/Hook.png').convert()

Fish1_Sprite=pygame.image.load('images/Fish_01.png').convert()
Fish2_Sprite=pygame.image.load('images/Fish_02.png').convert()
Fish3_Sprite=pygame.image.load('images/Fish_03.png').convert()

# Define the grid
grid_width = 9
grid_height = 9
cell_size = 16
grid = hunt_n_kill(grid_width, grid_height)

def Maze_Game():
    player_x, player_y=grid_width-1,0
    # Game loop
    catch_level = 0
    done = False
    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a and player_x>0:
                    if grid[player_x-1][player_y] >0:
                        player_x -=1
                if event.key==pygame.K_w and player_y>0:
                    if grid[player_x][player_y-1] >0:
                        player_y-=1
                if event.key==pygame.K_s and player_y<(grid_height*2)-1:
                    if grid[player_x][player_y+1] >0:
                        player_y+=1
                if event.key==pygame.K_d and player_x<(grid_width*2)-1: 
                    if grid[player_x+1][player_y] >0:
                        player_x+=1



        # Clear the screen
        screen.fill((100, 100, 100))

        # Draw the grid
        for x in range(0, grid_width*2-1, 1):
            for y in range(0,grid_height*2-1, 1):
                cell_x, cell_y = x * cell_size, y * cell_size
                if grid[x][y]== 0:
                    screen.blit(Wall_Sprite, (cell_x, cell_y))
                elif grid[x][y] == 1: 
                    screen.blit(Path_Sprite, (cell_x, cell_y))
                else:
                    if grid[x][y] <15:
                        screen.blit(Fish1_Sprite, (cell_x, cell_y))
                    elif grid[x][y] <30:
                        screen.blit(Fish2_Sprite, (cell_x, cell_y))
                    else:
                        screen.blit(Fish3_Sprite, (cell_x, cell_y))

        screen.blit(Player_Sprite, (player_x*cell_size, player_y*cell_size))
        
        if grid[player_x][player_y] >1:
            done=True
            if grid[x][y] <15:
                catch_level=1
            elif grid[x][y] <30:
                catch_level=2
            else:
                catch_level=3
                        
        # Update the screen
        pygame.display.flip()

        # Tick the clock
        clock.tick(60)
    
    return catch_level
    
    
if __name__ == "__main__":
    print(Maze_Game())