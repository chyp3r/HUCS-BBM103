import sys

def read_input_file():    
    """
    Returns:
        game_table (str): A game table reading from input file
    """
    with open(sys.argv[1],"r", encoding="utf-8") as f:
        game_table = f.read()
        return game_table
    
def fix_game_table(game_table:str):
    """
    Adapts the given game table to the problem  

    Args:
        game_table (str): A game table given from user 

    Returns:
        fixed_game_table (list): The data in the game table arranged for the given problem. A separate list is created for each row and the elements in the row are placed in these lists
    """
    row_list = list(game_table.split("\n"))
    fixed_game_table = []
    for row in row_list:
        fixed_game_table.append(row.split(" "))
    return fixed_game_table

def concat_domino_pieces(data:str):
    """
    Concats individual domino pieces into a dictionary

    Args:
        data (str): A game table given from user 

    Returns:
        table_map (dict):{"<row_number>-<col_number>":["<item>","<coordinate_of_other_half_of_domino>","<value>"]}     
            item: Describes which part of the domino it is (U, D, L or R)
            value: Describes the value of the domino (H, B, N or i(empty))
    """
    table_map = {}
    row_number = 0
    for row in data:
        col_number = 0
        for item in row:
            if (item == "U"):
                table_map[str(row_number)+"-"+str(col_number)] = [item,str(row_number+1)+"-"+str(col_number),"i"] # Concat the upper part with the downer part in table_map
            if (item == "D"):
                table_map[str(row_number)+"-"+str(col_number)] = [item,str(row_number-1)+"-"+str(col_number),"i"] # Concat the downer part with the upper part in table_map
            if (item == "L"):
                table_map[str(row_number)+"-"+str(col_number)] = [item,str(row_number)+"-"+str(col_number+1),"i"] # Concat the righter part with the lefter part in table_map
            if (item == "R"):
                table_map[str(row_number)+"-"+str(col_number)] = [item,str(row_number)+"-"+str(col_number-1),"i"] # Concat the righter part with the lefter part in table_map
            col_number += 1
        row_number += 1
    return table_map

def test_limits(current_value:str,current_row:str,current_col:str,table_map:dict):
    """
    Checks compliance with neighbor conditions
 
    Args:
        current_value (str): Value to be checked (H B or N) 
        current_row (str): Row of value to be checked
        current_col (str): Column of value to be checed
        table_map (dict): Dictionary created by concat_domino_pieces() function

    Returns:
        True/False (bool): Returns True if the piece can be placed in place, otherwise False. 
    """
    if current_value != "N":
        try:
            if table_map[str(int(current_row)+1)+"-"+current_col][2] == current_value: # Check upper value
                return False        
        except:
            pass
        try:
            if table_map[str(int(current_row)-1)+"-"+current_col][2] == current_value: # Check downer value
                return False        
        except:
            pass
        try:
            if table_map[current_row+"-"+str(int(current_col)+1)][2] == current_value: # Check righter value
                return False        
        except:
            pass
        try:
            if table_map[current_row+"-"+str(int(current_col)-1)][2] == current_value: # Check lefter value
                return False        
        except:
            pass
        return True
    else:
        return True # For N we have not any limit
    
def check_row(row_high_limits:list,row_base_limits:list,table_map:dict):
    """
    Checks compliance with row conditions
 
    Args:
        row_high_limits (list): List showing how many high values ​​should be in the rows (-1: no limit)
        row_base_limits (list): List showing how many base values ​​should be in the rows (-1: no limit)
        table_map (dict): Dictionary created by concat_domino_pieces() function

    Returns:
        True/False (bool): Returns True if all rows match the row limits, otherwise False.
    """   
    for current_row in range(len(row_high_limits)):
        high_count = 0
        counter = 0 # Column number
        if int(row_high_limits[current_row]) != -1:
            while True:
                try:
                    if table_map[str(current_row)+"-"+str(counter)][2] == "H":
                        high_count += 1
                    counter += 1
                except: # Stop end of the row
                    break
            if high_count != int(row_high_limits[current_row]):
                return False
        base_count = 0
        counter = 0 # Column number
        if int(row_base_limits[current_row]) != -1:
            while True:
                try:
                    if table_map[str(current_row)+"-"+str(counter)][2] == "B":
                        base_count += 1
                    counter += 1
                except: # Stop end of the row
                    break
            if base_count != int(row_base_limits[current_row]):
                return False
    return True

def check_col(col_high_limits:list,col_base_limits:list,table_map:dict):
    """
    Checks compliance with column conditions
 
    Args:
        col_high_limits (list): List showing how many high values ​​should be in the columns (-1: no limit)
        col_base_limits (list): List showing how many base values ​​should be in the columns (-1: no limit)
        table_map (dict): Dictionary created by concat_domino_pieces() function

    Returns:
        True/False (bool): Returns True if all columns match the column limits, otherwise False.
    """   
    for current_col in range(len(col_high_limits)):
        high_count = 0
        counter = 0 # Row number
        if int(col_high_limits[current_col]) != -1:
            while True:
                try:
                    if table_map[str(counter)+"-"+str(current_col)][2] == "H":
                        high_count += 1
                    counter += 1
                except: # Stop end of the column
                    break
            if high_count != int(col_high_limits[current_col]):
                return False 
                
        base_count = 0
        counter = 0 # Row number
        if int(col_base_limits[current_col]) != -1:
            while True:
                try:
                    if table_map[str(counter)+"-"+str(current_col)][2] == "B":
                        base_count += 1
                    counter += 1
                except: # Stop end of the column
                    break
            if base_count != int(col_base_limits[current_col]):
                    return False 
    return True # Compliance with all conditions

def find_next_empty_domino(empty_domino:list,table_map:dict):
    """
    Finds the empty piece closest to the top left position among all elements, starting from the top left

    Args:
        table_map (dict): Dictionary created by concat_domino_pieces() function

    Returns:
        True/False (bool): Returns False if empty piece is found, otherwise True
    """   
    for i in table_map:
        if (table_map[i][2] == "i"):
            empty_domino[0] = i.split("-")[0] # Row number of empty domino
            empty_domino[1] = i.split("-")[1] # Column number of empty domino
            return False
    return True

def backtracking_solver(row_high_limits:list,row_base_limits:list,col_high_limits:list,col_base_limits:list,table_map:dict):
    """
    Recursive backtracking algorithm

    Args:
        row_high_limits (list): List showing how many high values ​​should be in the rows (-1: no limit)
        row_base_limits (list): List showing how many base values ​​should be in the rows (-1: no limit)
        col_high_limits (list): List showing how many high values ​​should be in the columns (-1: no limit)
        col_base_limits (list): List showing how many base values ​​should be in the columns (-1: no limit)
        table_map (dict): Dictionary created by concat_domino_pieces() function

    Returns:
        True/False (bool): Returns if all squares are filled and all conditions are met, otherwise False.
    """ 

    next_domino = [0,0] 

    if (find_next_empty_domino(next_domino,table_map)):
        if check_col(col_high_limits,col_base_limits,table_map) and check_row(row_high_limits,row_base_limits,table_map):
            return True # If all squares are filled and all conditions are met
        else:
            return False 
    
    current_row = next_domino[0]
    current_col = next_domino[1]

    for i in "HBN":
        if test_limits(i,current_row,current_col,table_map):
            table_map[current_row+"-"+current_col][2] = i
        else:
            continue

        temp_row = table_map[current_row+"-"+current_col][1].split("-")[0]
        temp_col = table_map[current_row+"-"+current_col][1].split("-")[1]
        
        # Test conditions 
        if table_map[current_row+"-"+current_col][2]== "H":
            if test_limits("B",temp_row,temp_col,table_map):
                table_map[table_map[current_row+"-"+current_col][1]][2] = "B"
            else:
                table_map[current_row+"-"+current_col][2] = "i"
                continue
        elif table_map[current_row+"-"+current_col][2] == "B":
            if test_limits("H",temp_row,temp_col,table_map):
                table_map[table_map[current_row+"-"+current_col][1]][2] = "H"
            else:
                table_map[current_row+"-"+current_col][2] = "i"
                continue
        elif table_map[current_row+"-"+current_col][2] == "N":
            table_map[table_map[current_row+"-"+current_col][1]][2] = "N"

        if backtracking_solver(row_high_limits,row_base_limits,col_high_limits,col_base_limits,table_map):
            return True
        
        # Delete if domino is not right
        table_map[current_row+"-"+current_col][2] = "i"
        table_map[table_map[current_row+"-"+current_col][1]][2] = "i" 

    return False # End of backtracking

def write_output_file(table_map:dict,col_base_limits:list):
    """
    Args:
        table_map (dict): Dictionary created by concat_domino_pieces() function
        col_base_limits (list): List showing how many base values ​​should be in the columns (used to find the number of items in a row)
    """
    with open (sys.argv[2],"a"): # Create output file if it is not exist
        pass
    with open(sys.argv[2],"r+") as f:
        item_counter_for_row = 0
        for item in table_map:
            if item_counter_for_row != len(col_base_limits)-1: 
                f.write(table_map[item][2]+" ")
                item_counter_for_row += 1
            else: # If we are on the end of row
                f.write(table_map[item][2])
                f.write("\n")
                item_counter_for_row = 0
        f.seek(0)
        data = f.read().rstrip('\n') # Delete last empty line

    with open(sys.argv[2],'w') as f:    
        f.write(data)

def main():
    data = fix_game_table(read_input_file())
    row_high_limits = data[0]
    row_base_limits = data[1]
    col_high_limits = data[2]
    col_base_limits = data[3]
    table = data[4:]
    table_map = concat_domino_pieces(table)

    if backtracking_solver(row_high_limits,row_base_limits,col_high_limits,col_base_limits,table_map):
        write_output_file(table_map,col_base_limits)
    else:
        with open(sys.argv[2],"w") as f:
            f.write("No solution!")  

if __name__ == "__main__":
    main()