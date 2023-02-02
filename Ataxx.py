from tkinter import *
import numpy as np

b_w="""
  ___ _                   _           _ _ _
 | _ ) |_  _ ___  __ __ _(_)_ _  ___ | | | |
 | _ \ | || / -_) \ V  V / | ' \(_-< |_|_|_|
 |___/_|\_,_\___|  \_/\_/|_|_||_/__/ (_|_|_)

"""

r_w="""
  ___        _          _           _ _ _
 | _ \___ __| | __ __ _(_)_ _  ___ | | | |
 |   / -_) _` | \ V  V / | ' \(_-< |_|_|_|
 |_|_\___\__,_|  \_/\_/|_|_||_/__/ (_|_|_)

"""



NB = 3  # Board number of rows/columns
size_of_board = 600
size_of_square = size_of_board/NB
symbol_size = (size_of_square*0.75-10)/2
symbol_thickness = 20
blue_color = '#496BAB'
#0492CF
red_color = '#F33E30'
#EE4035
possible_moves_global=[]
position_global=[]
bool=False
origin_pos=[]

class ataxx():
    def __init__(self):
        self.window = Tk()
        self.window.title('Ataxx')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, background="white")
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.init_draw_board()
        self.board = np.zeros(shape=(NB, NB))
        self.board[0][0]=2
        self.board[0][NB-1]=1
        self.board[NB-1][NB-1]=1
        self.board[NB-1][0]=2
        self.player_blue_turn = True
        self.game_ended = False


    def mainloop(self):
        self.window.mainloop()


    #----------------DESENHO DO TABULEIRO---------------------------------------------------------------------------------------------------------

    def init_draw_board(self):
        self.canvas.delete("all")
        for i in range(NB-1):
            self.canvas.create_line((i+1)*size_of_square, 0, (i+1)*size_of_square, size_of_board)
        for i in range(NB-1):
            self.canvas.create_line(0,(i+1)*size_of_square, size_of_board, (i+1)*size_of_square)
        self.canvas.create_oval(size_of_square/2 - symbol_size, size_of_square/2 - symbol_size,
                                size_of_square/2 + symbol_size, size_of_square/2 + symbol_size,
                                width=symbol_thickness, outline=red_color,
                                fill=red_color)
        self.canvas.create_oval(size_of_board - size_of_square/2 - symbol_size,size_of_board - size_of_square/2 - symbol_size,
                                size_of_board - size_of_square/2 + symbol_size, size_of_board - size_of_square/2 + symbol_size,
                                width=symbol_thickness, outline=blue_color,
                                fill=blue_color)
        self.canvas.create_oval(size_of_square/2 - symbol_size,size_of_board - size_of_square/2 - symbol_size,
                                size_of_square/2 + symbol_size, size_of_board - size_of_square/2 + symbol_size,
                                width=symbol_thickness, outline=blue_color,
                                fill=blue_color)
        self.canvas.create_oval(size_of_board - size_of_square/2 - symbol_size, size_of_square/2- symbol_size,
                                size_of_board - size_of_square/2 + symbol_size, size_of_square/2 + symbol_size,
                                width=symbol_thickness, outline=red_color,
                                fill=red_color)

    def update_board(self, x, y, origin):

        # após um movimento ser valido pelo jogo, a funcao dá
        # update à matriz que representa o tabuleiro, transformando
        # qualquer quadrado adjacente ao quadrado de destino que
        # esteja ocupado para a cor do jogador.
        # se a peça "saltar", chama a funcao draw_whitespace para desenhar
        # um quadrado branco no local de origem da peça e mete essa posicao
        # na board a 0, "apagando" a peça

        for i in range(max(0, x-1), min(NB, x+2)):
            for j in range(max(0, y-1), min(NB, y+2)):
                if not self.is_square_clear([i,j]):
                    if self.player_blue_turn:
                        self.draw_blue([i,j])
                    else:
                        self.draw_red([i,j])
                    self.board[i][j]=self.board[x][y]
        if x-origin[0]== 2 or y-origin[1]== 2 or x-origin[0]== -2 or y-origin[1]== -2:
            self.board[origin[0]][origin[1]]=0
            pos=self.convert_logical_to_grid_position(origin)
            self.draw_whitespace(pos)
        self.player_blue_turn = not self.player_blue_turn
        self.score()



    def execute_move(self, move, origin, player):

        # altera na board o destino da peca que foi jogado para o valor
        # correspondente dessa peca(1 se azul, 2 se vermelho)
        # chama a funcao update_board para completar a execucao do movimento

        self.board[move[0]][move[1]] = player
        self.update_board(move[0], move[1], origin)

    def is_square_clear(self, pos):
        #print(pos)
        if not np.array_equal(pos, []):
            return self.board[pos[0]][pos[1]] == 0

    def valid_move(self, logical_pos):
        return self.is_square_clear(logical_pos)

    def possible_moves(self, move):

        # dado uma certa peça que foi seleciona, devolve uma lista
        # com todos os movimentos possiveis dessa peça

        possible_moves=[]
        for i in range(max(0,move[0]-2), min(NB, move[0]+3)):
            for j in range(max(0,move[1]-2), min(NB, move[1]+3)):
                #print(i, j)
                #print(self.is_square_clear([i,j]))
                if self.is_square_clear([i,j]):
                    possible_moves.append([i,j])
        #print(possible_moves)
        return possible_moves

    def score(self):
        cont_blue=0
        cont_red=0
        cheio=True
        for i in range(NB):
            for j in range(NB):
                if self.board[i][j]==1:
                    cont_blue+=1
                elif self.board[i][j]==2:
                    cont_red+=1
                if self.board[i][j]==0:
                    cheio=False
        if cont_blue==0:
            self.game_is_over(cont_red, cont_blue)
        elif cont_red==0:
            self.game_is_over(cont_red, cont_blue)
        elif cheio:
            self.game_is_over(cont_red, cont_blue)

        print("Blue score= ",  cont_blue)
        print("Red score= ",  cont_red)
        print("------------------------")

    def game_is_over(self, red, blue):
        print("Blue score= ",  blue)
        print("Red score= ",  red)
        print("")
        if blue>red:
            print(b_w)
            print("De volta ao menu")
        else:
            print(r_w)
        print("")
        self.clear_possible_moves()
        self.window.destroy()
        start_menu()




#----------------------TRANSFORMAR EM MATRIZ PARA APLICAR REGRAS-------------------------------------------------------------------------------
# Drawing Functions:
# The modules required to draw required game based object on canvas
# logical_position = grid value on the board
# grid_position = actual pixel values of the center of the grid

    def convert_logical_to_grid_position(self, logical_pos):
        logical_pos = np.array(logical_pos, dtype=int)
        return np.array((size_of_square)*logical_pos + size_of_square/2)

    def convert_grid_to_logical_position(self, grid_pos):
        grid_pos = np.array(grid_pos)
        return np.array(grid_pos//size_of_square, dtype=int)

#-----------------------DESENHAR PECAS----------------------------------------
    def draw_whitespace(self, grid_pos):

        # desenha o quadrado branco no local dado

        self.canvas.create_rectangle(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                            grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                            width=symbol_thickness, outline="white",
                            fill="white")


    def draw_blue(self, logical_pos):
        logical_pos = np.array(logical_pos)
        grid_pos = self.convert_logical_to_grid_position(logical_pos)
        self.canvas.create_oval(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                            grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                            width=symbol_thickness, outline=blue_color,
                            fill=blue_color)

    def draw_red(self, logical_pos):
        logical_pos = np.array(logical_pos)
        grid_pos = self.convert_logical_to_grid_position(logical_pos)
        self.canvas.create_oval(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                            grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                            width=symbol_thickness, outline=red_color,
                            fill=red_color)

    def draw_possible_moves(self, possible_moves):

        # desenha no ecrâ todos os moves possiveis de uma
        # determinada peça, utilizando circulos cinzentos para
        # representar os moves possiveis

        moves=[0]*len(possible_moves)
        for i in range(len(possible_moves)):
            moves[i]=self.convert_logical_to_grid_position(possible_moves[i])
            self.canvas.create_oval(moves[i][0]-symbol_size, moves[i][1] - symbol_size,
                                    moves[i][0]+symbol_size, moves[i][1]+ symbol_size,
                                    width=symbol_thickness, outline="gray", fill="gray", tags="possible")


    def clear_possible_moves(self):

        # limpa do ecrã os moves possiveis(os circulos cinzentos)

        self.canvas.delete("possible")

#--------------------------MINIMAX----------------------------


    def click(self, event):

        # ao clicar pela primeira vez numa peça,
        # altera o bind do Button 1 para second_click,
        # funcao que regista o segundo click do jogador
        # se a peça que foi clicada for uma peça de um jogador,
        # chama as funçoes possible_moves e draw_possible_moves
        # para mostrar no ecra os moves possiveis dessa peça

        if self.game_ended: return
        grid_pos = [event.x, event.y]
        logical_pos = self.convert_grid_to_logical_position(grid_pos)
        global origin_pos
        origin_pos = logical_pos
        if self.player_blue_turn:
            player=1
        else:
            player=2
        if self.board[logical_pos[0]][logical_pos[1]] == 1 or self.board[logical_pos[0]][logical_pos[1]] == 2:
            self.window.bind("<Button-1>", self.second_click)
            global possible_moves_global
            possible_moves_global = self.possible_moves(logical_pos)
            self.draw_possible_moves(possible_moves_global)


    def second_click(self, event):

        #ao clicarmos uma segunda vez no ecrã, esta função
        # é executada. Regista a posição do click e compara
        # se o local onde clicamos faz parte da lista dos possible_moves.
        #Se True, chama a função click2.

        global bool
        grid_pos = [event.x, event.y]
        logical_pos = self.convert_grid_to_logical_position(grid_pos)
        global possible_moves_global
        possible_moves_global=np.array(possible_moves_global, dtype=int)
        for element in possible_moves_global:
            #print(element)
            #print(np.array_equal(logical_pos, element))
            if np.array_equal(logical_pos, element):
                global position_global
                position_global = logical_pos
                bool=True
        bool = True
        self.click2()
        possible_moves_global=[]
        position_global=[]


    def click2(self):

        # Dado que o segundo click aconteceu, e fazemos
        # isto com recurso à função second_click_pressed,
        # a função verifica se o move é valido(kinda já fizemos
        # isto mais atras no codigo, mas isto é antes de ter feito
        # alterações então nao sei se se tirar isto fode-se tudo) e se for,
        # consoante o jogador que está a jogar, ele vai desenhar no ecrã
        # uma peça vermelha ou uma peça azul chamando as funcoes draw_blue or draw_red.
        #Por fim, chama a função execute_move e no fim, a função clear_possible_moves

        global bool
        if self.player_blue_turn:
            player=1
        else:
            player=2
        if self.valid_move(position_global):
            if self.second_click_pressed(bool):
                if self.player_blue_turn and self.board[origin_pos[0]][origin_pos[1]] == 1:
                    self.draw_blue(position_global)
                    self.execute_move(position_global, origin_pos, player)
                elif not self.player_blue_turn and self.board[origin_pos[0]][origin_pos[1]] == 2:
                    self.draw_red(position_global)
                    self.execute_move(position_global, origin_pos, player)
        self.clear_possible_moves()
        self.window.bind("<Button-1>", self.click)

    def second_click_pressed(self, bool):

        # após ter sido executado o segundo click,
        # esta função vai alterar novamente o bind
        # do Button-1 para self.click e retorna um valor de True.
        # Caso contratrio, retorna um False.

        if bool:
            return True
        return False

def PvsP():
    game = ataxx()
    game.mainloop()
    start_menu()


def PvsAI():
    print("COMING SOON!!!!!")
    print("")
    start_menu()

def AIvsAI():
    print("COMING SOON!!!!!")
    print("")
    start_menu()



def start_menu():
    print("")
    print("|-----------------------------------------------------------|")
    print("|      ___   .__________.     ___      ___   ___ ___   ___  |")
    print("|     /   \  |           |   /   \     \  \ /  / \  \ /  /  |")
    print("|    /  ^  \ `---|  |---`   /  ^  \     \  V  /   \  V  /   |")
    print("|   /  /_\  \    |  |      /  /_\  \     >   <     >   <    |")
    print("|  /  _____  \   |  |     /  _____  \   /  .  \   /  .  \   |")
    print("| /__/     \__\  |__|    /__/     \__\ /__/ \__\ /__/ \__\  |")
    print("|-----------------------------------------------------------|")
    print("")
    print("")
    print("Escolha uma das seguintes opções:")
    print("")
    print("(1) Player contra player")
    print("(2) Player contra AI")
    print("(3) AI contra AI")
    print("(4) Sair")
    print("")
    escolha=input("Opção: ")
    print("")

    while(escolha!="1" or escolha!="2" or escolha!="3" or escolha!="4"):
        if escolha=="1":
            print("--------------------------------------")
            print("")
            print("Opção player contra player selecionada")
            print("")
            PvsP()
            break

        elif escolha=="2":
            print("----------------------------------")
            print("")
            print("Opção player contra AI selecionada")
            print("")
            PvsAI()
            break

        elif escolha=="3":
            print("----------------------------------")
            print("")
            print("Opção AI contra AI selecionada")
            print("")
            AIvsAI()
            break
        elif escolha=="4":
            quit()
        else:
            print("------------------------------------------------------------")
            print("")
            print("-Opção inválida")
            print("")
            print("|-----------------------------------------------------------|")
            print("|      ___   .__________.     ___      ___   ___ ___   ___  |")
            print("|     /   \  |           |   /   \     \  \ /  / \  \ /  /  |")
            print("|    /  ^  \ `---|  |---`   /  ^  \     \  V  /   \  V  /   |")
            print("|   /  /_\  \    |  |      /  /_\  \     >   <     >   <    |")
            print("|  /  _____  \   |  |     /  _____  \   /  .  \   /  .  \   |")
            print("| /__/     \__\  |__|    /__/     \__\ /__/ \__\ /__/ \__\  |")
            print("|-----------------------------------------------------------|")
            print("")
            print("")
            print("Escolha uma das seguintes opções:")
            print("")
            print("(1) Player contra player")
            print("(2) Player contra AI")
            print("(3) AI contra AI")
            print("(4) Sair")
            print("")
            escolha=input("Opção: ")
            print("")



start_menu()
