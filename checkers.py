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
    "debug": True,
}


## CURRENT ISSUES ##
## Level 1 red piece unable to find a 2 jump when there are 2 different jump directions available ##
## Level 1 red piece unable to find a 3 jump when there are 2 different jump directions after a 1 jump ##
## Does not find multijumps beyond 3 jumps ##
## Does not find 3+ jumps if there are multiple 2 jumps available ##
## Where paths diverge, only 1 additional jump is shown ##
## Maybe go back to jump_path_list idea?  Sorta like in CarPG? ##


## RECENTLY FIXED ISSUE: CHECK TO MAKE SURE IT IS FULLY FIXED ##
## Can make multijumps, however:
## In multijumps using a level 1 piece, the first jumped piece is very often not removed ##
## Somehow the first jumped piece is not added to kill list ##
## ## It appears that kill list only ever contains one element!  It should be able to contain more ##
## This does occur when making multijumps with a level 0 piece ##
## ## For level 0 pieces, the first and second jumps work fine.  After that, further pieces not removed ##
## ## For level 1 pieces, the first jump is often not removed, even in 2-jump multijumps ##
## What the hell could cause this??? ##
## Find pieces of code that allude to level and determine how they affect the process stack ##


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


## Works perfectly ##
## Takes a clickPoint and the boxes list ##
## Returns the box that was clicked upon, or None if no box was clicked ##
def which_box(clickPoint,boxes):
    for box in boxes:
        if (clickPoint.getX() >= box["center_x"] - box["radius"]) and (clickPoint.getX() <= box["center_x"] + box["radius"]) and (clickPoint.getY() >= box["center_y"] - box["radius"]) and (clickPoint.getY() <= box["center_y"] + box["radius"]):
            return(box)
    return(None)


## Works perfectly ##
## Takes a click and a single box, and tells if click coords are within box coords ##
## Returns True or False ##
def compare_click(clickPoint,box):
    if (clickPoint.getX() >= box["center_x"] - box["radius"]) and (clickPoint.getX() <= box["center_x"] + box["radius"]) and (clickPoint.getY() >= box["center_y"] - box["radius"]) and (clickPoint.getY() <= box["center_y"] + box["radius"]):
        return(True)
    return(False)


## Works perfectly ##
## Takes two boxes are returns True if they occupy the same coordinates ##
def compare_box_coords(box_a,box_b):
    if box_a["x"] == box_b["x"] and box_a["y"] == box_b["y"]:
        return(True)
    return(False)




## ##

## ##

## ##




## Main function called by main() to progress the game ##
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


## Takes a piece to remove, finds the piece in piece list and removes it ##
## Then finds the box the piece was in and resets the "side" variable ##
## To remove multiple pieces, run this function for each piece ##
def remove_piece(window,boxes,pieces,to_remove):
    for piece in pieces:
        if to_remove["x"] == piece["x"] and to_remove["y"] == piece["y"]:
            piece["obj"].undraw()
            pieces.remove(piece)
    for box in boxes:
        if to_remove["x"] == box["x"] and to_remove["y"] == box["y"]:
            box["side"] = ""
            if settings["debug"]:
                print("side data removed from box")
    return(boxes,pieces)


## Takes a list of possible moves, and check for further possible moves ##
def compile_possible_moves(window,boxes,possible_moves,pieces,piece,turn,kill):
    #kill = []
    further_possible_moves = []
    for possible_move in possible_moves:
        if possible_move["type"] == "jump" or possible_move["type"] == "multi":
            ## kill contains a list of boxes with a piece to be removed during a multijump ##
            if possible_move["mid"] not in kill:
                kill.append(possible_move["mid"])
            if settings["debug"]:
                print("scanning for multijumps from "+str(possible_move["end"]))
            further_possible_moves = scan_boxes(
                window,boxes,possible_move["end"],piece,turn,pieces,True,kill)
    return(further_possible_moves)


## Take list of possible moves and highlights the "end" boxes ##
def calc_to_flash(possible_moves):
    to_flash = []
    for possible_move in possible_moves:
        to_flash.append(possible_move["end"])
    return(to_flash)


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
    to_flash = []
    #kill = ""
    kill = []
    stop_search = False
    
    possible_moves = scan_boxes(window,boxes,start_box,piece,turn,pieces,False,kill)
    to_flash = calc_to_flash(possible_moves)
    
    further_possible_moves = compile_possible_moves(window,boxes,possible_moves,pieces,piece,turn,kill)
    further_to_flash = calc_to_flash(further_possible_moves)
    
    
    while len(further_possible_moves) > 0 and not stop_search:
        for further_possible_move in further_possible_moves:
            ## To prevent infinite loops, as soon as we get a box for a second time, stop the loop ##
            if further_possible_move in possible_moves:
                if settings["debug"]:
                    print("Possible Move already here!  Ending loop manually!")
                stop_search = True
            else:
                if settings["debug"]:
                    print("appending to possible_moves: "+str(further_possible_move))
                possible_moves.append(further_possible_move)
                to_flash.append(further_possible_move["end"])
        further_possible_moves = compile_possible_moves(window,boxes,possible_moves,pieces,piece,turn,kill)
    
    if settings["debug"]:
        print("further possible moves: "+str(further_possible_moves))
    for further_possible_move in further_possible_moves:
        possible_moves.append(further_possible_move)
        to_flash.append(further_possible_move["end"])
        
    if settings["debug"]:
        print("\nCombined possible moves: ")
        for move in possible_moves:
            print(move)
        
    ## All possible moves have been determined and copied to to_flash ##
    ## Highlight these boxes to show user what they can do ##
    if len(to_flash) > 0:
        for box in to_flash:
            box["obj"].setFill(settings["color_d"])
        update()
        
        ## Now that possible moves are highlighted, allow player to click something ##
        ## If they click a valid box, then return the info ##
        piece,pieces,boxes,moved,jumped = move_piece(
            window,boxes,pieces,piece,possible_moves,start_box,turn)
        if settings["debug"]:
            print("jumped: "+str(jumped))

        if jumped != None and jumped != "":
            boxes,pieces = remove_piece(window,boxes,pieces,jumped)
            
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


def scan_boxes(window,boxes,start_box,piece,turn,pieces,multi,kill):
    ## Takes a start_box and piece to determine starting position
    ## GOAL: reduce output to a single list: possible_moves ##
    ## kill contains a box with a piece to be removed during a multijump ##

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
        if (box["x"] == left or box["x"] == right) and (box["y"] == below or box["y"] == above):
            ## If adjacent box is empty, then a move is possible ##
            ## In this case, add the box to the to_flash list ##
            if box["side"] == "" and multi == False:
            #if box["side"] == "" and not multi:
                if settings["debug"]:
                    print("Moves available!")
                to_flash.append(box)
                    
                possible_moves.append(
                    {"type": "basic", "start": start_box, "end": box, "mid": None, "kill": []})
                    
            ## If adjacent box contains an opposing piece, then capture is possible ##
            elif box["side"] != turn and box["side"] != "":
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
                can_jump_to = check_for_jump(boxes,start_box,box,piece,turn,where,multi)
                ## Check if can_jump_to is empty or not ##
                if can_jump_to == []:
                    if settings["debug"]:
                        print("can_jump_to is empty!")
                    ## Package the square that can be jumped and the one that can be jumped to
                else:                
                    if multi:
                        ## Need to make sure start_box and can_jump_to have different x and y
                        if start_box["x"] == can_jump_to["x"] or start_box["y"] == can_jump_to["y"]:
                            pass
                        else:
                            possible_moves.append(
                                {"type": "multi", "start": start_box, "end": can_jump_to, "mid": box, "kill": kill})
                    else:
                        possible_moves.append(
                            {"type": "jump", "start": start_box, "end": can_jump_to, "mid": box, "kill": []})
    if settings["debug"]:                    
        print("\n-----\nPossible Moves:")
        for move in possible_moves:
            print(str(move)+"\n")
    return(possible_moves)


## For multi-jumps, perhaps re-run this function with a new start_box and jump_box? ##
def check_for_jump(boxes,start_box,mid_box,piece,turn,where_list,multi):
    ## Takes a start_box (players selected piece) and a jump_box (adjacent opposing piece) ##
    ## Returns a single square behind the piece to be jumped ##
    ## If nothing is returned, then no jump is possible ##
    ## Start_box is where the piece starts, jump_box is the box with the opposing piece ##
    if settings["debug"]:
        print("\nvvvv START check_for_jump\n")
        print("checking from "+str(start_box["x"])+","+str(start_box["y"]))
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
            target_x = mid_box["x"] - 1
            target_y = mid_box["y"] + 1
        elif where == "left above":
            target_x = mid_box["x"] - 1
            target_y = mid_box["y"] - 1
        elif where == "right below":
            target_x = mid_box["x"] + 1
            target_y = mid_box["y"] + 1
        elif where == "right above":
            target_x = mid_box["x"] + 1
            target_y = mid_box["y"] - 1
    
        ## Check each box to see if we have any matches ##
        for box in boxes:
            ## If the coordinates match, box is empty, and box is not already occupied by piece ##
            if target_x == box["x"] and target_y == box["y"] and box["side"] == "":
                if multi == False and (target_x != piece["x"] and target_y != piece["y"]):
                    can_jump_to = box
                elif multi == True:
                    can_jump_to = box
    if settings["debug"]:
        print("****can_jump_to: "+str(can_jump_to))
        print("^^^^ END check_for_jump\n")
    return(can_jump_to)


## Takes players click coords and compares to possible_moves ##
## Returns list can_jump_to, which can have 0 or 1 elements ##
def get_player_move(window,boxes,possible_moves,clickPoint):
    to_flash = []
    for possible_move in possible_moves:
        to_flash.append(possible_move["end"])
    for box in boxes:
        if compare_click(clickPoint,box) and (box in to_flash):
            return(box)
    return(None)

        
## All possible moves are highlighted: now let player click on one of them ##
def move_piece(window,boxes,pieces,piece,possible_moves,start_box,turn):
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
    box = get_player_move(window,boxes,possible_moves,clickPoint)
    
    ## Make sure a box was returned ##
    if box != None:
        ## ##
        ## ## ## vv VISUAL UPDATE HERE vv ## ## ##
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
        ## ## ## ^^ VISUAL UPDATE HERE ^^ ## ## ##
        ## ##
        
        ## Check if a piece was jumped ##
        jumped,move = which_jumped(boxes,start_box,box,possible_moves)
        ## Jumped may be returned as "", in which case nothing was jumped ##
        if jumped != "" and jumped != None:
            boxes, pieces = remove_piece(window,boxes,pieces,jumped)
            if len(move["kill"]) > 0:
                for to_kill in move["kill"]:
                    boxes, pieces = remove_piece(window,boxes,pieces,to_kill)

        piece = check_for_upgrade(piece,boxes)
            
    if settings["debug"]:
        print("^^^ END move_piece\n")

    return(piece,pieces,boxes,moved,jumped)


## Called by move_piece ##
## Player has made their move, we have start_box and end_box ##
## We scan throguh possible moves list to locate one whose mid-box is between start and end box ##
def which_jumped(boxes,start_box,end_box,possible_moves):
    jumped = ""
    if settings["debug"]:
        print("\nvvvvv START which_jumped")
        for possible_move in possible_moves:
            print("possible_move: "+str(possible_move))

    for possible_move in possible_moves:
        if compare_box_coords(possible_move["end"],end_box):
                jumped = possible_move["mid"]
                move = possible_move
                
    if settings["debug"]:
        print("\v^^^^^ END which_jumped")
    ## Return box that was jumped, or "" if none was jumped ##
    return(jumped,move)

    
    
    

## ##

## ##

## ##

## ##


    



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
    
    
    

## ##

## ##

## ##

## ##


    
    
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
