#!/usr/bin/env python3


import random
import os
import time

from graphics import *


settings = {
    "window_x": 700,
    "window_y": 800,
    "header_y": 100,
    "border_x": 10,
    "border_y": 10,
    "board_x": 8,
    "board_y": 8,
    "color_a": "black",
    "color_b": "white",
    "color_b2": "gray",
    "color_c": "red",
    "color_c2": "red4",
    "color_d": "yellow",
    "debug": False,
}


## CURRENT ISSUES ##
## Need to allow for multi-jumps ##
## Perhaps, after a capture is made, look for further captures? ##


## Works perfectly ##
def init():
    clear()
    print("Welcome!\n")
    time.sleep(2)
    clear()

    
## Works perfectly ##
def clear():
    os.system("clear")

    
## Works perfectly ##
def main():
    ## Open window, gather window variables ##
    window = draw_window()
    center_x,center_y,x1,x2,y1,y2 = calculate_grid()
    
    ## Draw grid and boxes ##
    draw_grid_outline(window,x1,x2,y1,y2)
    boxes = draw_grid(window,x1,x2,y1,y2)
    pass
    
    ## Draw pieces ##
    pieces = setup_checkers(window,boxes)
    info_boxes = draw_info_boxes(window)
    
    ## Initiate play, starting with Player A ##
    play = True
    turn = "a"
    info_boxes["center"]["txt"].setText("<-- Player A to move")
    update()
    ## Main game loop ##
    while play:
        ## Main game function ##
        ## move_made returns True is player made a valid move ##
        ## If no valid move made, then turn does not end yet ##
        move_made = check_click(window,boxes,turn,pieces,info_boxes)
        ## Swap turns after main function ##
        if move_made:
            if turn == "a":
                turn = "b"
                info_boxes["center"]["txt"].setText("Player B to move  -->")
            else:
                turn = "a"
                info_boxes["center"]["txt"].setText("<--  Player A to move")
            update()
        who_won = check_for_win(pieces)
        if who_won != "":
            play = False
    victory(window,info_boxes,who_won)
    ## When play becomes False, loop ends, and proceed with function ##
    undraw_window(window)
    
    
## Works perfectly ##
def victory(window,info_boxes,who_won):
    info_boxes["center"]["txt"].setText("Side "+who_won.upper()+" has won the game!!")
    update()
    time.sleep(2)
    
    
## Works perfectly ##
def check_for_win(pieces):
    ## Counts pieces per side ##
    ## If a side has no pieces, then return the other side ##
    who_won = ""
    a_pieces = 0
    b_pieces = 0
    
    for piece in pieces:
        if piece["side"] == "a":
            a_pieces += 1
        elif piece["side"] == "b":
            b_pieces += 1
    if a_pieces == 0:
        who_won = "b"
    elif b_pieces == 0:
        who_won = "a"
    return(who_won)

    
## Works perfectly ##
## Very verbose ##
## Could do with simplification and loops ##
def draw_info_boxes(window):
    ## Info boxes sit above the gamefield and give the user information ##
    ## Information on how the game is proceeding, whose turn it is, etc ##
    to_draw = []
    
    ## Find center of header space ##
    header_center_x = settings["window_x"] / 2
    header_center_y = settings["header_y"] / 2
    
    ## Calculate the corners (Points) of each of the three boxes ##
    left_box_x1 = settings["border_x"]
    left_box_x2 = settings["header_y"]
    left_box_y1 = settings["border_y"]
    left_box_y2 = settings["header_y"]
    
    cntr_box_x1 = settings["border_x"] + settings["header_y"]
    cntr_box_x2 = settings["window_x"] - settings["border_x"] - settings["header_y"]
    cntr_box_y1 = settings["border_y"]
    cntr_box_y2 = settings["header_y"]
    
    right_box_x1 = settings["window_x"] - settings["header_y"]
    right_box_x2 = settings["window_x"] - settings["border_x"]
    right_box_y1 = settings["border_y"]
    right_box_y2 = settings["header_y"]
    
    ## Create the box objects ##
    left_box_obj = Rectangle(Point(left_box_x1,left_box_y1),Point(left_box_x2,left_box_y2))
    cntr_box_obj = Rectangle(Point(cntr_box_x1,cntr_box_y1),Point(cntr_box_x2,cntr_box_y2))
    right_box_obj = Rectangle(Point(right_box_x1,right_box_y1),Point(right_box_x2,right_box_y2))
    
    ## Add properties to the box objects ##
    ## Could use a loop to reduce number of lines of code ##
    left_box_obj.setFill(settings["color_c"])
    left_box_obj.setOutline("black")
    left_box_obj.setWidth(2)
    right_box_obj.setFill(settings["color_b"])
    right_box_obj.setOutline("black")
    right_box_obj.setWidth(2)
    cntr_box_obj.setFill(settings["color_a"])
    cntr_box_obj.setOutline("black")
    cntr_box_obj.setWidth(2)
    
    ## Create text objects to sit on top of boxes ##
    ## Could use a loop to reduce number of lines of code ##
    left_box_center_x = (left_box_x1 + left_box_x2) / 2
    left_box_center_y = (left_box_y1 + left_box_y2) / 2
    left_box_txt = Text(Point(left_box_center_x,left_box_center_y),"")
    left_box_txt.setSize(18)
    cntr_box_center_x = (cntr_box_x1 + cntr_box_x2) / 2
    cntr_box_center_y = (cntr_box_y1 + cntr_box_y2) / 2
    cntr_box_txt = Text(Point(cntr_box_center_x,cntr_box_center_y),"")
    cntr_box_txt.setTextColor(settings["color_b"])
    right_box_center_x = (right_box_x1 + right_box_x2) / 2
    right_box_center_y = (right_box_y1 + right_box_y2) / 2
    right_box_txt = Text(Point(right_box_center_x,right_box_center_y),"")
    right_box_txt.setSize(18)
    
    ## Add box objects to draw queue ##
    ## Could use a loop to reduce number of lines of code ##
    to_draw.append(left_box_obj)
    to_draw.append(cntr_box_obj)
    to_draw.append(right_box_obj)
    to_draw.append(left_box_txt)
    to_draw.append(cntr_box_txt)
    to_draw.append(right_box_txt)
    
    ## Draw each item, then update screen after all have been drawn ##
    for item in to_draw:
        item.draw(window)
    update()
    
    ## Make verbose dictionaries with all necessary box controls ##
    ## Allows changes to boxes and text at runtime ##
    info_boxes = {
        "left": {
            "obj": left_box_obj,
            "txt": left_box_txt,
        },
        "center": {
            "obj": cntr_box_obj,
            "txt": cntr_box_txt,
        },
        "right": {
            "obj": right_box_obj,
            "txt": right_box_txt,
        },
    }
    
    ## Return dictionaries ##
    return(info_boxes)
    
    
## Works perfectly ##
def calculate_grid():
    ## Determine how big the playfield will be ##
    ## Determine how big each grid square should be ##
    ## First, find the center of the grid box outline ##
    center_x = settings["window_x"] / 2
    center_y = (settings["window_y"] / 2) - settings["header_y"]
    
    ## Define the corners of the grid outline ##
    ## x1, y1 becomes Point 1 ##
    ## x2, y2 becomes Point 2 ##
    x1 = settings["border_x"]
    y1 = settings["border_y"] + settings["header_y"]
    x2 = settings["window_x"] - settings["border_x"]
    y2 = settings["window_y"] - settings["border_y"]
    return(center_x,center_y,x1,x2,y1,y2)
    
    
## Works perfectly ##
def draw_grid_outline(window,x1,x2,y1,y2):
    ## Draw the big rectangle around the whole playfield ##
    gridbox = Rectangle(Point(x1,y1),Point(x2,y2))
    gridbox.draw(window)
    update()
    
    
## Works perfectly ##
def draw_grid(window,x1,x2,y1,y2):
    ## Taking calculate points, draw the individual squares that make up the grid ##
    ## Determine how tall and wide the outline box is ##
    outline_x = x2 - x1
    outline_y = y2 - y1
    
    ## Divide that by how many grid lines we need to draw ##
    ## 8 rows means 7 grid lines, since the border counts for top and bottom grid lines ##
    ## Should give the width/height of each grid square ##
    grid_x = outline_x / (8 - 0)
    grid_y = outline_y / (8 - 0)
    
    ## Prepare lists for iteration ##
    grid_x_list = []
    grid_y_list = []
    to_draw = []
    boxes = []
    ## Use "odd" bool to alternate black and white boxes ##
    odd = False
    
    ## Calculate the Points of each X and Y grid line ##
    ## Using a loop for this because programming 64 squares individually in insane ##
    for y in range(0,8):
        ## Since there is an even number of boxes, alternate at top of each column ##
        ## This ensures that we have alternating A and B colored squares ##
        if odd:
            odd = False
        else:
            odd = True
        for x in range(0,8):
            new_rect_x1 = (x*grid_x) + settings["border_x"]
            new_rect_x2 = ((x+1)*grid_x) + settings["border_x"]
            new_rect_y1 = (y*grid_y) + settings["border_y"] + settings["header_y"]
            new_rect_y2 = ((y+1)*grid_y) + settings["border_y"] + settings["header_y"]
            
            center_x = (new_rect_x1 + new_rect_x2) / 2
            center_y = (new_rect_y1 + new_rect_y2) / 2
            
            radius = ((new_rect_x2 - new_rect_x1) / 2) - settings["border_x"]

            new_rect = Rectangle(Point(new_rect_x1,new_rect_y1),Point(new_rect_x2,new_rect_y2))
            ## Use bool to determine box color, then switch bool ##
            if odd:
                new_rect.setFill(settings["color_b"])
                odd = False
                color = settings["color_b"]
            else:
                new_rect.setFill(settings["color_a"])
                odd = True
                color = settings["color_a"]
            to_draw.append(new_rect)
            boxes.append({
                "x": x,
                "y": y,
                "odd": odd,
                "side": "",
                "center_x": center_x,
                "center_y": center_y,
                "radius": radius,
                "obj": new_rect,
                "color": color,
            })
        
    for item in to_draw:
        item.draw(window)
        
    update()
    return(boxes)


## Works perfectly ##
## A bit verbose ##
## Can it be simplified? ##
def setup_checkers(window,boxes):
    ## Prepare the window with all the visuals needed to play the game ##
    ## In this case, preparing and drawing the game pieces on the board ##
    
    ## Pieces are placed only on "odd" squares ##
    ## Pieces are placed one at a time, sequentially per side ##
    ## Starting from top-left, then placing pieces on "odd" squares until all pieces placed ##
    to_draw = []
    pieces_per_side = 12
    pieces_made = 0
    pieces = []
    
    ## Start with Player A, at the top ##
    ## Draw the piece, then mark the square with player name ##
    for box in boxes:
        if box["odd"] and pieces_made < pieces_per_side:
            piece = Circle(Point(box["center_x"],box["center_y"]),box["radius"])
            piece.setFill(settings["color_c"])
            pieces_made += 1
            to_draw.append(piece)
            box["side"] = "a"
            pieces.append({
                "x": box["x"],
                "y": box["y"],
                "obj": piece,
                "side": "a",
                "center_x": box["center_x"],
                "center_y": box["center_y"],
                "level": 0,
            })
    
    ## Then to Player B, at the bottom ##
    ## Build a new list from the old list in reverse ##
    ## Instead of appending boxes to the end of list, insert them at beginning ##
    pieces_made = 0
    boxes_reversed = []
    for box in boxes:
        boxes_reversed.insert(0,box)
    
    ## Iterate through list, placing pieces at appropriate squares ##
    ## Pieces are placed one at a time, starting from bottom-right and proceeding in reverse ##
    for box in boxes_reversed:
        if box["odd"] and pieces_made < pieces_per_side:
            piece = Circle(Point(box["center_x"],box["center_y"]),box["radius"])
            piece.setFill(settings["color_b"])
            pieces_made += 1
            to_draw.append(piece)
            ## Mark the box so we know whose piece is there ##
            box["side"] = "b"
            ## Create a dictionary with all relevant info about each piece ##
            pieces.append({
                "x": box["x"],
                "y": box["y"],
                "obj": piece,
                "side": "b",
                "center_x": box["center_x"],
                "center_y": box["center_y"],
                "level": 0,
            })
            
    ## Draw all pending objects ##
    for item in to_draw:
        item.draw(window)
    ## Draw the screen ##
    update()
    ## Compile boxes for complete list ##
    boxes = combine_boxes(boxes,boxes_reversed)
    for box in boxes:
        #print(box)
        pass
    return(pieces)


## Works perfectly ##                  
def combine_boxes(boxes,boxes_reversed):
    for box in boxes:
        for box_r in boxes_reversed:
            ## If the x and y coords match, then it is the same box ##
            if box["x"] == box_r["x"] and box["y"] == box_r["y"]:
                if box["side"] == "" and box_r["side"] != "":
                    box["side"] = box_r["side"]
    return(boxes)


## Works perfectly ##
def update_scores(window,info_boxes,pieces):
    ## Count how many pieces per side ##
    ## Visually display number of pieces per side in info boxes ##
    pcs = {"a": 0, "b": 0}
    for piece in pieces:
        if piece["side"] == "a":
            pcs["a"] += 1
        elif piece["side"] == "b":
            pcs["b"] += 1
    info_boxes["left"]["txt"].setText(str(pcs["a"]))
    info_boxes["right"]["txt"].setText(str(pcs["b"]))
    update()
    

## Works perfectly ##
def check_for_upgrade(piece,boxes):
    ## After a piece has moved, check if it made it to opposing end zone ##
    ## If it did make it, then it becomes level 1 ##
    ## Level 1 allows it to move backwards, as well as forwards ##
    if piece["side"] == "b" and piece["y"] == 0 and piece["level"] == 0:
        piece["level"] = 1
        piece["obj"].setFill(settings["color_b2"])
    if piece["side"] == "a" and piece["y"] == (settings["board_y"] - 1) and piece["level"] == 0:
        piece["level"] = 1
        piece["obj"].setFill(settings["color_c2"])
    return(piece)


## Works well enough for now ##
def check_click(window,boxes,turn,pieces,info_boxes):
    ## Controlling function that interprets player input ##
    ## Take clickpoint and determine which square was clicked on ##
    ## Highlight selected box ##
    ## If piece belongs to player, then check_for_move ##
    ## If piece belongs to opponent, or no piece present, then do nothing: wait for next click ##
    ## After all sub-functions complete, then: ##
    ## Reset all boxes to original color (aka unhighlight all boxes) ##
    if settings["debug"]:
        print("\nv START check_click")
        print("Waiting for player input...\n")
        
    ## Update scoreboard for players benefit ##
    update_scores(window,info_boxes,pieces)
    
    ## Wait for player to click a box ##
    clickPoint = window.getMouse()
    moved = False

    ## Pass clickPoint to which_box, which returns the box that was clicked upon ##
    box = which_box(clickPoint,boxes)
    if box != None:
            ## If a match is found, proceed with the function ##
            ## Highlight selected box ##
            box["obj"].setFill(settings["color_d"])
            update()
            ## If it is the piece of the current player, check for move ##
            if box["side"] == turn:
                if settings["debug"]:
                    print("This piece belongs to you")
                for piece in pieces:
                    if piece["x"] == box["x"] and piece["y"] == box["y"]:
                        piece,moved = check_for_move(window,boxes,box,piece,pieces,turn)
            elif box["side"] != "":
                #print("This piece belongs to your opponent")
                pass
            else:
                #print("There is no piece here.")
                pass
            
            ## Unhighlight selected box ##
            if box["odd"]:
                box["obj"].setFill(settings["color_a"])
            else:
                box["obj"].setFill(settings["color_b"])
            update()
    update_scores(window,info_boxes,pieces)
    if settings["debug"]:
        print("^ END check_click\n")
    return(moved)


## Takes a clickPoint and the boxes list ##
## Returns the box that was clicked upon, or None if no box was clicked ##
def which_box(clickPoint,boxes):
    for box in boxes:
        if (clickPoint.getX() >= box["center_x"] - box["radius"]) and (clickPoint.getX() <= box["center_x"] + box["radius"]) and (clickPoint.getY() >= box["center_y"] - box["radius"]) and (clickPoint.getY() <= box["center_y"] + box["radius"]):
            return(box)
    return(None)


## Player has clicked on a piece that they own ##
## They have not yet committed to moving this piece ##
## But we need to show them what moves are possible with this piece ##
def check_for_move(window,boxes,start_box,piece,pieces,turn):
    ## Player has selected a piece that they own ##
    ## Highlight the squares that this particular piece can move to ##
    if settings["debug"]:
        print("\nvv STARTING check_for_move\n")

    moved = False
    multijump = False
    capture_jump = ""
    can_capture_list = []
    
    ## Returns several lists ##
    ## Surely we can reduce this number ##
    ## capture_jump_list is used to determine which pieces can be jumped over
    ## to_flash is used to determine which squares to highlight
    ## can_jump_to is used to identify where piece ends up after jump
    ## can_capture is used to identify which piece to remove from board
    capture_jump_list,to_flash,can_jump_to,can_capture,where,multijump = scan_boxes(
        window,boxes,start_box,piece,turn,pieces)
    can_capture_list.append(can_capture)
    
    #try:
    #    if multijump:
    #        capture_jump_list2,to_flash2,can_jump_to2,can_capture2,where2,multijump = scan_boxes(
    #            window,boxes,can_jump_to,piece,turn,pieces)
    #    capture_jump_list = capture_jump_list + capture_jump_list2
    #    can_capture_list.append(can_capture2)
    #except:
    #    pass
    
    if settings["debug"]:
        print("\nto_flash before appending jump_to: "+str(to_flash))
    
    ## If there is anything in capture_jump_list, then add it to to_flash list ##
    ## parts of capture_jump_list are merged into to_flash list ##
    for capture_jump in capture_jump_list:
        if len(capture_jump) > 0:
            if len(capture_jump["jump_to"]) > 0:
                to_flash.append(capture_jump["jump_to"])
                
    if settings["debug"]:
        print("to_flash after appending jump_to: "+str(to_flash)+"\n")
    if settings["debug"]:
        print("\nto_flash: "+str(to_flash))
        
    ## All possible moves have been determined and copied to to_flash ##
    ## Highlight these boxes to show user what they can do ##
    if len(to_flash) > 0:
        for box in to_flash:
            box["obj"].setFill(settings["color_d"])
        update()
        
        ## Now that possible moves are highlighted, allow player to click something ##
        ## If they click a valid box, then return the info ##
        piece,boxes,moved,jumped = move_piece(
            window,boxes,piece,to_flash,start_box,turn,capture_jump_list)
        
        if jumped != "":
            pass
        
        if settings["debug"]:
            print("\n**CONTINUE check_for_move\n")
            print("move_piece returned the following data:")
            print("piece: "+str(piece))
            print("boxes: (truncated due to lots of data)")
            print("moved: "+str(moved))
            print("capture_jump: "+str(capture_jump))
            print("len(capture_jump): "+str(len(capture_jump))+"\n")
            print("jumped: "+str(jumped))
            print("can_capture: "+str(can_capture))
            
        for can_capture in can_capture_list:
            if (len(can_capture) > 0 and moved) and (len(capture_jump) > 0) and jumped != "":
                for can_cap in can_capture:
                    if (jumped["x"] == can_cap["x"] and jumped["y"] == can_cap["y"]):
                        if settings["debug"]:
                            print("can_cap: "+str(can_cap))
                        pieces.remove(can_cap)
                        can_cap["obj"].undraw()
                        can_capture.remove(can_cap)

                        for box_a in boxes:
                            if can_cap["x"] == box_a["x"] and can_cap["y"] == box_a["y"]:
                                box_a["side"] = ""
                    
        ## After choice is made, remove flash effect ##
        time.sleep(0.2)
        for box in to_flash:
            if box["side"]:
                box["obj"].setFill(box["color"])
            else:
                box["obj"].setFill(box["color"])
        update()
    ## If no boxes are available to move to, then cancel ##
    else:
        if settings["debug"]:
            print("No moves available")
        
    if settings["debug"]:
        print("^^ END check_for_move\n")
    return(piece,moved)


def scan_boxes(window,boxes,start_box,piece,turn,pieces):
    ## Takes a start_box and piece to determine starting position
    ##
    ## GOAL: reduce output to a single list: possible_moves ##
    ##
    ## Presently, returns all of the following:
    ## Returns to_flash: a list of boxes to hightlight
    ## ## ["end"] in each possible_moves becomes to_flash
    ##
    ## Returns capture_jump_list: a list of dictionaries that relates a box containing an...
    ## ... opposing piece with the box behind it, which the piece can jump to ##
    ## Returns can_jump_to: a single box, which is behind an opposing piece ##
    ## ## can_jump_to comes from capture_jump_list
    ## Returns can_capture: a piece that is to be removed from the board ##
    ## ## can_capture comes from capture_jump_list
    ## Returns where: a list of strings that describe directional relation to opposing pieces ##
    
    ## Piece level determines which directions piece can move
    ## Scans boxes adjacent to start_box, looking for opposing pieces
    ## For each opposing piece, we run check_for_jump
    ## ## check_for_jump returns to tell if opposing piece can be jumped
    ## ## If opposing piece can be jumped, add it to list of possible moves
    
    ## Get basic coordinates for possible basic moves ##
    ## Function will check to see if these squares are open ##
    to_flash = []
    can_jump_to = []
    can_capture = []
    capture_jump = {}
    capture_jump_list = []
    where = []
    possible_moves = []
    moved = False
    jumped = False
    multijump = False
    
    ## Calculate what coordinates are adjacent to coordinates of selected box ##
    left = start_box["x"] - 1
    right = start_box["x"] + 1
    above = start_box["y"] - 1
    below = start_box["y"] + 1
    #left = piece["x"] - 1
    #right = piece["x"] + 1
    #above = piece["y"] - 1
    #below = piece["y"] + 1
    
    ## How to prevent level 0 pieces from moving backwards? ##
    ## Side A moves down; Side B moves up ##
    if piece["level"] == 0:
        if piece["side"] == "a":
            above = -1
        elif piece["side"] == "b":
            below = -1
            
    ## Iterate through list of boxes ##
    ## If both X and Y coordinates match a box in the list: ##
    ## Inspect the box and check if it is empty, or contains an opposing piece ##
    ## While multijump == True loop? ##
    for box in boxes:
        ## Make sure the X variable matches ##
        if (box["x"] == left) or (box["x"] == right):
            ## Make sure the Y variable matches too ##
            if (box["y"] == below) or (box["y"] == above):
                ## If adjacent box is empty, then a move is possible ##
                ## In this case, add the box to the to_flash list ##
                if box["side"] == "":
                    if settings["debug"]:
                        print("Moves available!")
                    to_flash.append(box)
                    
                    possible_moves.append(
                        {"type": "basic", "start": start_box, "end": box, "mid": None,})
                    
                ## If adjacent box contains an opposing piece, then capture is possible ##
                ## Capturable pieces added to can_capture list ##
                ## What if I had a piece of data that contained the capturable piece as well
                ## ## as the box which they would need to jump to to capture it ##
                elif box["side"] != turn:
                    if settings["debug"]:
                        print("Opposing piece adjacent!")
                    ## Then caulculate where piece would end up after capture ##
                    ## And check if further jumps are possible ##
                    ## Can I use recursion here? ##
                    if box["x"] == left and box["y"] == below:
                        where.append("left below")
                    elif box["x"] == left and box["y"] == above:
                        where.append("left above")
                    elif box["x"] == right and box["y"] == below:
                        where.append("right below")
                    elif box["x"] == right and box["y"] == above:
                        where.append("right above")
                    ## Get the square that the piece can jump to ##
                    can_jump_to = check_for_jump(boxes,start_box,box,piece,turn,where)
                    ## Check if can_jump_to is empty or not ##
                    if can_jump_to == []:
                        if settings["debug"]:
                            print("can_jump_to is empty!")
                    ## Package the square that can be jumped and the one that can be jumped to
                    else:                
                        to_box = box.copy()
                        
                        capture_jump = {"to_jump": to_box, "jump_to": can_jump_to}
                        capture_jump_list.append(capture_jump)

                        if settings["debug"]:
                            print('capture_jump["to_jump"]'+str(capture_jump["to_jump"]))
                            print('capture_jump["jump_to"]'+str(capture_jump["jump_to"]))
                            print("can_jump_to is NOT empty")
                        #multijump = True
                        
                        possible_moves.append(
                            {"type": "jump", "start": start_box, "end": can_jump_to, "mid": to_box,})
                    
                    ## How to remove captured piece from the board? ##
                    ## Store jumpable piece info ##
                    for p in pieces:
                        if p["x"] == box["x"] and p["y"] == box["y"]:
                            can_capture.append(p)
    print("\n-----\nPossible Moves:")
    for move in possible_moves:
        print(str(move)+"\n")
    return(capture_jump_list,to_flash,can_jump_to,can_capture,where,multijump)


## For multi-jumps, perhaps re-run this function with a new start_box and jump_box? ##
def check_for_jump(boxes,start_box,jump_box,piece,turn,where_list):
    ## Takes a start_box (players selected piece) and a jump_box (adjacent opposing piece) ##
    ## Returns a single square behind the piece to be jumped ##
    ## If nothing is returned, then no jump is possible ##
    ## Start_box is where the piece starts, jump_box is the box with the opposing piece ##
    if settings["debug"]:
        print("\nvvvv START check_for_jump\n")
    ## Player has selected a piece that they own ##
    ## Chosen piece is adjacent to opposing pieces ##
    ## Highlight the boxes they can jump to behind the opposing piece ##
    can_jump_to = []
    
    ## Use "where" string to determine which box to inspect ##
    ## Maybe make it a list that is iterated through ##
    if settings["debug"]:
        print("where list: "+str(where_list))
    for where in where_list:
        if where == "left below":
            target_x = jump_box["x"] - 1
            target_y = jump_box["y"] + 1
        elif where == "left above":
            target_x = jump_box["x"] - 1
            target_y = jump_box["y"] - 1
        elif where == "right below":
            target_x = jump_box["x"] + 1
            target_y = jump_box["y"] + 1
        elif where == "right above":
            target_x = jump_box["x"] + 1
            target_y = jump_box["y"] - 1
    
        ## Check each box to see if we have any matches ##
        for box in boxes:
            ## If the coordinates match and box is empty ##
            if target_x == box["x"] and target_y == box["y"] and box["side"] == "" and (
                target_x != piece["x"] and target_y != piece["y"]):
                can_jump_to = box
    if settings["debug"]:
        print("****can_jump_to: "+str(can_jump_to))
        print("^^^^ END check_for_jump\n")
    return(can_jump_to)
## Returns list can_jump_to, which can have 0 or 1 elements ##


def get_player_move(window,boxes,to_flash,clickPoint):
    for box in boxes:
        if (clickPoint.getX() >= box["center_x"] - box["radius"]) and (clickPoint.getX() <= box["center_x"] + box["radius"]) and (clickPoint.getY() >= box["center_y"] - box["radius"]) and (clickPoint.getY() <= box["center_y"] + box["radius"]) and (box in to_flash):
            return(box)
    return(None)

        
## All possible moves are highlighted: now let player click on one of them ##
def move_piece(window,boxes,piece,to_flash,start_box,turn,capture_jump_list):
    if settings["debug"]:
        print("\nvvv START move_piece\n")
        
    ## Player has selected a piece that they own ##
    ## Player can cancel the move at this point ##
    ## clickPoint returns the coordinates that were clicked on ##
    clickPoint = window.getMouse()
    moved = False
    jumped = ""
    
    ## Take clickPoint and see if it matches any of the boxes ##
    ## Return the box if it does -- return None if it doesn't ##
    box = get_player_move(window,boxes,to_flash,clickPoint)
    
    ## Make sure a box was returned ##
    if box != None:
        ## How to check if box selected is a multijump? ##
        
        
        
        ## Using returned box, gather info ##
        box_x = box["center_x"]
        box_y = box["center_y"]
        piece_x = piece["center_x"]
        piece_y = piece["center_y"]

        ## Calculate how far the piece will move visually  ##
        move_x = box_x - piece_x
        move_y = box_y - piece_y

        ## Visually move the piece object ##
        piece["obj"].move(move_x,move_y)

        ## Update the pieces coordinates ##
        piece["x"] = box["x"]
        piece["y"] = box["y"]
        piece["center_x"] = piece["obj"].getCenter().getX()
        piece["center_y"] = piece["obj"].getCenter().getY()

        ## Update the box itself with side(team) info ##
        start_box["side"] = ""
        box["side"] = turn
        update()
        moved = True

        ## Check if a piece was jumped ##
        try:
            jumped = which_jumped(boxes,start_box,box,capture_jump_list)
        except:
            jumped = ""
        ## Jumped may be returned as "", in which case nothing was jumped ##
        if jumped != "":
            pass

        piece = check_for_upgrade(piece,boxes)
            
    if settings["debug"]:
        print("^^^ END move_piece\n")

    return(piece,boxes,moved,jumped)


## Called by move_piece ##
## Player has made their move, we have start_box and end_box ##
## >> We also need a jump_sequence list, with each start_box and end_box ##
## Now we determine which piece was jumped over ##
## Iterate through capture_jump_list and try to match up a ["to_jump"] box with mid_box ##
def which_jumped(boxes,start_box,end_box,capture_jump_list):
    jumped = ""
    if settings["debug"]:
        print("\nvvvvv START which_jumped")
        for capture_jump in capture_jump_list:
            print("capture_jump: "+str(capture_jump))
    jump_sequence = []
    ## Maybe a list of mid-boxes? ##
    #for jump in jump_sequence:
    #    print(jump)
    mid_box = calculate_mid_box(start_box,end_box)
    #    if jump["capture_box"] == mid_box:
    #        print("capture box found successfully")
    ## Iterate through list ##
    for capture_jump in capture_jump_list:
        ## Only continue if list item is not empty ##
        if len(capture_jump) > 0:
            ## Try to match up mid_box x and y with capture_jump["to_jump"] ##
            if mid_box["x"] == capture_jump["to_jump"]["x"] and mid_box["y"] == capture_jump["to_jump"]["y"]:
                ## If a match is found, then copy box info to jumped ##
                jumped = mid_box
    if settings["debug"]:
        print("\v^^^^^ END which_jumped")
    ## Return box that was jumped, or "" if none was jumped ##
    return(jumped)


def which_jumped_backup(boxes,start_box,end_box,capture_jump_list):
    jumped = ""
    if settings["debug"]:
        print("\nvvvvv START which_jumped")
        for capture_jump in capture_jump_list:
            print("capture_jump: "+str(capture_jump))
    mid_box = calculate_mid_box(jump["start_box"],jump["end_box"])
    ## Iterate through list ##
    for capture_jump in capture_jump_list:
        ## Only continue if list item is not empty ##
        if len(capture_jump) > 0:
            ## Try to match up mid_box x and y with capture_jump["to_jump"] ##
            if mid_box["x"] == capture_jump["to_jump"]["x"] and mid_box["y"] == capture_jump["to_jump"]["y"]:
                ## If a match is found, then copy box info to jumped ##
                jumped = mid_box
    if settings["debug"]:
        print("\v^^^^^ END which_jumped")
    ## Return box that was jumped, or "" if none was jumped ##
    return(jumped)


## Takes a box_jump sequence and returns a list of boxes captured during the sequence ##
## box_jump_sequence is a list of dictionaries ##
    ## [{"start_box": box, "end_box": box,},{"start_box": box, "end_box": box,},]
def calculate_jumps(box_jump_sequence):
    to_capture = []
    ## Take each step, find the mid_box, and add it to a list ##
    for box_jump in box_jump_sequence:
        mid_box = calculate_mid_box(box_jump["start"],box_jump["end"])
        to_capture.append(mid_box)
    return(to_capture)
        

## Takes a start and end box, and finds the box between them: mid_box ##
## Works best if boxes are 45 degrees diagonal and have 1 box between them ##
def calculate_mid_box(start_box,end_box):
    mid_box = {"x": 0, "y": 0}
    mid_box["x"] = (start_box["x"] + end_box["x"]) / 2
    mid_box["y"] = (start_box["y"] + end_box["y"]) / 2
    return(mid_box)


def check_for_multijump(boxes,start_box,piece):
    ## THEORY ##
    ## To check for multijump, recieve a start_box and piece ##
    ## start_box is the pieces position after a jump ##
    ## Scan boxes adjacent to the start_box ##
    ## If an opposing piece is adjacent, in correct direction if level 0: set multijump to True
    if settings["debug"]:
        print("check_for_multijump received:")
        print("boxes")
        print("start_box: "+str(start_box))
    multijump = False
    ## Need a function that does the following: ##
    ## Takes a start_box and side, and returns a capture_jump_list ##
    for box in boxes:
        if start_box["x"] == box["x"] and start_box["y"] == box["y"]:
            print("Looking for jumps starting at "+str(box["x"])+","+str(box["y"]))
            direction = direction_to_piece(start_box,box)
            print(direction)
    return(multijump)


## Takes a start_box and end_box, returns a string describing direction from start to end ##
def direction_to_piece(boxes,start_box,end_box):
    dir_x = ""
    dir_y = ""
    diff_x = end_box["x"] - start_box["x"]
    diff_y = end_box["y"] - start_box["y"]
    if diff_x < 0:
        dir_x = "left"
    elif diff_x > 0:
        dir_x = "right"
    if diff_y < 0:
        dir_y = "above"
    elif diff_y > 0:
        dir_y = "below"
    direction = dir_x+" "+dir_y
    return(direction)


## Receives a start_box and a piece for side reference ##
## Returns a list of adjacent opposing pieces ##
def test_adjacent_opposing_pieces(boxes,piece,start_box):
    turn = piece["side"]
    opposing_boxes = []
    ## Calculate what coordinates are adjacent to coordinates of selected box ##
    left = piece["x"] - 1
    right = piece["x"] + 1
    above = piece["y"] - 1
    below = piece["y"] + 1
    ## To prevent level 0 pieces from moving backwards ##
    ## Side A moves down; Side B moves up ##
    if piece["level"] == 0:
        if piece["side"] == "a":
            above = -1
            opposing = "b"
        elif piece["side"] == "b":
            below = -1
            opposing = "a"
    ## Iterate through box list, find boxes adjacent to start_box ##
    for box in boxes:
        ## If box contains an opposing piece ##
        if box["side"] == opposing:
            ## Match coordinates and store in list ##
            if box["x"] == left and box["y"] == below:
                opposing_boxes.append(box)
            elif box["x"] == left and box["y"] == above:
                opposing_boxes.append(box)
            elif box["x"] == right and box["y"] == below:
                opposing_boxes.append(box)
            elif box["x"] == right and box["y"] == below:
                opposing_boxes.append(box)
    return(opposing_boxes)
    

## Receives a start_box and a piece for side reference ##
## Returns a list of possible capture jumps ##
def test_create_capture_jump_list(boxes,piece,start_box):
    side = piece["side"]
    check_box = ""
    turn = side
    
    
    for box in boxes:
        if box["x"] == start_box["x"] and box["y"] == start_box["y"]:
            check_box = box
    
    to_flash = check_for_jump(boxes,start_box,check_box,piece,turn,where_list)
    
    
## Works perfectly ##
## Text is not really readable though ##
## Could use a background box to make text readable ##
def draw_text(window,center_x,center_y,text):
    ## Draws black text in the middle of the screen ##
    info_text = Text(Point(center_x,center_y),str(text))
    info_text.draw(window)
    update()
    
    
## Works perfectly ##
def draw_window():
    ## Used to initialize the window ##
    win = GraphWin("Checkers", settings["window_x"], settings["window_y"], autoflush=False)
    return(win)


## Works perfectly ##
def undraw_window(win):
    ## Undraw, close the window ##
    win.close()

    
## Works perfectly ##
def farewell():
    ## Clear the screen, print farewell, pause to let user read, then clear again ##
    clear()
    print("Farewell!\n")
    time.sleep(2)
    clear()


## Function stack ##
init()
main()
farewell()
