import pygame, random


# intialising essential parts of pygame
WIDTH = 750
HEIGHT = 750
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("TANKS_V2")


# miscellaneous constants
TANKS = 6
SIZE = 7
GRID_HEIGHT = 600
# RGB colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# class for the game board
class board:
    def __init__ (self): 
        self.BOX_WIDTH = int((WIDTH / SIZE))
        self.BOX_HEIGHT = int((GRID_HEIGHT / SIZE))
        self.colour_list = [[BLACK for i in range(SIZE)] for j in range(SIZE)]
        self.tanklist = [["-" for i in range(SIZE)] for j in range(SIZE)]
        self.player1 = "P1"
        self.player2 = "P2"
        self.bool = True
        self.turn_counter = 0


    def turn(self):
        """ A method that displays text for the player's turn """
        if self.bool:
            if self.turn_counter % 2 == 0:
                font = pygame.font.Font('freesansbold.ttf', 35).render("Blue player's turn...", True, BLACK, WHITE)
                rectfont = font.get_rect()
                rectfont.center = (WIDTH // 2, HEIGHT // 16)
                screen.blit(font, rectfont)
            else:
                font = pygame.font.Font('freesansbold.ttf', 35).render("Red player's turn...", True, BLACK, WHITE)
                rectfont = font.get_rect()
                rectfont.center = (WIDTH // 2, HEIGHT // 16)
                screen.blit(font, rectfont)


    def game_over(self, colour, string):
        """ a method that, when one of the scores is zero, will display some pygame text saying the other player has won """
        num = self.count_score(colour, True)
        if num == 0:            
            font = pygame.font.Font('freesansbold.ttf', 35).render(f"{string} player has won!", True, BLACK, WHITE)
            rectfont = font.get_rect()
            rectfont.center = (WIDTH // 2, HEIGHT // 12)
            screen.blit(font, rectfont)
            self.bool = False
  


    def display_score_blue(self):
        """ a method that displays how many tanks the blue player has left """
        blue_display = self.count_score(BLUE, True)
     
        square_width = WIDTH // 15
        square_height = HEIGHT // 15
        
        for x in range(blue_display):
            width = (square_width * x + 5)
            score = pygame.Rect(width, square_height + 35, square_width - 5, square_height)
            pygame.draw.rect(screen, BLUE, score)


    def display_score_red(self):
        """ displays how many tanks the red player has left (the loop is done differently so 
            it pops off the squares from the other side)
        """
        red_display = self.count_score(RED, False)

        square_width = WIDTH // 15
        square_height = HEIGHT // 15
        x = SIZE
        while x > red_display:
            width = (square_width * x + 400)
            score = pygame.Rect(width, square_height + 35, square_width - 5, square_height)
            pygame.draw.rect(screen, RED, score)
            x -= 1


    def count_score(self, colour, bool):
        """ a method that counts the number of specified colours in the colour_list grid """
        if bool:
            playercount = TANKS - sum(x.count(colour) for x in self.colour_list)
            return playercount
        else:
            playercount = sum(x.count(colour) for x in self.colour_list)
            return playercount
    

    def mouse_pos(self):
        """ a method that maps where the user has left clicked to the grid  """
        if self.bool:
            self.mouse_position = pygame.mouse.get_pos()
            nums = [0, 1, 2, 3, 4, 5, 6]
            col = self.mouse_position[0] // self.BOX_WIDTH
            row = self.mouse_position[1] // self.BOX_HEIGHT - 2 

            if col in nums and row in nums:
                if self.colour_list[row][col] == BLACK:
                    if self.tanklist[row][col] == "-":
                        self.colour_list[row][col] = WHITE
                        self.turn_counter += 1
                    
                    if self.tanklist[row][col] == self.player1:
                        self.colour_list[row][col] = BLUE
                        self.turn_counter += 1
            
                    if self.tanklist[row][col] == self.player2:
                        self.colour_list[row][col] = RED
                        self.turn_counter += 1


    def random_placement(self, player):
        """ a method that randomly places player tanks onto the 2d grid """
        counter = 0
        while counter < TANKS:
            row = random.randint(0,6)
            col = random.randint(0,6)
            
            if self.tanklist[row][col] == "-":
                self.tanklist[row][col] = player
                counter += 1


    def draw_board(self):
        """ a method that draws the grid to the game window """
        screen.fill(WHITE)
        for row in range(SIZE):
            for column in range(SIZE):
                
                width = column * self.BOX_WIDTH + 3
                height = row * self.BOX_HEIGHT + 155
                square = pygame.Rect(width, height, self.BOX_WIDTH - 5, self.BOX_HEIGHT - 5)

                if self.tanklist[row][column] == "-":
                    pygame.draw.rect(screen, self.colour_list[row][column], square)
                
                elif self.tanklist[row][column] == self.player1:
                    pygame.draw.rect(screen, self.colour_list[row][column], square)
                
                elif self.tanklist[row][column] == self.player2:
                    pygame.draw.rect(screen, self.colour_list[row][column], square)
        
        self.display_score_blue()
        self.display_score_red()
        self.game_over(RED, "Blue")
        self.game_over(BLUE, "Red")
        self.turn()
                

board_ = board()
board_.random_placement(board_.player1)
board_.random_placement(board_.player2)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                board_.mouse_pos()
        board_.draw_board()
        
        pygame.display.flip()
        clock.tick(10)  

    pygame.quit()


if __name__ == "__main__":
    main()
