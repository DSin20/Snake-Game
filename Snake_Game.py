import pygame 
import random 
from enum import Enum
from collections import namedtuple
import math



pygame.init()

font = pygame.font.Font('/Users/dipendersingh/Desktop/Python Projects/Snake', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2 
    UP = 3
    DOWN = 4
Point = namedtuple('Point', 'x, y')

B_size = 20
#colours
W = (255,255,255)
R = (200,0,0)
B1 = (0,0,255)
B2 = (0,100,255)
BL = (0,0,0)

class SnakeGame:
    def __init__(self, w=840, h=560):
        self.w = w 
        self.h = h
        #initialize display
        self.display  = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

    #initial game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-B_size, self.head.y), Point(self.head.x-(2*B_size), self.head.y)]

        self.speed = 12
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(0, (self.w-B_size)//B_size)*B_size
        y = random.randint(0, (self.h-B_size)//B_size)*B_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        #1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP                
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        #2. move 

        self._move(self.direction)
        self.snake.insert(0, self.head)

        #3. check if game is over
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #4. place food or just move

        if self.head == self.food:
            self.score += math.floor(1 + 0.05*self.score)
            self._place_food()
            self.speed += 0.1
        else:
            self.snake.pop()

        #5. update ui and clock 
        self._update_ui()
        self.clock.tick(self.speed) 

        #6. return game over and the score for the person
        game_over = False
        return game_over, self.score


    def _is_collision(self):
        if self.head in self.snake[2:]:
            return True

    def _update_ui(self):
        self.display.fill(W)

        for pt in self.snake:
            pygame.draw.rect(self.display, B1, pygame.Rect(pt.x, pt.y, B_size, B_size))
            pygame.draw.rect(self.display, B2, pygame.Rect(pt.x+2, pt.y+2, 16,16))
    
        pygame.draw.rect(self.display, R, pygame.Rect(self.food.x, self.food.y, B_size, B_size))

        # text = font.render('Score: ' + str(self.score), True, BL)
        # self.display.blit("test", [0,0])
        print(str(self.score))
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x % self.w
        y = self.head.y % self.h

        if direction == Direction.RIGHT:
            x += B_size
        elif direction == Direction.LEFT:
            x -= B_size
        elif direction == Direction.UP:
            y -= B_size
        elif direction == Direction.DOWN:
            y += B_size

        self.head = Point(x,y)

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()
        if game_over == True:
            break

    print('Final Score: ', score)
    pygame.quit()