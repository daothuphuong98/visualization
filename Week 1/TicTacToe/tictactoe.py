import pygame
import numpy as np

SCREEN_HEIGHT = 700
WIDTH = 600
BOARD_HEIGHT = 600
LINE_WIDTH = 15
SQUARE_SIZE = 200

COLOR_4 = (236,224,209)
COLOR_2 = (219,193,172)
COLOR_1 = (150,114,89)
COLOR_3 = (99,72,50)

class ScoreBoard:
    def __init__(self):
        self.score_board = pygame.Rect((0, SQUARE_SIZE * 3, WIDTH, SQUARE_SIZE))
        self.small_font = pygame.font.Font('LEMONMILK-Medium.otf', 30)
        self.smaller_font = pygame.font.Font('LEMONMILK-Medium.otf', 15)

    def draw_score(self, screen, player_list):
        pygame.draw.rect(screen, COLOR_2, self.score_board)
        player_score = [self.small_font.render(f'{player.score}', True, COLOR_3, COLOR_2) for player in player_list]
        player_score_rect = [player_score[i].get_rect(midtop=(SQUARE_SIZE*(0.5 + 2*i), SQUARE_SIZE*3.1)) for i in range(2)]
        for i in range(2):
            screen.blit(player_score[i], player_score_rect[i])

    def draw_winner(self, screen, winner):
        if winner:
            message = self.small_font.render(f'{winner.tag.upper()} wins', False, COLOR_3, COLOR_2)
        else:
            message = self.small_font.render(f'DRAW', True, COLOR_3, COLOR_2)
        message_rect = message.get_rect(midtop=(WIDTH / 2, SQUARE_SIZE * 3.1))
        replay = self.smaller_font.render('Press any key to restart', False, COLOR_3, COLOR_2)
        replay_rect = replay.get_rect(midtop=(WIDTH / 2, SQUARE_SIZE * 3.36))
        screen.blit(message, message_rect)
        screen.blit(replay, replay_rect)

class Board:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.font = pygame.font.Font('consola.ttf', 150)
        self.x = self.font.render('\u00D7', False, COLOR_3, COLOR_1)
        self.o = self.font.render('\u25CB', False, COLOR_4, COLOR_1)

    def empty_square(self, row, col):
        return self.board[row, col] == 0

    def check_square(self, row, col, player):
        self.board[row, col] = player.num

    def draw(self, screen):
        pygame.draw.line(screen, COLOR_2, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, COLOR_2, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, COLOR_2, (SQUARE_SIZE, 0), (SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, COLOR_2, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)

        for row in range(3):
            for col in range(3):
                if self.board[row, col] == 1:
                    x_rect = self.x.get_rect(center=(SQUARE_SIZE * (row+0.5), SQUARE_SIZE * (col+0.5)))
                    screen.blit(self.x, x_rect)
                if self.board[row, col] == 2:
                    o_rect = self.x.get_rect(center=(SQUARE_SIZE * (row+0.5), SQUARE_SIZE * (col+0.5)))
                    screen.blit(self.o, o_rect)

    def check_win(self, player):
        for row in range(3):
            if np.all(self.board[row] == player.num):
                return True

        trans_board = self.board.T
        for row in range(3):
            if np.all(trans_board[row] == player.num):
                return True

        return (self.board[2,0] == player.num and self.board[1,1] == player.num and self.board[0,2] == player.num) \
               or (self.board[0,0] == player.num and self.board[1,1] == player.num and self.board[2,2] == player.num)

    def check_draw(self):
        return np.count_nonzero(self.board) == self.board.size

class Player:
    def __init__(self, num):
        self.score = 0
        self.num = num
        if num == 1:
            self.tag = 'Left'
        else:
            self.tag = 'Right'

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(COLOR_1)
        self.running = True
        self.quit = False

        self.players = [Player(1), Player(2)]
        self.winner = None
        self.first_player = 0

        self.score_board = ScoreBoard()

    def new_game(self):
        self.running = True
        self.screen.fill(COLOR_1)
        self.board = Board()
        self.winner = None
        self.player_ind = self.first_player

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    self.running = True
                    waiting = False

    def run(self):
        self.new_game()
        while self.running:

            self.clock.tick(17)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:

                    x_pos = event.pos[0]
                    y_pos = event.pos[1]

                    row_click = int(x_pos // SQUARE_SIZE)
                    col_click = int(y_pos // SQUARE_SIZE)

                    if self.board.empty_square(row_click, col_click):

                        self.board.check_square(row_click, col_click, self.players[self.player_ind])
                        if self.board.check_win(self.players[self.player_ind]):
                            self.winner = self.players[self.player_ind]
                            self.winner.score += 1
                            self.running = False
                        if self.board.check_draw():
                            self.running = False
                        self.player_ind = (self.player_ind + 1) % 2
            self.board.draw(self.screen)
            self.score_board.draw_score(self.screen, self.players)
            pygame.display.update()

    def end(self):
        if self.quit:
            return
        self.score_board.draw_winner(self.screen, self.winner)
        self.first_player = (self.first_player + 1) % 2
        pygame.display.update()
        self.wait_for_key()

if __name__ == '__main__':
    pygame.init()
    g = Game()
    while g.running:
        g.run()
        g.end()
    pygame.quit()