import pygame
import random
import time
import numpy as np

class PongGame:
    def __init__(self):
        pygame.init()

        # Set up the display
        self.screen_width = 800
        self.screen_height = 500
        self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong Game Environment")

        # Set up the colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Set up the game clock
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Set up the game variables
        self.ball_radius = 8
        self.ball_speed = 8
        self.paddle_width = 10
        self.paddle_height = 100
        self.paddle_speed = 8
  
        self.ball_direction = 1

        # Initialize scores
        self.player1_score = 0
        self.player2_score = 0

        # Set up the font for displaying scores
        self.font = pygame.font.Font(None, 74)

        self.reset()
        self.need_pause = True

        self.running = True
  
        self.skip_frames = 0
  
        self.current_ai_key_pressed = None

    def new_point(self):
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2
        self.ball_dx = self.ball_speed * self.ball_direction
        self.ball_dy = self.ball_speed * random.choice([-1, 1])
        self.current_ai_key_pressed = None
  
        # Change the serving direction of the ball
        self.ball_direction *= -1
  
        self.need_pause = True
        
    def reset(self):
        self.new_point()
        self.ball_direction = 1
        self.player1_score = 0
        self.player2_score = 0
        self.paddle1_x = 10
        self.paddle1_y = self.screen_height // 2 - self.paddle_height // 2
        self.paddle1_dy = 0

        self.paddle2_x = self.screen_width - 10 - self.paddle_width
        self.paddle2_y = self.screen_height // 2 - self.paddle_height // 2
        self.paddle2_dy = 0
        return self.get_state()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.current_ai_key_pressed == pygame.K_UP:
            self.paddle1_dy = -self.paddle_speed
        elif self.current_ai_key_pressed == pygame.K_DOWN:
            self.paddle1_dy = self.paddle_speed
                
    def paddle1_follow_ball(self):
        if self.ball_y < self.paddle1_y + self.paddle_height // 2:
            self.current_ai_key_pressed = pygame.K_UP
        elif self.ball_y > self.paddle1_y + self.paddle_height // 2:
            self.current_ai_key_pressed = pygame.K_DOWN
        else:
            self.current_ai_key_pressed = None
            
    def step(self, action):
        if action == 0:
            self.paddle2_dy = -self.paddle_speed
        elif action == 1:
            self.paddle2_dy = self.paddle_speed
        else:
            self.paddle2_dy = 0
        self.paddle1_follow_ball()
        self.update()
        # self.render()
        return self.get_state(), self.get_reward(), self.is_done()

    def update(self):
        # Update the ball's position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Update the paddles' position
        self.paddle1_y += self.paddle1_dy
        self.paddle2_y += self.paddle2_dy

        # Check for collision with the top and bottom walls
        if self.ball_y - self.ball_radius <= 0 or self.ball_y + self.ball_radius >= self.screen_height:
            self.ball_dy = -self.ball_dy

        # Check for collision with the paddles
        if self.ball_x - self.ball_radius <= self.paddle1_x + self.paddle_width:
            if self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_height:
                self.ball_dx = -self.ball_dx
                self.ball_x = self.paddle1_x + self.paddle_width + self.ball_radius  # Move ball outside the paddle

        if self.ball_x + self.ball_radius >= self.paddle2_x:
            if self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_height:
                self.ball_dx = -self.ball_dx
                self.ball_x = self.paddle2_x - self.ball_radius  # Move ball outside the paddle

        # Check for collision with the left and right walls
        if self.ball_x - self.ball_radius <= 0:
            self.player2_score += 1
            self.new_point()
        if self.ball_x + self.ball_radius >= self.screen_width:
            self.player1_score += 1
            self.new_point()

        # Check for collision with the top and bottom walls
        if self.paddle1_y <= 0:
            self.paddle1_y = 0
        if self.paddle1_y + self.paddle_height >= self.screen_height:
            self.paddle1_y = self.screen_height - self.paddle_height
        if self.paddle2_y <= 0:
            self.paddle2_y = 0
        if self.paddle2_y + self.paddle_height >= self.screen_height:
            self.paddle2_y = self.screen_height - self.paddle_height
            
    def get_reward(self):
        reward = 0

        # Check if player 1 (the trainer) scored a point
        if self.ball_x + self.ball_radius >= self.screen_width:
            reward = -1

        # Check if player 2 (the agent) scored a point
        elif self.ball_x - self.ball_radius <= 0:
            reward = 1

        # Check if the ball hit the paddle
        elif (self.ball_dx < 0 and self.paddle1_x <= self.ball_x <= self.paddle1_x + self.paddle_width and
            self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_height) or \
            (self.ball_dx > 0 and self.paddle2_x <= self.ball_x <= self.paddle2_x + self.paddle_width and
            self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_height):
            reward = 0.1

        return reward

    def render(self, episode = None):
        # Fill the screen with black color
        self.win.fill(self.BLACK)

        # Draw the ball
        pygame.draw.circle(self.win, self.WHITE, (self.ball_x, self.ball_y), self.ball_radius)

        # Draw the paddles
        pygame.draw.rect(self.win, self.WHITE, (self.paddle1_x, self.paddle1_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.win, self.WHITE, (self.paddle2_x, self.paddle2_y, self.paddle_width, self.paddle_height))

        # Draw the scores
        player1_text = self.font.render(str(self.player1_score), True, self.WHITE)
        player2_text = self.font.render(str(self.player2_score), True, self.WHITE)
        self.win.blit(player1_text, (self.screen_width // 4, 10))
        self.win.blit(player2_text, (self.screen_width * 3 // 4, 10))
        
        if episode is not None:
            small_font = pygame.font.Font(None, 24)
            episode_text = small_font.render(f'Episode: {episode}', True, (255, 255, 255))
            self.win.blit(episode_text, (10, 10))

        # Update the display
        pygame.display.flip()
  
        # if self.need_pause:
        #     time.sleep(1)
        #     self.need_pause = False
    
    def is_done(self):
        return self.player1_score >= 5 or self.player2_score >= 5
            
    def get_state(self):
        return np.array([self.paddle1_y, self.ball_x, self.ball_y, self.ball_dx, self.ball_dy])

    # def run(self, get_ai_action: callable):
    #     skip_frames = self.skip_frames
    #     while self.running:
    #         self.paddle1_follow_ball()
    #         self.handle_events()
    #         action = get_ai_action(self.get_state())
    #         self.step(action)
    #         if skip_frames == 0 or self.need_pause:
    #             self.render()
    #             skip_frames = self.skip_frames
    #         else:
    #             skip_frames -= 1
    #         self.clock.tick(60)
    #     pygame.quit()