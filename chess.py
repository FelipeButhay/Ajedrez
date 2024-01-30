import pygame
import chess_defs as ch
import fen

#fen = input("FEN: ")
fen_code = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
obj_list, data_turn = fen.fen_to_board(fen_code)
    
playin = True
turn = data_turn

mouse = False
promoting = False

sq_size = ch.board_coord//8
#background_colour = (133, 146, 158)

obj = ch.piece((None, None), turn, None, False)
posible = [[],[]]
fix_pos = lambda: ((mouse_pos[0]-ch.gap)//sq_size, (mouse_pos[1]-ch.gap)//sq_size)
search_inter = lambda posible: posible[0].count(fix_pos()) != 0 or posible[1].count(fix_pos()) != 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((ch.screen_x, ch.screen_y))
pygame.display.set_caption("Chess")
pygame.mouse.get_visible

while playin:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #MOUSE
    mouse_pos = pygame.mouse.get_pos()
    mouse_save = mouse
    mouse = pygame.mouse.get_pressed()[0]      

    #MOVE THE PIECES
    if (mouse and not mouse_save) and search_inter(posible):
        promoting = obj.move(obj.position, fix_pos(), screen, sq_size, obj_list, clock, True)
        freeze_mouse_pos = mouse_pos
        turn = not turn
        for x in obj_list:
            if x.colour == turn:
                x.enpassant = None
                
        checkmate, stalemate = ch.mate(turn, obj_list)
        if checkmate or stalemate:
            if checkmate:
                if not turn == True:
                    print("\nWHITE WINS\n")
                elif not turn == False:
                    print("\nBLACK WINS\n")
            elif stalemate:
                print("\nTIE\n")
            playin = False
        
    elif mouse and not mouse_save and not promoting:
        for obj_it in obj_list:
            if obj_it.position == fix_pos() and obj_it.colour == turn:
                obj = obj_it
                obj.selected = True
                posible = obj.posible(obj_list, 1)
                break
        else:
            obj = ch.piece((None, None), None, None, False)

    if not obj.selected:
        posible = [[], []]

    # DRAW THINGS ON THE SCREEN
    ch.draw_board(screen, sq_size, obj_list)
        
    for x in posible[0]:
        screen.blit(ch.sprites[14], (x[0]*sq_size+ch.gap, x[1]*sq_size+ch.gap))
    for x in posible[1]:
        screen.blit(ch.sprites[15], (x[0]*sq_size+ch.gap, x[1]*sq_size+ch.gap))
        
    if promoting:
        promoting = obj.promote(screen, sq_size, freeze_mouse_pos, mouse_pos, mouse, mouse_save)
        
    pygame.display.update()
    clock.tick(60)