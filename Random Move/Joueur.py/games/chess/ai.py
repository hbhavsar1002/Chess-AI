'''
Name: Harsh Hirenkumar Bhavsar
'''

# This is where you build your AI for the Chess game.
# All the required packages
from joueur.base_ai import BaseAI
import random

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
    def fen_to_array(self, fen: str) -> list[str]:
    
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
    def uci_format(self,row,col,new_row,new_col) -> str:
        uci_col = ['a','b','c','d','e','f','g','h']
        
        b = 'black'
        w = 'white'
        
        row = 8 - row
        new_row = 8 - new_row
        
        uci_format = uci_col[col] + str(row) + uci_col[new_col] + str(new_row)
        return uci_format
    
    # Function to make valid next move 
    def make_next_move(self, random_piece, offset, row, col,possible_moves, color,board) -> list[str]:
    
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
                        next_move  = self.uci_format(row,col,new_row,new_col)
                        #print(random_piece,next_move)
                        possible_moves.append(next_move)
                        if board[new_row][new_col] == ' ':
                            continue
                        else: 
                            break
                    else:
                        break
        return possible_moves
    #END of custom code
    
    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Interface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """
        # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for makeMove
        
        # Initialize variables
        w_alphabets = 'BKNPQR'
        b_alphabets = 'bknpqr'
        
        w_promo = 'BKNQR'
        b_promo = 'bknqr'
        
        b = 'black'
        w = 'white'
        
        board = self.fen_to_array(self.game.fen)
        
        fen_parts = self.game.fen.split(' ')
        
        #print(board)
        
        #print(self.game.history)
        #print("FEN String",self.game.fen)
        #print("Color of my player",self.player.color)
        color =  self.player.color
        #print(color)
        en_passant = False
        
        if color == w:
            alphabets = w_alphabets
        elif color == b:
            alphabets = b_alphabets
        
        # Initialize Next Possible Moves variable
        possible_moves = []
        
        for random_piece in alphabets:
            if any(random_piece in x for x in board):
                
                positions = []
                for i, line in enumerate(board):
                        for j,k in enumerate(line):
                            try:
                                if k == random_piece:
                                    positions.append((i,j))
                            except ValueError:
                                continue
                
                #print("positions",random_piece,positions)
                
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
                            
                            
                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                                # Diagonal direction
                                if pos_col == 1 or pos_col == -1:
                                    if board[new_row][new_col] == ' ':
                                    
                                        if en_passant:
                                            next_move  = self.uci_format(row,col,new_row,new_col)
                                            if fen_parts[3] == next_move[-2:]:
                                                #print(next_move)
                                                possible_moves.append(next_move)
                                        continue
                                    elif (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets):
    
                                        next_move  = self.uci_format(row,col,new_row,new_col)
                                        if promotion: # Code for Promotion
                                            if color == w:
                                                next_move = next_move + random.choice(w_promo)
                                            else:
                                                next_move = next_move + random.choice(b_promo)
                                        possible_moves.append(next_move)
                                # Vertical direction
                                else:
                                    
                                    if board[new_row][new_col] == ' ':
                                    
                                        next_move  = self.uci_format(row,col,new_row,new_col)
                                        
                                        if promotion: # Code for Promotion
                                            if color == w:
                                                next_move = next_move + random.choice(w_promo)
                                            else:
                                                next_move = next_move + random.choice(b_promo)
                                        
                                        possible_moves.append(next_move)
                        #print(random_piece, possible_moves)
                        continue
                        
                    # KING movements
                    piece_present = False
                    if random_piece == 'K' or random_piece == 'k':
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
                                        if x == 'K':
                                            next_move = 'e1g1'
                                        if x == 'k':
                                            next_move = 'e8g8'
                                        possible_moves.append(next_move)
                                
                                if x == 'Q' or x == 'q':
                                    for i in range(-1, -4, -1):
                                        new_col = col + i
                                        if self.is_valid_pos(row,new_col,len(board),len(board[0])):
                                            if board[row][new_col] != ' ':
                                                piece_present = True
                                                break
                                        
                                    
                                    if piece_present == False:
                                        if x == 'Q':
                                            next_move = 'e1c1'
                                        if x == 'q':
                                            next_move = 'e8c8'
                                        possible_moves.append(next_move)
                                                  
                        # Code for valid moves
                        K_offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                        
                        for pos_ in K_offset:
                            
                            pos_row,pos_col = pos_[0],pos_[1]
                            
                            new_row = row + pos_row
                            new_col = col + pos_col
                            
                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                            
                                if (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets) or (board[new_row][new_col] == ' '):
                                    next_move  = self.uci_format(row,col,new_row,new_col)
                                    possible_moves.append(next_move)
                        #print(random_piece, possible_moves)
                        continue
                    
                    # KNIGHT movements
                    if random_piece == 'N' or random_piece == 'n':
                        N_offset = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
                        
                        for pos_ in N_offset:
                            
                            pos_row,pos_col = pos_[0],pos_[1]
                            new_row = row + pos_row 
                            new_col = col + pos_col
                            if self.is_valid_pos(new_row,new_col,len(board),len(board[0])):
                                if (color == w and board[new_row][new_col] in b_alphabets) or (color == b and board[new_row][new_col] in w_alphabets) or (board[new_row][new_col] == ' '):
                                    next_move  = self.uci_format(row,col,new_row,new_col)
                                    possible_moves.append(next_move)
                                    
                        #print(random_piece, possible_moves)
                        continue
                    
                    # BISHOP movements
                    if random_piece == 'B' or random_piece == 'b':
                        B_offset = [(1,1),(1,-1),(-1,-1),(-1,1)]
                        
                        possible_moves = self.make_next_move(random_piece, B_offset, row, col,possible_moves, color, board)
                        
                        continue
                    
                    # ROOK movements
                    if random_piece == 'R' or random_piece == 'r':
                        R_offset = [(0,1),(1,0),(0,-1),(-1,0)]
                        
                        possible_moves = self.make_next_move(random_piece, R_offset, row, col,possible_moves, color, board)
                        continue
                    
                    # QUEEN movements
                    if random_piece == 'Q' or random_piece == 'q':
                        Q_offset = [(0,1),(1,1),(1,0),(1,-1),(-1,-1),(0,-1),(-1,0),(-1,1)]
                        
                        possible_moves = self.make_next_move(random_piece, Q_offset, row, col,possible_moves, color, board)
                        
                        continue
                        
    
        print(len(possible_moves))
        print(possible_moves)
        
        if len(possible_moves) != 0:
            random.shuffle(possible_moves)
            random_move = possible_moves.pop()
            print(random_move)
            
            return random_move
            
        else:
            return None


        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
