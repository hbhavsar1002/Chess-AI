'''
Name: Harsh Hirenkumar Bhavsar
'''

# This is where you build your AI for the Chess game.
# All the required packages
from joueur.base_ai import BaseAI
import random, copy,time, math

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "CaramelizedOnions" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    #BEGIN of custom code
    # Function to check if the position of piece is valid 
    def is_valid_pos(self, i: int, j: int, n: int, m: int) -> bool:
    
        if i < 0 or j < 0 or i > n - 1 or j > m - 1:
            return False
        return True

    # Function to convert FEN string into a 2D array 
    def fen_to_array(self, fen: str):
    
        fen_parts = fen.split(' ')
        board_str = fen_parts[0].split('/')
        
        board_arr = [[] for a in range(8)]
        for i, row in enumerate(board_str):
            j = 0
            for char in row:
                if char.isdigit():
                    board_arr[i].extend([' '] * int(char))
                else:
                    board_arr[i].append(char)
                    j += 1
        return board_arr
        
    
    # Function to convert the moves into UCI format
    def uci_format(self,row,col,new_row,new_col):
        uci_col = ['a','b','c','d','e','f','g','h']
        
        b = 'black'
        w = 'white'
        
        row = 8 - row
        new_row = 8 - new_row
        
        uci_format = uci_col[col] + str(row) + uci_col[new_col] + str(new_row)
        return uci_format
    
    # Function to make valid next move 
    def make_next_move(self, random_piece, offset, row, col,possible_moves, color,board, king_row, king_col):
    
        w_alphabets = 'BKNPQR'
        b_alphabets = 'bknpqr'
    
        
        b = 'black'
        w = 'white'
        
        for pos_ in offset:
                            
            pos_row,pos_col = pos_[0],pos_[1]
            
            new_row = row + pos_row
            new_col = col + pos_col
        
                                        
            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                if (color == w and board[new_row][new_col] in w_alphabets) or (color == b and board[new_row][new_col] in b_alphabets):
                    continue
            else: 
                continue
    
                
            for x in range(1,8):
                
                new_row = row + (pos_row * x )
                new_col = col + (pos_col * x )
                
                if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                    
                    if (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets) or (board[new_row][new_col] == ' '):
                        
                        new_board = self.change_board(board,row,col,new_row,new_col, False)
                        next_move  = self.uci_format(row,col,new_row,new_col)
                        king_check = self.is_king_check(king_row, king_col, new_board, False )
                    
                        if not king_check:
                            
                            possible_moves.append(next_move)
                       
                            if board[new_row][new_col] == ' ':
                                continue
                            else: 
                                break
                    else:
                        break
        return possible_moves
        
    def is_king_check(self,row,col,board, get_pos):
        
        w = 'white'
        b = 'black'
        
        if self.player.color == w:
            alphabets = 'bknpqr'
        else:
            alphabets = 'BKNPQR'
        
        check_positions = []
        
        king_check = False
    
        piece = ' '
        
        piece_there = False
        
        for x in alphabets:
            if king_check:
                break

            if x == 'Q' or x == 'q':
                offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                
                for i in offset:
                    if king_check:                        
                        break
                        
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                        continue
                    
                    if (board[new_row][new_col] == 'q' and self.player.color == w) or (board[new_row][new_col] == 'Q' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
                    elif (board[new_row][new_col] != 'q' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'Q' and self.player.color == b and board[new_row][new_col] != ' '):
                        continue
                    
                    for y in range(1,8):
                        
                        new_row = row + (i[0] * y )
                        new_col = col + (i[1] * y )
                        
                        if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                        if (board[new_row][new_col] == 'q' and self.player.color == w) or (board[new_row][new_col] == 'Q' and self.player.color == b):
                            
                            check_positions.append((new_row,new_col))
                            king_check = True
                            piece = x
                            break
                        elif board[new_row][new_col] == ' ':
                            continue
                        elif (board[new_row][new_col] != 'q' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'Q' and self.player.color == b and board[new_row][new_col] != ' '):
                            break
                            
            
            if x == 'R' or x == 'r':
                offset = [(0,1),(1,0),(0,-1),(-1,0)]
                
                for i in offset:
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                    if (board[new_row][new_col] == 'r' and self.player.color == w) or (board[new_row][new_col] == 'R' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
                    elif (board[new_row][new_col] != 'r' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'R' and self.player.color == b and board[new_row][new_col] != ' '):
                            continue
                    
                    for y in range(1,8):
                        
                        new_row = row + (i[0] * y )
                        new_col = col + (i[1] * y )
                        
                        if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                            
                        
                        if (board[new_row][new_col] == 'r' and self.player.color == w) or (board[new_row][new_col] == 'R' and self.player.color == b):
                            check_positions.append((new_row,new_col))
                            king_check = True
                            piece = x
                            break
                        elif board[new_row][new_col] == ' ':
                            continue
                        elif (board[new_row][new_col] != 'r' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'R' and self.player.color == b and board[new_row][new_col] != ' '):
                            break
                            
                        
            if x == 'B' or x == 'b':
                offset = [(1,1),(1,-1),(-1,-1),(-1,1)]
                
                for i in offset:
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                    if (board[new_row][new_col] == 'b' and self.player.color == w) or (board[new_row][new_col] == 'B' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
                    elif (board[new_row][new_col] != 'b' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'B' and self.player.color == b and board[new_row][new_col] != ' '):
                            continue
                    
                    for y in range(1,8):
                        
                        new_row = row + (i[0] * y )
                        new_col = col + (i[1] * y )
                        
                        if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                        if (board[new_row][new_col] == 'b' and self.player.color == w) or (board[new_row][new_col] == 'B' and self.player.color == b):
                            check_positions.append((new_row,new_col))
                            king_check = True
                            piece = x
                            break
                        elif board[new_row][new_col] == ' ':
                            continue
                        elif (board[new_row][new_col] != 'b' and self.player.color == w and board[new_row][new_col] != ' ') or (board[new_row][new_col] != 'B' and self.player.color == b and board[new_row][new_col] != ' '):
                            break
                            
            if x == 'K' or x == 'k':
                offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                
                for i in offset:
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                    if (board[new_row][new_col] == 'k' and self.player.color == w) or (board[new_row][new_col] == 'K' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
                        
                        
            if x == 'N' or x == 'n':
                offset = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
                
                for i in offset:
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                    if (board[new_row][new_col] == 'n' and self.player.color == w) or (board[new_row][new_col] == 'N' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
            
            if x == 'p' or x == 'P':
                if x.islower():
                    offset = [(-1,1),(-1,-1)]
                else:
                    offset = [(1,-1),(1,1)]
                    
            
                for i in offset:
                    new_row =  row + i[0]
                    new_col =  col + i[1]
                    
                    if not self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            continue
                        
                    if (board[new_row][new_col] == 'p' and self.player.color == w) or (board[new_row][new_col] == 'P' and self.player.color == b):
                        check_positions.append((new_row,new_col))
                        king_check = True
                        piece = x
                        break
                        
        
        if get_pos:
        
            if king_check:
                return True, check_positions
            else: 
                return False, check_positions
        
        else:
        
            if king_check:
                return True
            else: 
                return False
                
    def heuristic_fucntion(self, board):
    
        heu_val = 0
        
        for i, line in enumerate(board):
            for j,k in enumerate(line):
                try:
                    if k == 'P' or k == 'p':
                        if k.isupper():
                            heu_val += 1
                        else: 
                            heu_val -= 1
                            
                    if k == 'K' or k == 'k':
                        if k.isupper():
                            heu_val += 90
                        else: 
                            heu_val -= 90
                            
                    if k == 'Q' or k == 'q':
                        if k.isupper():
                            heu_val += 9
                        else: 
                            heu_val -= 9
                    
                    if k == 'N' or k == 'n' or k == 'B' or k == 'b':
                        if k.isupper():
                            heu_val += 3
                        else: 
                            heu_val -= 3
                    
                    if k == 'R' or k == 'r':
                        if k.isupper():
                            heu_val += 5
                        else: 
                            heu_val -= 5
                                
                except ValueError:
                    continue
                    
        return heu_val
        
    def change_board(self,board,old_row,old_col,new_row,new_col, castle):
    
        board_upd = copy.deepcopy(board)
        
        if castle:
            
            temp = board_upd[new_row][new_col] 
            
            board_upd[new_row][new_col] = board_upd[old_row][old_col]
            
            board_upd[old_row][old_col] = temp
        else:
        
            board_upd[new_row][new_col] = board_upd[old_row][old_col]
            
            board_upd[old_row][old_col] = ' '
        
        return board_upd
        
        
    def get_legal_moves(self, board, color):
    
        # Initialize variables
        w_alphabets = 'KBNPQR'
        b_alphabets = 'kbnpqr'
        
        w_promo = 'BNQR'
        b_promo = 'bnqr'
        
        b = 'black'
        w = 'white'
        
        fen_parts = self.game.fen.split(' ')
        
        #print(board)
        
        #print(self.game.history)
        #print("FEN String",self.game.fen)
        #print("Color of my player",self.player.color)
        color =  self.player.color
        en_passant = False
        
        if color == w:
            alphabets = w_alphabets
        elif color == b:
            alphabets = b_alphabets
        
        king_row = 0
        king_col = 0 
        
        # Initialize Next Possible Moves variable
        possible_moves = []
        for random_piece in alphabets:
            king_check = False
            if any(random_piece in x for x in board):
                
                positions = []
                for i, line in enumerate(board):
                        for j,k in enumerate(line):
                            #try:
                                if k == random_piece:
                                    positions.append((i,j))
                            #except ValueError:
                                #continue
                
                #print("positions",random_piece,positions)
                
                if (random_piece == 'k' and color == b) or (random_piece == 'K' and color == w):
                    king_row = positions[0][0]
                    king_col = positions[0][1]
                # Process all the positions of the random piece
                for pos in positions:
                    
                    row = pos[0]
                    col = pos[1]
                    
                    #print("current piece pos",pos, random_piece)
                    
                    promotion = False
                    
                    #PAWN movements 
                    if random_piece == 'P' or random_piece == 'p':
                        
                        if color == w:
                            P_offset = [(-1,-1),(-1,1),(-1,0)]
                        else:
                            P_offset = [(1,-1),(1,1),(1,0)]
                        
                        
                        if color == w and row == 6:
                            if board[row-1][col] == ' ':
                                P_offset.append((-2,0))
                        elif (color == b and row == 1):
                            if board[row+1][col] == ' ':
                                P_offset.append((2,0))
                        # Code for Pawn promotion
                        elif (color == w and row == 1) or (color == b and row == 6):  
                            promotion = True
                        # Code for En Passant
                        if fen_parts[3] != '-':
                            en_passant = True
                    
                        for pos_ in P_offset:
                            
                            pos_row,pos_col = pos_[0],pos_[1]
                            
                            new_row = row + pos_row
                            new_col = col + pos_col
                            
                            king_check = False

                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                                # Diagonal direction
                                if pos_col == 1 or pos_col == -1:
                                    if board[new_row][new_col] == ' ':
                                    
                                        if en_passant:
                                            new_board = self.change_board(board,row,col,new_row,new_col, False)
                                            king_check = self.is_king_check(king_row, king_col, new_board, False )
                                            if not king_check:
                                                next_move  = self.uci_format(row,col,new_row,new_col)
                                                if fen_parts[3] == next_move[-2:]:
                                                    #print(next_move)
                                                    possible_moves.append(next_move)
                                        continue
                                    elif (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets):
                                        new_board = self.change_board(board,row,col,new_row,new_col, False)
                                        king_check = self.is_king_check(king_row, king_col, new_board, False )
                                        
                                        if not king_check:
                                            next_move  = self.uci_format(row,col,new_row,new_col)
                                            if promotion: # Code for Promotion
                                                if color == w:
                                                    promo = w_promo
                                                else:
                                                    promo = b_promo
                                                for x in promo:
                                                    next_move += x
                                                possible_moves.append(next_move)
                                            else:
                                                possible_moves.append(next_move)
                                # Vertical direction
                                else:
                                    
                                    if board[new_row][new_col] == ' ':
                                        new_board = self.change_board(board,row,col,new_row,new_col, False)
                                        king_check = self.is_king_check(king_row, king_col, new_board, False )
                                        if not king_check:
                                    
                                            next_move  = self.uci_format(row,col,new_row,new_col)
                                        
                                            if promotion: # Code for Promotion
                                                if color == w:
                                                    promo = w_promo
                                                else:
                                                    promo = b_promo
                                                for x in promo:
                                                    next_move += x
                                                    
                                                    # add code to check for pawn promotion
                                                    
                                                    possible_moves.append(next_move)
                                            else:
                                                possible_moves.append(next_move)
                                                
                        #print(random_piece, possible_moves)
                        
                        
                    # KING movements
                    piece_present = False
                    if random_piece == 'K' or random_piece == 'k':
                        king_check = False
                            
                        # Code for Castling
                        if fen_parts[2] != '-':
                            for x in fen_parts[2]:
                                if x == 'K' or x == 'k':
                                    for i in range(1,3):
                                        new_col = col + i
                                        if self.is_valid_pos(row,new_col,len(board),len(board[0])):
                                            if board[row][new_col] != ' ':
                                                piece_present = True
                                                break
                                        
                                    
                                    if piece_present == False:
                                        if x == 'K' and color == w:
                                            next_move = 'e1g1'
                                            old_row = 7
                                            new_row = 7
                                            old_col = 4
                                            new_col = 6
                                            new_board = self.change_board(board,old_row,old_col,new_row,new_col, True)
                                            king_check = self.is_king_check(new_row, new_col, new_board, False )
                                            if not king_check:
                                                possible_moves.append(next_move)
                                        if x == 'k' and color == b:
                                            next_move = 'e8g8'
                                            old_row = 0
                                            new_row = 0
                                            old_col = 4
                                            new_col = 6
                                            new_board = self.change_board(board,old_row,old_col,new_row,new_col, True)
                                            king_check = self.is_king_check(new_row, new_col, new_board, False )
                                            if not king_check:
                                                possible_moves.append(next_move)
                                
                                if x == 'Q' or x == 'q':
                                    for i in range(-1, -4, -1):
                                        new_col = col + i
                                        if self.is_valid_pos(row,new_col,len(board),len(board[0])):
                                            if board[row][new_col] != ' ':
                                                piece_present = True
                                                break
                                        
                                    
                                    if piece_present == False:
                                        if x == 'Q' and color == w:
                                            next_move = 'e1c1'
                                            old_row = 7
                                            new_row = 7
                                            old_col = 4
                                            new_col = 2
                                            new_board = self.change_board(board,old_row,old_col,new_row,new_col, True)
                                            king_check = self.is_king_check(new_row, new_col, new_board, False )
                                            if not king_check:
                                                possible_moves.append(next_move)
                                        if x == 'q' and color == b:
                                            next_move = 'e8c8'
                                            old_row = 0
                                            new_row = 0
                                            old_col = 4
                                            new_col = 2
                                            new_board = self.change_board(board,old_row,old_col,new_row,new_col, True)
                                            king_check = self.is_king_check(new_row, new_col, new_board, False )
                                            if not king_check:
                                                possible_moves.append(next_move)
                                                  
                        # Code for valid moves
                        K_offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                        
                        for pos_ in K_offset:
                            
                            pos_row,pos_col = pos_[0],pos_[1]
                            
                            new_row = row + pos_row
                            new_col = col + pos_col
                            
                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                                
                                king_check = False
                            
                                if (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets) or (board[new_row][new_col] == ' '):
                                    
                                    new_board = self.change_board(board,row,col,new_row,new_col, False)
                                    king_check = False
                                    next_move  = self.uci_format(row,col,new_row,new_col)
                                    king_check = self.is_king_check(new_row, new_col, new_board, False )
                                    if not king_check:
                                        
                                        possible_moves.append(next_move)
                        #print(random_piece, possible_moves)
                        
                    
                    # KNIGHT movements
                    if random_piece == 'N' or random_piece == 'n':
                        N_offset = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
                        
                        for pos_ in N_offset:
                            
                            pos_row,pos_col = pos_[0],pos_[1]
                            new_row = row + pos_row 
                            new_col = col + pos_col
                            
                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                                if (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets) or (board[new_row][new_col] == ' '):
                                    
                                    
                                    new_board = self.change_board(board,row,col,new_row,new_col, False)
                                    king_check = False
                                    next_move  = self.uci_format(row,col,new_row,new_col)
                                    king_check = self.is_king_check(king_row, king_col, new_board, False )
                                    if not king_check:
                                        
                                        possible_moves.append(next_move)
                                    
                        #print(random_piece, possible_moves)
                    
                    # BISHOP movements
                    if random_piece == 'B' or random_piece == 'b':
                        B_offset = [(1,1),(1,-1),(-1,-1),(-1,1)]
                        
                        possible_moves = self.make_next_move(random_piece, B_offset, row, col,possible_moves, color, board, king_row, king_col)
                        
                    # ROOK movements
                    if random_piece == 'R' or random_piece == 'r':
                        R_offset = [(0,1),(1,0),(0,-1),(-1,0)]
                        
                        possible_moves = self.make_next_move(random_piece, R_offset, row, col,possible_moves, color, board, king_row, king_col)
                        
                    
                    # QUEEN movements
                    if random_piece == 'Q' or random_piece == 'q':
                        Q_offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                        
                        possible_moves = self.make_next_move(random_piece, Q_offset, row, col,possible_moves, color, board, king_row, king_col)
                        
        return possible_moves
    
    def uci_to_index(self, uci_move):
        file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        rank_map = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

        # Extract the source and destination squares from the UCI move
        source = (file_map[uci_move[0]], rank_map[uci_move[1]])
        dest = (file_map[uci_move[2]], rank_map[uci_move[3]])

        return source, dest
        
    def minimax(self, board, temp_board, depth, is_maximizing_player, alpha, beta, time_limit, elapsed_time, total_sec, source, dest):
        elapsed_time1 = elapsed_time

        if depth == 0:
        
            heu_val = self.heuristic_fucntion(board)
            
            if (board[source[0]][source[1]].isupper() and board[dest[0]][dest[1]].islower() and is_maximizing_player) or (board[source[0]][source[1]].islower() and board[dest[0]][dest[1]].isupper() and not is_maximizing_player):
                heu_val += 100
            
            if is_maximizing_player:
                king = 'K'
            else:
                king = 'k'
            
            positions = []
            for i, line in enumerate(board):
                for j,k in enumerate(line):
                    if k == king:
                        positions.append((i,j))
            if positions != []:
                king_check = self.is_king_check(positions[0][0], positions[0][1], board, False )
                if king_check:
                    heu_val += 1000
            
            return heu_val, None

        if is_maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in self.get_legal_moves(board, 'white'):
                
                if len(self.game.history) >= 1:
                    swapped_move = move[-2:] + move[2:-2] + move[:2]
                    #if self.game.history.count(move) > 1 or self.game.history.count(swapped_move) > 1:
                    if move in self.game.history[-3:] or swapped_move in self.game.history[-3:]:
                        #print(move)
                        continue
                        
                source, dest = self.uci_to_index(move)
                new_board = self.change_board(board, source[0], source[1], dest[0], dest[1], False)

                score, temp_move = self.minimax(new_board, temp_board, depth - 1, False, alpha, beta, time_limit, elapsed_time1, total_sec, source, dest)
                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

                if elapsed_time >= time_limit or elapsed_time1 >= time_limit:
                    return best_score, best_move

                tm_sec1 = time.localtime(time.time()).tm_sec
                tm_min1 = time.localtime(time.time()).tm_min
                elapsed_time1 = (tm_sec1 + (tm_min1 * 60)) - total_sec
                
            return best_score, best_move

        else:
            best_score = float('inf')
            best_move = None
            for move in self.get_legal_moves(board, 'black'):
                
                if len(self.game.history) >= 1:
                    swapped_move = move[-2:] + move[2:-2] + move[:2]
                    #if self.game.history.count(move) > 1 or self.game.history.count(swapped_move) > 1:
                    if move in self.game.history[-3:] or swapped_move in self.game.history[-3:]:
                        #print(move)
                        continue
                
            
                source, dest = self.uci_to_index(move)
                new_board = self.change_board(board, source[0], source[1], dest[0], dest[1], False)

                score, temp_move = self.minimax(new_board, temp_board, depth - 1, True, alpha, beta, time_limit, elapsed_time1, total_sec, source, dest)
                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)
                if alpha >= beta:
                    break

                if elapsed_time >= time_limit or elapsed_time1 >= time_limit:
                    return best_score, best_move
                

                tm_sec1 = time.localtime(time.time()).tm_sec
                tm_min1 = time.localtime(time.time()).tm_min
                elapsed_time1 = (tm_sec1 + (tm_min1 * 60)) - total_sec
                
            return best_score, best_move

    '''
    def minimax(self, board, temp_board,depth, is_maximizing_player, time_limit, elapsed_time, total_sec):
        elapsed_time1 =  elapsed_time

        if depth == 0:
            return self.heuristic_fucntion(board),None

        if is_maximizing_player:
            best_score = float('-inf')
            for move in self.get_legal_moves(board,'white'):
                source,dest = self.uci_to_index(move)
                new_board = self.change_board(board,source[0],source[1],dest[0],dest[1], False)
                
                score,temp_move = self.minimax(new_board, temp_board,depth-1, False, time_limit, elapsed_time1, total_sec)
                if score > best_score:
                    best_score = score
                    best_move = move
                
                if elapsed_time >= time_limit or elapsed_time1 >= time_limit :
                    return best_score,best_move
                   
                
                tm_sec1 = time.localtime(time.time()).tm_sec
                tm_min1 = time.localtime(time.time()).tm_min
                elapsed_time1 = (tm_sec1 + (tm_min1 * 60)) - total_sec
            
            return best_score,best_move

        else:
            best_score = float('inf')
            for move in self.get_legal_moves(board,'black'):
                source,dest = self.uci_to_index(move)
                new_board = self.change_board(board,source[0],source[1],dest[0],dest[1], False)
                score,temp_move = self.minimax(new_board, temp_board,depth-1, True, time_limit, elapsed_time1, total_sec)
                if score < best_score:
                    best_score = score
                    best_move = move
                if elapsed_time >= time_limit or elapsed_time1 >= time_limit :
                    return best_score,best_move
                   
                
                tm_sec1 = time.localtime(time.time()).tm_sec
                tm_min1 = time.localtime(time.time()).tm_min
                elapsed_time1 = (tm_sec1 + (tm_min1 * 60)) - total_sec
                
            return best_score, best_move
    '''
    
    def iterative_deepening_minimax(self,board, temp_board,max_depth, time_limit, elapsed_time, total_sec):
        best_move = None
        best_value = -math.inf
        elapsed_time1 = elapsed_time
        for depth in range(1, max_depth + 1):
            # Check if we have run out of time.
            if elapsed_time >= time_limit or elapsed_time1 >= time_limit :
                break
            alpha = float("-inf")
            beta = float("inf")
            # Find the best move at the current depth.
            value, move = self.minimax(board, temp_board,depth, True, alpha, beta,time_limit, elapsed_time1, total_sec,(),())
            if value > best_value:
                best_value = value
                best_move = move
                
            tm_sec1 = time.localtime(time.time()).tm_sec
            tm_min1 = time.localtime(time.time()).tm_min
            elapsed_time1 = (tm_sec1 + (tm_min1 * 60)) - total_sec
        
        if best_move != None:
            return best_move
        else:
            return None

    #END of custom code
    
    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Interface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """
        # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for makeMove
        
        board = self.fen_to_array(self.game.fen)
        temp_board = self.fen_to_array(self.game.fen)
        
        start_time = time.localtime(time.time())
        tm_sec = start_time.tm_sec
        tm_min = start_time.tm_min
        
        total_sec = tm_sec + (tm_min * 60)
        rem_ts = self.player.time_remaining / 1000000000
        if rem_ts > 350:
            time_limit = (rem_ts) * 0.0125 
        elif rem_ts < 350:
            time_limit = (rem_ts) * 0.025 
        elif rem_ts > 125 and rem_ts < 350:
            time_limit = (rem_ts) * 0.05
        else:
            time_limit = (rem_ts) * 0.0125 
        
        
        max_depth = 1
        
        elapsed_time  = 0
        random_move = ' ' 
        while elapsed_time < time_limit:
            
            random_move = self.iterative_deepening_minimax(board, temp_board,max_depth, time_limit, elapsed_time, total_sec)
            max_depth += 1
            
            tm_sec1 = time.localtime(time.time()).tm_sec
            tm_min1 = time.localtime(time.time()).tm_min
            elapsed_time = (tm_sec1 + (tm_min1 * 60)) - total_sec
            
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------", random_move)
        print("max depth", max_depth,"time",elapsed_time, board)
        if random_move != ' ':
            return random_move
        else:
            return None
    
        '''
        possible_moves = self.get_legal_moves(board, self.player.color)
        
        print(len(possible_moves))
        print(possible_moves)
        
        if len(possible_moves) != 0:
            random.shuffle(possible_moves)
            random_move = possible_moves.pop()
            print(random_move)
            print(self.player.color)
            
            return random_move
            
        else:
            return None
        '''

        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
