import sys

def read_input_file():
    """
    Returns:
        game_table (str): A game table reading from input file
    """
    with open(sys.argv[1],"r", encoding="utf-8") as f:
        game_table = f.read()
        return game_table

def fix_data(game_table:str):
    """
    Adapts the given game table to the problem  

    Args:
        game_table (str): A game table given from user 

    Returns:
        fixed_sgame_table (list): The data in the game table arranged for the given problem
    """
    row_list = list(game_table.split("\n"))
    fixed_game_table = []
    for row in row_list:
        fixed_game_table.append(row.split(" "))
    return fixed_game_table

def create_table_map(data:list):
    """
    Create a location dictionary for given data

    Args:
        data (list): A fixed game table 
    
    Returns:
        my_map (dict): A dictionary that holds row and column information (row-column) as key,the value in the cell (i: empty cell) as value, 
    and whether the value in the cell has been checked before (0: not checked, 1: checked). -> {"<row>-<col>":["<value_of_cell>","<0 or 1>"]}
    """
    my_map = {}
    row_number = 0
    for row in data:
        col_number = 0
        for _ in row:
            my_map[str(row_number)+"-"+str(col_number)] = [data[row_number][col_number],"0"]
            col_number +=1
        row_number +=1
    return my_map

def neighbour_collector(row:int,col:int,table_map:dict):
    """
    Compares the value in the given cell with the values ​​in the neighboring cell

    Args:
        row (int): Row number of cell
        col (int): Col number of cell
        table_map: Table created by create_table_map()
    Returns:
        neighbours (list): Cells with the same value as in the given cell
        table_map: Changed version of table_map (If a cell is looked at, it sets the control value to 1) 
    """ 
    row = int(row)
    col = int(col)
    selected = table_map[str(row)+"-"+str(col)][0]
    neighbours = []
    try:
        if row-1 >= 0:
            if selected == table_map[str(row-1)+"-"+str(col)][0] and table_map[str(row-1)+"-"+str(col)][1] == "0": # Check previous row neighbour
                neighbours.append(str(row-1)+"-"+str(col))
                table_map[str(row-1)+"-"+str(col)][1] = "1"
    except Exception as _:
        pass
    try:
        if selected == table_map[str(row+1)+"-"+str(col)][0] and table_map[str(row+1)+"-"+str(col)][1] == "0": # Check next row neighbour
            neighbours.append(str(row+1)+"-"+str(col))
            table_map[str(row+1)+"-"+str(col)][1] = "1"
    except Exception as _:
        pass
    try:
        if col-1 >= 0:
            if selected == table_map[str(row)+"-"+str(col-1)][0] and table_map[str(row)+"-"+str(col-1)][1] == "0": # Check previous column neighbour
                neighbours.append(str(row)+"-"+str(col-1))
                table_map[str(row)+"-"+str(col-1)][1] = "1"
    except Exception as _:
        pass    
    try:
        if selected == table_map[str(row)+"-"+str(col+1)][0] and table_map[str(row)+"-"+str(col+1)][1] == "0": # Check next column neighbour
            neighbours.append(str(row)+"-"+str(col+1))
            table_map[str(row)+"-"+str(col+1)][1] = "1"
    except Exception as _:
        pass
    return neighbours,table_map

def path_finder(table_map:dict,row:int,col:int):
    """
    Find all neighbours of cell which has same value

    Args:
        table_map: Table created by create_table_map()
        row (int): Row number of cell
        col (int): Col number of cell
    
    Returns:
        table_map (dict): Changed version of table_map (If a cell is looked at, it sets the control value to 1) 
    """
    neighbours = []
    neighbours.append(str(row)+"-"+str(col))
    new_neighbours = []
    single_counter = 0 # A counter for no movement statu
    for _ in range(len(table_map)):
        index = 0
        for _ in neighbours:
            temp = neighbour_collector(neighbours[index].split("-")[0],neighbours[index].split("-")[1],table_map) # Find neighbours with same value
            table_map = temp[1]
            for a in temp[0]:
                new_neighbours.append(a)
            index +=1
            single_counter += 1
        neighbours = new_neighbours
    if single_counter == 1:
        print("No movement happened try again")
        print("")
    return table_map
    
def map_updater(table_map:dict,score:int):
    """
    Updates the game table and calculates score

    Args:
        table_map (dict): Table created by create_table_map() 
        score (int): Last score of player before play move
    Returns:
        table_map (dict): Version of exploding cells with values ​​replaced by i(empty)
        score (int): New score of player after play move
    """
    katsayi = 0
    for keys in table_map:
        if table_map[keys][1] == "1" and table_map[keys][0] != "i" :
            n = table_map[keys][0]
            table_map[keys][0] = "i" # Change cells with "i" i-> This cell is empty 
            katsayi +=1
    try:
        score += int(n)*katsayi
    except Exception as _:
        pass
    return table_map,score

def col_check(table_map:dict,max_row:int,max_col:int):
    """
    Control the empty columns and delete them

    Args:
        table_map (dict): Table created by create_table_map()
        max_row (int): Number of rows in the table
        max_col (int): Number of columns in the table
    
    Returns:
        table_map (dict): New version of table_map (empty columns deleted)
        max_col: Number of columns in the table (if some column deleted first version will change)
    """
    while True and len(table_map.keys()):
        for col in range(max_col):
            delete = True # Are we have empty column
            for row in range(max_row):
                if table_map[str(row)+"-"+str(col)][0] != "i":
                    delete = False
                    break

            if delete:
                for row_inner in range(max_row):
                    del table_map[str(row_inner)+"-"+str(col)] # Delete empty cell
                max_col -=1
                for i in range(col,max_col):
                    for r in range(max_row):
                        table_map[str(r)+"-"+str(i)] = table_map[str(r)+"-"+str(i+1)] # Shift to left
                for row1 in range(max_row):
                    try:
                        del table_map[str(row1)+"-"+str(max_col)] # Delete last cells (Because of left shifting last cells are empty)
                    except Exception as _:
                        pass
                break
        if not delete:
            break

    def key_for_short(item):
        row_col_list = item.split("-")
        return int(row_col_list[0])*max_col+int(row_col_list[1])
    
    # Short dict 
    key_of_table = list(table_map.keys())
    key_of_table.sort(key=key_for_short)
    sorted_dict = {item: table_map[item] for item in key_of_table}
    table_map = sorted_dict 
    
    return table_map,max_col

def is_first_empty(table_map:dict):
    """
    Control the is first row empty or not

    Args:
        table_map (dict): Table created by create_table_map() 
    
    Returns:
        is_empty (bool): If first row, empty return true otherwise return false 
    """
    is_empty = True
    for keys in table_map:
        if keys.split("-")[0] != "0":
            break
        elif table_map[keys][0] != "i":
            is_empty = False
            break
    return is_empty

def row_check(table_map:dict,max_row:int,max_col:int):
    """
    Control the empty rows and delete them

    Args:
        table_map (dict): Table created by create_table_map()
        max_row (int): Number of rows in the table
        max_col (int): Number of columns in the table 
    
    Returns:
        new_dic (dict): New version of table_map (empty rows deleted)
        max_row: Number of rows in the table (if a row deleted, first version of row count will change)
    """
    table_map_copy = table_map.copy()
    new_dic = {}
    for row in range(max_row):
        for col in range(max_col):
            try:
                new_dic[str(row)+"-"+str(col)] = table_map_copy[str(row+1)+"-"+str(col)]
            except Exception as err:
                pass
    max_row -=1
    return new_dic,max_row
        
def writer(table_map:dict,max_col:int):
    """
    Print the game table

    Args:
        table_map (dict): Table created by create_table_map()
        max_col (int): Number of columns in the table 
    """
    satir_sonu = 0
    if table_map == {}:
        print("")
    for keys in table_map:
        if table_map[keys][0] != "i":
            print(table_map[keys][0],end=" ")
        else:
            print(" ",end=" ")
        satir_sonu += 1
        if satir_sonu == max_col:
            print("")
            satir_sonu = 0

def table_map_fixer(table_map:dict):
    """
    Gravity for game

    Args:
        table_map (dict): A fixed game table 
    
    Returns:
        table_map (dict): Version where top cells are placed in spaces which down
    """
    while True:
        change = False
        for keys in table_map:
            row_number = keys.split("-")[0]
            col_number = keys.split("-")[1]
            if table_map[keys][0] == "i" and row_number != "0": 
                if table_map[str(int(row_number)-1)+"-"+str(col_number)][0] != "i": 
                    temp = table_map[str(int(row_number)-1)+"-"+str(col_number)]
                    table_map[str(int(row_number)-1)+"-"+str(col_number)] = table_map[keys]
                    table_map[keys] = temp
                    change = True
        if not change:
            break
    return table_map

def is_game_over(table_map:dict,max_row:int,max_col:int):
    """
    Check the is game over

    Args:
        table_map: Table created by create_table_map()
        max_row (int): Number of rows in the table
        max_col (int): Number of columns in the table
    
    Returns:
        game_over (bool): Returns false if there are no moves left to make, otherwise true 
    """
    game_over = False
    for keys in table_map:
        row_number = keys.split("-")[0]
        col_number = keys.split("-")[1]
        if table_map[keys][0] != "i":
            if int(row_number)+1 <max_row :
                if table_map[keys][0] == table_map[str(int(row_number)+1)+"-"+str(int(col_number))][0]:
                    game_over = True
            if int(row_number)-1 >= 0:
                if table_map[keys][0] == table_map[str(int(row_number)-1)+"-"+str(int(col_number))][0]:
                    game_over = True
            if int(col_number)+1 <max_col:  
                if table_map[keys][0] == table_map[str(int(row_number))+"-"+str(int(col_number)+1)][0]:
                    game_over = True
            if int(col_number)-1 >= 0:
                if table_map[keys][0] == table_map[str(int(row_number))+"-"+str(int(col_number)-1)][0]:
                    game_over = True  
    return game_over

def main():
    score = 0
    data = read_input_file()
    fixed_table = fix_data(data)
    table_map = create_table_map(fixed_table)

    max_row = len(fixed_table)
    max_col = len(fixed_table[0])

    writer(table_map,max_col)
    print("")
    print("Your score:",score)
    print("")

    while is_game_over(table_map,max_row,max_col):
        
        number = input("Please enter a row and a column: ")
        print("")

        row = int(number.split(" ")[0]) - 1
        col = int(number.split(" ")[1]) - 1 

        if row+1>max_row or col+1>max_col or row <0 or col<0:
            print("Please enter a correct size!")
            print("")
            continue

        table_map= path_finder(table_map,row,col)
        table_map,score = map_updater(table_map,score)
        table_map = table_map_fixer(table_map)
        table_map,max_col= col_check(table_map,max_row,max_col)

        if is_first_empty(table_map):
            table_map, max_row = row_check(table_map,max_row,max_col)

        writer(table_map,max_col)
        print("")
        print("Your score:",score)
        print("")

    print("Game over")
    
if __name__ == "__main__":
    main()