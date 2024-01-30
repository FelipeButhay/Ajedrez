import pygame
import os

screen_x, screen_y = 1080, 600
while False:
    try:
        resolution = input("resolution (x,y format): ").split(",")
        screen_x = int(resolution[0])
        screen_y = int(resolution[1]) 
        break
    except:
        pass
    
import tkinter as tk
resolution_screen = tk.Tk()
screen_x = resolution_screen.winfo_screenwidth()
screen_y = resolution_screen.winfo_screenheight()
        
board_coord = screen_y*0.9//1
gap = (screen_y - board_coord)//2

direc = os.path.dirname(os.path.abspath(__file__)).replace('\'', '/')
white_rook   = pygame.image.load(f"{direc}/chess/white_rook.png")
white_knight = pygame.image.load(f"{direc}/chess/white_knight.png")
white_bishop = pygame.image.load(f"{direc}/chess/white_bishop.png")
white_queen  = pygame.image.load(f"{direc}/chess/white_queen.png")
white_king   = pygame.image.load(f"{direc}/chess/white_king.png")
white_pawn   = pygame.image.load(f"{direc}/chess/white_pawn.png")

black_rook   = pygame.image.load(f"{direc}/chess/black_rook.png")
black_knight = pygame.image.load(f"{direc}/chess/black_knight.png")
black_bishop = pygame.image.load(f"{direc}/chess/black_bishop.png")
black_queen  = pygame.image.load(f"{direc}/chess/black_queen.png")
black_king   = pygame.image.load(f"{direc}/chess/black_king.png")
black_pawn   = pygame.image.load(f"{direc}/chess/black_pawn.png")

castel_sign  = pygame.image.load(f"{direc}/chess/plus sign.png")
circle       = pygame.image.load(f"{direc}/chess/circle.png")
hole_circle  = pygame.image.load(f"{direc}/chess/capture circle.png")

rect         = pygame.image.load(f"{direc}/chess/rect.png")
reset_butt1  = pygame.image.load(f"{direc}/chess/reset.png")
reset_butt2  = pygame.image.load(f"{direc}/chess/reset2.png")

last_piece_moved = pygame.image.load(f"chess/last piece.png")
illegal_sprite   = pygame.image.load(f"chess/king in check.png")


sprites = [white_rook, white_knight, white_bishop, white_queen, white_king, white_pawn, 
           black_rook, black_knight, black_bishop, black_queen, black_king, black_pawn, 
           last_piece_moved, illegal_sprite, circle, hole_circle]

rect = pygame.transform.scale(rect, (board_coord//8+10, board_coord//2+10))
for x in sprites[:]:
    sprites.remove(x)
    sprites.append(pygame.transform.scale(x, (board_coord//8, board_coord//8)))
    

def draw_board(screen, sq_size, obj_list):
    screen.fill((85,85,85))
    pygame.draw.rect(screen, (133, 146, 158),(gap, gap, sq_size*8, sq_size*8), 0)
    for y in range(0,4):  
        for x in range(0,8):
            pygame.draw.rect(screen, "white",((x*sq_size)+gap, ((y*sq_size*2)+(x%2)*sq_size)+gap, sq_size, sq_size), 0)
            
    for x in obj_list:
        x.insert(screen, sq_size)


def pieces_list_gen(obj_list):
    white_pieces=[]
    black_pieces=[]
    for x in obj_list:
        if x.colour:
            white_pieces.append(x.position)
        elif not x.colour:
            black_pieces.append(x.position)
    
    return (white_pieces, black_pieces)
    
def recon_pieces(turn, obj_list):
    white_pieces, black_pieces = pieces_list_gen(obj_list)
    
    if turn:
        my_pieces = white_pieces
        alt_pieces = black_pieces
    else:
        my_pieces = black_pieces
        alt_pieces = white_pieces
        
    return (my_pieces, alt_pieces)

#depth 0
def fix_movements(moves, colour, obj_list):
    captures = []
    din_pieces = recon_pieces(colour, obj_list)
    
    for x in moves[:]:
        if x in din_pieces[0]:
            moves.remove(x)
        elif x in din_pieces[1]:
            moves.remove(x)
            captures.append(x)
    
    return (moves,captures)

def move_out(moves):
    for x in moves[:]:
        for xx in x:
            if 0>xx or xx>7:
                moves.remove(x)
                break
    return moves

#depth 1
def check(colour, obj_list):
    multi_check = False
    bool_check = False
    piece_pos = []
    for x in obj_list:
        if x.type.lower() == "k" and x.colour == colour:
            king_pos = x.position
            break
    for x in obj_list:
        for y in x.posible(obj_list, 0)[1]:
            if y == king_pos:
                piece_pos.append(x.position)
                bool_check = True
                break
    if len(piece_pos)>1:
        multi_check = True
    return (bool_check, multi_check, king_pos, tuple(piece_pos))

#checkmate and stalemate
def mate(colour, obj_list):
    stealmate = False
    for x in obj_list:
        if len(x.posible(obj_list, 1)[0])!=0 and x.colour == colour:
            break
        elif len(x.posible(obj_list, 1)[1])!=0 and x.colour == colour:
            break
    else:
        stealmate = True
        
    if stealmate and check(colour, obj_list)[0]:
        checkmate = True
    else:
        checkmate = False
    
    return (checkmate, stealmate)
 
    
class piece:
    def __init__(self, position, colour, piece_type, selected):
        self.position = position
        self.inv_position = (position[1], position[0])
        
        self.colour = colour
        self.type = piece_type
        self.selected = selected
        self.moved = False
        self.enpassant = None
        
    def insert(self, screen, sq_size):
        screen.blit(self.sprite, (self.position[0]*sq_size+gap, self.position[1]*sq_size+gap))
        
    def promote(self, screen, sq_size, mouse_position, nu_mouse_pos, mouse, mouse_save):
        if self.colour:
            screen.blit(rect, mouse_position)
            screen.blit(sprites[3], (mouse_position[0]+5, mouse_position[1] + 5 + (board_coord//8)*0))
            screen.blit(sprites[0], (mouse_position[0]+5, mouse_position[1] + 5 + (board_coord//8)*1))
            screen.blit(sprites[2], (mouse_position[0]+5, mouse_position[1] + 5 + (board_coord//8)*2))
            screen.blit(sprites[1], (mouse_position[0]+5, mouse_position[1] + 5 + (board_coord//8)*3))
            
            if mouse and not mouse_save and (mouse_position[0]+4)<nu_mouse_pos[0]<(mouse_position[0]+5+board_coord//8):
                if   (nu_mouse_pos[1] - mouse_position[1]-5)//sq_size == 0:
                    self.__class__ = queen
                    self.type = "Q"
                    self.sprite = sprites[3]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1]-5)//sq_size == 1:
                    self.__class__ = rook
                    self.type = "R"
                    self.sprite = sprites[0]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1]-5)//sq_size == 2:
                    self.__class__ = bishop
                    self.type = "B"
                    self.sprite = sprites[2]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1]-5)//sq_size == 3:
                    self.__class__ = knight
                    self.type = "N"
                    self.sprite = sprites[1]
                    return False
            
        if not self.colour:
            screen.blit(rect, (mouse_position[0], mouse_position[1] - (board_coord//2+10)))
            screen.blit(sprites[9], (mouse_position[0]+5, mouse_position[1] - (5 + (board_coord//8)*4)))
            screen.blit(sprites[6], (mouse_position[0]+5, mouse_position[1] - (5 + (board_coord//8)*3)))
            screen.blit(sprites[8], (mouse_position[0]+5, mouse_position[1] - (5 + (board_coord//8)*2)))
            screen.blit(sprites[7], (mouse_position[0]+5, mouse_position[1] - (5 + (board_coord//8)*1)))
            #print(f"{mouse_position[0]+4} < {nu_mouse_pos[0]} < {mouse_position[0]+5+board_coord//8} -> {(mouse_position[0]+4)<nu_mouse_pos[0]<(mouse_position[0]+5+board_coord//8)}")
            
            if mouse and not mouse_save and (mouse_position[0]+4)<nu_mouse_pos[0]<(mouse_position[0]+5+board_coord//8):
                if   (nu_mouse_pos[1] - mouse_position[1] - (board_coord//2+10)-5)//sq_size == -8:
                    self.__class__ = queen
                    self.type = "q"
                    self.sprite = sprites[9]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1] - (board_coord//2+10)-5)//sq_size == -7:
                    self.__class__ = rook
                    self.type = "r"
                    self.sprite = sprites[6]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1] - (board_coord//2+10)-5)//sq_size == -6:
                    self.__class__ = bishop
                    self.type = "b"
                    self.sprite = sprites[8]
                    return False
                elif (nu_mouse_pos[1] - mouse_position[1] - (board_coord//2+10)-5)//sq_size == -5:
                    self.__class__ = knight
                    self.type = "n"
                    self.sprite = sprites[7]
                    return False
        return True
            
    def move(self, start_position, end_position, screen, sq_size, obj_list, clock, animated):
        x_var = (start_position[0] - end_position[0])/12
        y_var = (start_position[1] - end_position[1])/12
        self.selected = False
        casteling = False
        
        for x in obj_list:
            if x.position == end_position:
                obj_list.remove(x)
                break
            elif x.enpassant == end_position:
                obj_list.remove(x)
                break
        
        if self.type.lower() == "k" and not self.moved and end_position == (2,0):
            for x in obj_list:
                if x.position == (0,0):
                    casteling = True
                    castel_rook = x
                    castel_rook_start = (0,0)
                    castel_x_var = (castel_rook_start[0] - 3)/12
                    break
        elif self.type.lower() == "k" and not self.moved and end_position == (6,0): 
            for x in obj_list:
                if x.position == (7,0):
                    casteling = True
                    castel_rook = x
                    castel_rook_start = (7,0)
                    castel_x_var = (castel_rook_start[0] - 5)/12
                    break
        elif self.type.lower() == "k" and not self.moved and end_position == (2,7): 
            for x in obj_list:
                if x.position == (0,7):
                    casteling = True
                    castel_rook = x
                    castel_rook_start = (0,7)
                    castel_x_var = (castel_rook_start[0] - 3)/12
                    break
        elif self.type.lower() == "k" and not self.moved and end_position == (6,7): 
            for x in obj_list:
                if x.position == (7,7):
                    casteling = True
                    castel_rook = x
                    castel_rook_start = (7,7)
                    castel_x_var = (castel_rook_start[0] - 5)/12
                    break
           
        if self.type.lower() == "p" and start_position[1] == 1 and end_position[1] == 3:
            self.enpassant = (self.position[0], 2)
        elif self.type.lower() == "p" and start_position[1] == 6 and end_position[1] == 4: 
            self.enpassant = (self.position[1], 5)
        else:
            self.enpassant = None
        
        if animated:
            for xx in range(0,13):
                self.position = (start_position[0] - x_var*xx, start_position[1] - y_var*xx)
                if casteling:
                    castel_rook.position = (castel_rook_start[0] - castel_x_var*xx, start_position[1])
                draw_board(screen, sq_size, obj_list)
                pygame.display.update()
                clock.tick(60)
        else:
            self.position = (start_position[0] - x_var*12, start_position[1] - y_var*12)
            if casteling:
                castel_rook.position = (castel_rook_start[0] - castel_x_var*12, start_position[1])
            
        self.moved = True

        if self.type.lower() == "p" and ((end_position[1] == 0 and self.colour) or (end_position[1] == 7 and not self.colour)):
            return True
        else: 
            return False
        
    def depth_func(self, depth, moves, captures, obj_list):
        moves = list(moves)
        captures =  list(captures)
        pos_save = self.position
        
        if depth == 1:
            if check(self.colour, obj_list)[1]:
                moves.clear()
                captures.clear()
            else:
                for x in moves[:]:
                    self.position = x
                    if check(self.colour, obj_list)[0]:
                        moves.remove(x)
            
                for x in captures[:]:
                    self.position = x
                    for y in obj_list:
                        if y.position == x:
                            obj_list.remove(y)
                            if check(self.colour, obj_list)[0]:
                                captures.remove(x)
                            obj_list.append(y)
                            break

        self.position = pos_save
        return (moves, captures)
        
    def __str__(self):
        string = f"""{self.position}
        {self.colour}
        {self.type}\n"""
        return string.replace(" ","")
        
class rook(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[0]
        else:
            self.sprite = sprites[6]
        
    def posible(self, obj_list, depth):
        din_pieces = recon_pieces(self.colour, obj_list)
        all_pieces = (*din_pieces[0], *din_pieces[1])
        moves = []
        captures = []

        for x in range(1,8):
            if (self.position[0]+x > 7) or (all_pieces.count((self.position[0]+x,self.position[1]))!=0):
                if din_pieces[1].count((self.position[0]+x,self.position[1])) != 0:
                    captures.append((self.position[0]+x,self.position[1]))
                break
            moves.append((self.position[0]+x,self.position[1]))
        for x in range(1,8):
            if (self.position[0]-x < 0) or (all_pieces.count((self.position[0]-x,self.position[1]))!=0):
                if din_pieces[1].count((self.position[0]-x,self.position[1])) != 0:
                    captures.append((self.position[0]-x,self.position[1]))
                break
            moves.append((self.position[0]-x,self.position[1]))
        for x in range(1,8):
            if (self.position[1]+x > 7) or (all_pieces.count((self.position[0],self.position[1]+x))!=0):
                if din_pieces[1].count((self.position[0],self.position[1]+x)) != 0:
                    captures.append((self.position[0],self.position[1]+x))
                break
            moves.append((self.position[0],self.position[1]+x))
        for x in range(1,8):
            if (self.position[1]-x < 0) or (all_pieces.count((self.position[0],self.position[1]-x))!=0):
                if din_pieces[1].count((self.position[0],self.position[1]-x)) != 0:
                    captures.append((self.position[0],self.position[1]-x))
                break
            moves.append((self.position[0],self.position[1]-x))
        
        return self.depth_func(depth, moves, captures, obj_list)
    
class bishop(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[2]
        else:
            self.sprite = sprites[8]
        
    def posible(self, obj_list, depth):
        din_pieces = recon_pieces(self.colour, obj_list)
        all_pieces = (*din_pieces[0], *din_pieces[1])
        moves = []
        captures = []

        for x in range(1,8):
            if (self.position[0]+x > 7) or (self.position[1]+x > 7) or (all_pieces.count((self.position[0]+x,self.position[1]+x))!=0):
                if din_pieces[1].count((self.position[0]+x,self.position[1]+x)) != 0:
                    captures.append((self.position[0]+x,self.position[1]+x))
                break
            moves.append((self.position[0]+x,self.position[1]+x))
        for x in range(1,8):
            if (self.position[0]+x > 7) or (self.position[1]-x < 0) or (all_pieces.count((self.position[0]+x,self.position[1]-x))!=0):
                if din_pieces[1].count((self.position[0]+x,self.position[1]-x)) != 0:
                    captures.append((self.position[0]+x,self.position[1]-x))
                break
            moves.append((self.position[0]+x,self.position[1]-x))
        for x in range(1,8):
            if (self.position[0]-x < 0) or (self.position[1]+x > 7) or (all_pieces.count((self.position[0]-x,self.position[1]+x))!=0):
                if din_pieces[1].count((self.position[0]-x,self.position[1]+x)) != 0:
                    captures.append((self.position[0]-x,self.position[1]+x))
                break
            moves.append((self.position[0]-x,self.position[1]+x))
        for x in range(1,8):
            if (self.position[0]-x < 0) or (self.position[1]-x < 0) or (all_pieces.count((self.position[0]-x,self.position[1]-x))!=0):
                if din_pieces[1].count((self.position[0]-x,self.position[1]-x)) != 0:
                    captures.append((self.position[0]-x,self.position[1]-x))
                break
            moves.append((self.position[0]-x,self.position[1]-x)) 
        
        return self.depth_func(depth, moves, captures, obj_list)
    
class queen(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[3]
        else:
            self.sprite = sprites[9]
        
    def posible(self, obj_list, depth):       
        bishop_for_queen = bishop(self.position, self.colour, self.type, self.selected)
        rook_for_queen = rook(self.position, self.colour, self.type, self.selected)
        
        bishop_moves, bishop_captures = bishop_for_queen.posible(obj_list, 0)
        rook_moves, rook_captures = rook_for_queen.posible(obj_list, 0)
        
        moves, captures = (*rook_moves, *bishop_moves), (*rook_captures, *bishop_captures)
        
        return self.depth_func(depth, moves, captures, obj_list)
    
class king(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[4]
        else:
            self.sprite = sprites[10]
        
    def posible(self, obj_list, depth):
        all_moves = [(self.position[0]-1,self.position[1]-1),(self.position[0],self.position[1]-1),(self.position[0]+1,self.position[1]-1),(self.position[0]-1,self.position[1]),(self.position[0]+1,self.position[1]),(self.position[0]-1,self.position[1]+1),(self.position[0],self.position[1]+1),(self.position[0]+1,self.position[1]+1)]
        moves, captures = fix_movements(list(move_out(all_moves)), self.colour, obj_list)
        
        if depth == 1:
            if self.colour and self.position == (4,7):
                for x in obj_list:
                    if x.position == (7,7) and not x.moved:
                        w_king_side_rook = True
                        break
                else:
                    w_king_side_rook = False
                        
                for x in obj_list:
                    if x.position == (0,7) and not x.moved:
                        w_queen_side_rook = True
                        break
                else: 
                    w_queen_side_rook = False
                
                for x in obj_list:
                    if x.position == (5,7):
                        w_king_empty_space = False
                        break
                    elif x.position == (6,7):
                        w_king_empty_space = False
                        break
                else:
                    w_king_empty_space = True
                
                for x in obj_list:
                    if x.position == (3,7):
                        w_queen_empty_space = False
                        break
                    elif x.position == (2,7):
                        w_queen_empty_space = False
                        break
                    elif x.position == (1,7):
                        w_queen_empty_space = False
                else:
                    w_queen_empty_space = True
                
                if not self.moved and w_king_side_rook and w_king_empty_space and (5,7) in moves:
                    moves.append((6,7))
                if not self.moved and w_queen_side_rook and w_queen_empty_space and (3,7) in moves:
                    moves.append((2,7))
        
            elif not self.colour and self.position == (4,0):
                for x in obj_list:
                    if x.position == (7,0) and not x.moved:
                        b_king_side_rook = True
                        break
                else:
                    b_king_side_rook = False
                        
                for x in obj_list:
                    if x.position == (0,0) and not x.moved:
                        b_queen_side_rook = True
                        break
                else: 
                    b_queen_side_rook = False
                
                for x in obj_list:
                    if x.position == (5,0):
                        b_king_empty_space = False
                        break
                    elif x.position == (6,0):
                        b_king_empty_space = False
                        break
                else:
                    b_king_empty_space = True
                
                for x in obj_list:
                    if x.position == (3,0):
                        b_queen_empty_space = False
                        break
                    elif x.position == (2,0):
                        b_queen_empty_space = False
                        break
                    elif x.position == (1,0):
                        b_queen_empty_space = False
                else:
                    b_queen_empty_space = True
                
                if not self.moved and b_king_side_rook and b_king_empty_space and (5,0) in moves:
                    moves.append((6,0))
                if not self.moved and b_queen_side_rook and b_queen_empty_space and (3,0) in moves:
                    moves.append((2,0))
                    
            pos_save = self.position
            for x in moves[:]:
                self.position = x
                if check(self.colour, obj_list)[0]:
                    moves.remove(x)  
            for x in captures[:]:
                self.position = x
                if check(self.colour, obj_list)[0]:
                    captures.remove(x)   
            self.position = pos_save
        
        return (moves, captures)
    
class knight(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[1]
        else:
            self.sprite = sprites[7]
        
    def posible(self, obj_list, depth):
        all_moves = [(self.position[0]-2,self.position[1]-1),(self.position[0]-2,self.position[1]+1),(self.position[0]-1,self.position[1]-2),(self.position[0]-1,self.position[1]+2),(self.position[0]+1,self.position[1]-2),(self.position[0]+1,self.position[1]+2),(self.position[0]+2,self.position[1]-1),(self.position[0]+2,self.position[1]+1)]
        moves, captures = fix_movements(list(move_out(all_moves)), self.colour, obj_list)

        return self.depth_func(depth, moves, captures, obj_list)
    
class pawn(piece):
    def __init__(self, position, colour, piece_type, selected):
        super().__init__(position, colour, piece_type, selected)
        if colour:
            self.sprite = sprites[5]
        else:
            self.sprite = sprites[11]
        
    def posible(self, obj_list, depth):
        white_pieces, black_pieces = pieces_list_gen(obj_list)
        all_pieces = (*white_pieces, *black_pieces)
        moves = []
        captures = []
        check_enpassant = None
        for x in obj_list:
            if x.enpassant != None:
                check_enpassant = x.enpassant
    
        if self.colour: #white
            if tuple(x for x in all_pieces).count((self.position[0], self.position[1]-1)) == 0:
                moves.append((self.position[0], self.position[1]-1))
                if self.position[1]==6 and tuple(x for x in all_pieces).count((self.position[0], self.position[1]-2)) == 0:
                    moves.append((self.position[0], self.position[1]-2))
            
            if self.position[0] < 7:
                if black_pieces.count((self.position[0]+1, self.position[1]-1)) != 0:
                    captures.append((self.position[0]+1, self.position[1]-1))
                elif (self.position[0]+1, self.position[1]-1) == check_enpassant:
                    captures.append(check_enpassant)
                    
            if self.position[0] > 0:
                if black_pieces.count((self.position[0]-1, self.position[1]-1)) != 0:
                    captures.append((self.position[0]-1, self.position[1]-1))
                elif (self.position[0]-1, self.position[1]-1) == check_enpassant:
                    captures.append(check_enpassant)
            
        elif not self.colour: #black
            if tuple(x for x in all_pieces).count((self.position[0], self.position[1]+1)) == 0:
                moves.append((self.position[0], self.position[1]+1))
                if self.position[1]==1 and tuple(x for x in all_pieces).count((self.position[0], self.position[1]+2)) == 0:
                    moves.append((self.position[0], self.position[1]+2))

            if self.position[0] < 7:
                if white_pieces.count((self.position[0]+1, self.position[1]+1)) != 0:
                    captures.append((self.position[0]+1, self.position[1]+1))
                elif (self.position[0]+1, self.position[1]+1) == check_enpassant:
                    captures.append(check_enpassant)
                    
            if self.position[0] > 0:
                if white_pieces.count((self.position[0]-1, self.position[1]+1)) != 0:
                    captures.append((self.position[0]-1, self.position[1]+1))
                elif (self.position[0]-1, self.position[1]+1) == check_enpassant:
                    captures.append(check_enpassant)
                    
        return self.depth_func(depth, moves, captures, obj_list)
    