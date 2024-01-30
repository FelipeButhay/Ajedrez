import chess_defs as ch
from operator import attrgetter

def fen_to_board(fen_code):
    fen_pos = fen_code.split(" ")[0]
    fen_data = fen_code.split(" ")[1:]
    
    if fen_data[0]=="w":
        turn = True
    elif fen_data[0]=="b":
        turn = False
    
    fen_pos = ",".join(fen_pos).split(",")
    
    piece_list = []
    x_axis = 0
    y_axis = 0
    for x in fen_pos:
        if x.isalpha():
            if x.isupper():
                if x=="P":
                    piece_list.append(ch.pawn((x_axis, y_axis), True, x, False))
                elif x=="R":
                    piece_list.append(ch.rook((x_axis, y_axis), True, x, False))
                elif x=="N":
                    piece_list.append(ch.knight((x_axis, y_axis), True, x, False))
                elif x=="B":
                    piece_list.append(ch.bishop((x_axis, y_axis), True, x, False))
                elif x=="Q":
                    piece_list.append(ch.queen((x_axis, y_axis), True, x, False))
                elif x=="K":
                    piece_list.append(ch.king((x_axis, y_axis), True, x, False))
            elif x.islower():
                if x=="p":
                    piece_list.append(ch.pawn((x_axis, y_axis), False, x, False))
                elif x=="r":
                    piece_list.append(ch.rook((x_axis, y_axis), False, x, False))
                elif x=="n":
                    piece_list.append(ch.knight((x_axis, y_axis), False, x, False))
                elif x=="b":
                    piece_list.append(ch.bishop((x_axis, y_axis), False, x, False))
                elif x=="q":
                    piece_list.append(ch.queen((x_axis, y_axis), False, x, False))
                elif x=="k":
                    piece_list.append(ch.king((x_axis, y_axis), False, x, False))
            x_axis += 1
        elif x.isnumeric():
            x_axis += int(x)
        else:
            y_axis += 1
            x_axis = 0
            
    return piece_list, turn,# castel, en-passant, num_move

def board_to_fen(obj_list, turn):
    sorted_obj = sorted(obj_list, key=attrgetter("inv_position"))
    fen_list = [[] for x in range(0,8)]
    sorted_obj_row = [[] for x in range(0,8)]
    for x in enumerate(sorted_obj_row):
        sorted_obj_row[x[0]] = [y for y in sorted_obj if y.position[1] == x[0]]
    
    fix_coinc = [[] for x in range(0,8)]
    for x in enumerate(sorted_obj_row):
        fen_list[x[0]].extend([y.type for y in x[1]])
        my_row = tuple(y.position for y in x[1])
        row = tuple((z, x[0]) for z in range(0,8))
        
        #crea una lista por cada fila, pone True en donde hay piezas y False donde no
        coinc = []
        for xx in row:
            for yy in my_row:
                if xx == yy:
                    coinc.append(True)
                    break
            else:
                coinc.append(False)
        
        #Junta los False en numeros (si hay 3 seguidos los reemplaza por un 3 y asi)
        fix_num = 0
        for y in coinc:
            if y:
                if fix_num!=0:
                    fix_coinc[x[0]].append(str(fix_num))
                fix_coinc[x[0]].append(y)   
                fix_num = 0            
            else:
                fix_num += 1
        else:
            if fix_num!=0:
                fix_coinc[x[0]].append(str(fix_num))
        
        if len(fix_coinc[x[0]])==0:
            fix_coinc[x[0]] = ["8"]    

    #Reemplaza los True por las letras de cada pieza
    for x in enumerate(fix_coinc[:]):
        xx = 0
        for y in enumerate(x[1]):
            if type(y[1])==type(True):
                fix_coinc[x[0]].pop(y[0])
                fix_coinc[x[0]].insert(y[0], fen_list[x[0]][xx],)
                xx += 1
    
    #junta cada item de la lista y crea la string final
    for x in range(0,8):
        fix_coinc[x] = "".join(fix_coinc[x])
    fix_coinc = "/".join(fix_coinc)
    
    return " ".join((fix_coinc, (lambda turn: "w" if turn else "b")(turn)))
            