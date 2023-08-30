import pygame


pygame.init() # ca sa nu importam noi manual
pygame.font.init() # ca sa inceapa fonturile

windows_size=(450,500) # marimea ferestrei
cell_size=150 # marimea patratelor

screen=pygame.display.set_mode(windows_size)
pygame.display.set_caption("Tic Tac Toe") # titlul ferestrei de se deschide

class TicTacToe():


    def __init__(self,table_size): # functie pentru initializare , o regasim la inceput de clasa
        self.table_size=table_size    # self e folosit pt obiectul curent
        self.cell_size=table_size//3 # pt ca avem 3x3 matricea pt joc
        self.table_space=20 # dimensiunea tabelei comparativ cu display ul
        self.table=[]
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")


        self.player="X"
        self.winner=None
        self.taking_move=True # se va muta atata timp cat nu exista castigator
        self.running=True #atata timp cat nu inchidem fereastra

        self.background_color=(255, 174, 66)
        self.table_color=(100,100,100) # culoarea chenarului
        self.line_color=(0,0,0,) # linia care taie
        self.instructions_color=(50,50,50)
        self.game_over_bg_color = (100,100,100)
        self.game_over_color= (230, 255, 255)
        self.font = pygame.font.SysFont("Times New Roman", 30)
        self.FPS = pygame.time.Clock()
     # aici mai sus am folosit tehnica RGB pentru a colora jocul

    def _draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        r1 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[0]],
                              [tb_space_point[1], cell_space_point[0]], 8)
        c1 = pygame.draw.line(screen, self.table_color, [cell_space_point[0], tb_space_point[0]],
                              [cell_space_point[0], tb_space_point[1]], 8)
        r2 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[1]],
                              [tb_space_point[1], cell_space_point[1]], 8)
        c2 = pygame.draw.line(screen, self.table_color, [cell_space_point[1], tb_space_point[0]],
                              [cell_space_point[1], tb_space_point[1]], 8)
        # tb_space_point[0]  pentru stanga si sus tb_space_point[1] pt jos si dreapta
        # toate au latimea de 8

    def _change_player(self):
        self.player="0" if self.player=="X" else "X"
        # daca e jucatorul x il schimba in 0 si invers

    def _move(self,pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            # pos = pozitia jucatorului pe tablita
            if self.table[x][y]=="-":
                self.table[x][y]=self.player
                self._draw_char(x,y,self.player) #ii pune semnul
                self._game_check() # sa vedem daca s a terminat
                self._change_player() # schimbam player ul
        except:
            print("Click inside the table only")

    # draws character of the recent player to the selected table cell
    def _draw_char(self, x, y, player):
        if self.player == "0":
            img = pygame.image.load("images/0.png")
        elif self.player == "X":
            img = pygame.image.load("images/X-ul.png")
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        screen.blit(img, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        # in randurile astea , se scaleaza imaginea in casuta
        # blit iti deseneaza in ecran

    # instructions and game-state messages

    def _message(self):
        if self.winner is not None:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35))
            msg = self.font.render(f'{self.winner} WINS!!', True, self.game_over_color) # ce sa scrie si in ce sa scrie
            screen.blit(msg, (165, 445)) #lungimea si inaltimea scrisului
        elif not self.taking_move:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35))
            instructions = self.font.render('DRAW!!', True, self.game_over_color)
            screen.blit(instructions, (170, 445))
        else:
            screen.fill(self.background_color, (135, 445, 188, 35))
            instructions = self.font.render(f'{self.player} to move', True, self.instructions_color)
            screen.blit(instructions, (160, 445))

    def _game_check(self):
        # vertical check
        for x_index, col in enumerate(self.table): #x_index e contorul folosit de enumerate
            win = True
            pattern_list = []
            for y_index, content in enumerate(col):
                if content != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))
            if win == True:
                self._pattern_strike(pattern_list[0],pattern_list[-1],"ver")
                self.winner = self.player
                self.taking_move = False
                self._message()
                break

        # horizontal check
        for row in range(len(self.table)):
            win = True
            pattern_list = []
            for col in range(len(self.table)):
                if self.table[col][row] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((col, row))
            if win == True:
                self._pattern_strike(pattern_list[0],pattern_list[-1],"hor")
                self.winner = self.player
                self.taking_move = False
                self._message()
                break

        # left diagonal check
        for index, row in enumerate(self.table):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self._pattern_strike((0,0),(2,2),"left-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()

        # right diagonal check
        for index, row in enumerate(self.table[::-1]):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self._pattern_strike((2,0),(0,2),"right-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()

        # blank table cells check
        blank_cells = 0
        for row in self.table:
            for cell in row:
                if cell == "-":
                    blank_cells += 1
        if blank_cells == 0:
            self.taking_move = False
            self._message()

    # strikes a line to winning patterns if already has
    def _pattern_strike(self, start_point, end_point, line_type):
        # gets the middle value of the cell
        mid_val = self.cell_size // 2

        # for the vertical winning pattern
        if line_type == "ver":
            start_x, start_y = start_point[0] * self.cell_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cell_size + mid_val, self.table_size - self.table_space

        # for the horizontal winning pattern
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[-1] * self.cell_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[-1] * self.cell_size + mid_val

        # for the diagonal winning pattern from top-left to bottom right
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space

        # for the diagonal winning pattern from top-right to bottom-left
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        # draws the line strike
        line_strike = pygame.draw.line(screen, self.line_color, [start_x, start_y], [end_x, end_y], 8)
    def main(self): # functia main gen int main
        screen.fill(self.background_color)
        self._draw_table()

        while self.running:
            self._message()
            for self.event in pygame.event.get():
                if self.event.type==pygame.QUIT: # daca se cere inchiderea jocului
                    self.running=False

                if self.event.type==pygame.MOUSEBUTTONDOWN:
                    if self.taking_move:
                        self._move(self.event.pos)

            pygame.display.flip() # ne da update la lucruri oe ecran
            self.FPS.tick(60) # sa jucam doar 60 de secunde

if __name__ == "__main__":
    g = TicTacToe(windows_size[0]) # o singura fereastra
    g.main()




