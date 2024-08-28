import pygame

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

		# Set up the game variables
		self.ball_radius = 8
		self.ball_speed = 5
		self.paddle_width = 10
		self.paddle_height = 100
		self.paddle_speed = 5

		# Initialize scores
		self.player1_score = 0
		self.player2_score = 0

		# Set up the font for displaying scores
		self.font = pygame.font.Font(None, 74)

		# Reset the game state
		self.reset()

		self.running = True

	def reset(self):
		self.ball_x = self.screen_width // 2
		self.ball_y = self.screen_height // 2
		self.ball_dx = self.ball_speed
		self.ball_dy = self.ball_speed

		self.paddle1_x = 10
		self.paddle1_y = self.screen_height // 2 - self.paddle_height // 2
		self.paddle1_dy = 0

		self.paddle2_x = self.screen_width - 10 - self.paddle_width
		self.paddle2_y = self.screen_height // 2 - self.paddle_height // 2
		self.paddle2_dy = 0
		
	def training_reset(self):
		self.reset()
		self.player1_score = 0
		self.player2_score = 0

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				
	def paddle_follow_ball(self):
		if self.ball_y < self.paddle2_y + self.paddle_height // 2:
			self.paddle2_dy = -self.paddle_speed
		else:
			self.paddle2_dy = self.paddle_speed

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
		if self.ball_x - self.ball_radius <= self.paddle1_x + self.paddle_width and self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_height:
			self.ball_dx = -self.ball_dx
		if self.ball_x + self.ball_radius >= self.paddle2_x and self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_height:
			self.ball_dx = -self.ball_dx

		# Check for collision with the left and right walls
		if self.ball_x - self.ball_radius <= 0:
			self.player2_score += 1
			self.reset()
		if self.ball_x + self.ball_radius >= self.screen_width:
			self.player1_score += 1
			self.reset()

		# Check for collision with the top and bottom walls
		if self.paddle1_y <= 0:
			self.paddle1_y = 0
		if self.paddle1_y + self.paddle_height >= self.screen_height:
			self.paddle1_y = self.screen_height - self.paddle_height
		if self.paddle2_y <= 0:
			self.paddle2_y = 0
		if self.paddle2_y + self.paddle_height >= self.screen_height:
			self.paddle2_y = self.screen_height - self.paddle_height

	def render(self):
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

		# Update the display
		pygame.display.update()

	def run(self):
		while self.running:
			self.handle_events()
			self.update()
			self.render()
			self.paddle_follow_ball()
			self.clock.tick(60)
		pygame.quit()

if __name__ == "__main__":
	game = PongGame()
	game.run()