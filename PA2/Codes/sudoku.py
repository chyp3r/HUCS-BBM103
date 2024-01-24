import sys

def read_input_file():
    """
    Returns:
        sudoku_table (str): A sudoku table reading from input file
    """
    with open(sys.argv[1],"r", encoding="utf-8") as f:
        sudoku_table = f.read()
        return(sudoku_table)

def fix_data(sudoku_table:str):
    """
    Adapts the given sudoku table to the problem  

    Args:
        sudoku_table (str): A sudoku table given from user 

    Returns:
        fixed_sudoku_table (list): The data in the sudoku table arranged for the given problem
    """
    row_list = list(sudoku_table.split("\n"))
    fixed_sudoku_table = []
    for row in row_list:
        fixed_sudoku_table.append(row.split(" "))
    return fixed_sudoku_table

def find_step_count(sudoku_table:str):
    """
    Calculates how many steps it takes to solve the given sudoku table.

    Args:
        sudoku_table (str): A sudoku table given from user
        
    Returns:
        max_step (int): Number of squares to be solved in the sudoku table
    """
    max_step = 0
    for item in sudoku_table:
        if item == "0" or item == "0\n":
            max_step+=1
    return max_step

def row_items(sudoku_table:list,row_number:int):
    """
    Args:
        sudoku_table (list): A sudoku table which fixed by fix_data function
        row_number (int): The row number to be selected

    Returns:
        row_list (list) = A list of elements in row
    """
    row_list = [item for item in sudoku_table[row_number]]
    return row_list

def col_items(sudoku_table:list,col_number:int):
    """    
    Args:
        sudoku_table (list): A sudoku table which fixed by fix_data function
        col_number (int): The column number to be selected

    Returns:
        col_list (list) = A list of elements in column
    """
    col_list = []
    for i in range(0,9):
        col_list.append(sudoku_table[i][col_number])
    return col_list

def box_items(sudoku_table:list,row_number:int,col_number:int):
    """
    Args:
        sudoku_table (list): A sudoku table which fixed by fix_data function
        row_number (int): The row number to be selected
        col_number (int): The column number to be selected

    Returns:
        box_list (list): The list of elements of the box containing the point at the intersection of the entered row and column 
    """
    box_list =[]
    start_row_index = (row_number // 3) * 3 # Row index of the first element of the box trying to be found
    start_col_index = (col_number // 3) * 3 # Column index of the first element of the box trying to be found
    for row in range(start_row_index,start_row_index+3):
        for col in range(start_col_index,start_col_index+3):
            box_list.append(sudoku_table[row][col])
    return box_list

def sudoku_bruteforcer(sudoku_table:list):
    """
    Each time the function is called, it uses the brute force method to solve the square that is closest to the square 0x0 and can take a single value.

    Args:
        sudoku_table (list): A sudoku table which fixed by fix_data function 

    Returns:
        sudoku_table (list): One more step solved version of the sudoku table 
        answer (int): Answer written to the solved square 
        row_counter (int): Row number of the solved square 
        col_counter (int): Column number of the solved square 
    """
    row_counter = 0
    for row in sudoku_table:
        col_counter = 0
        for item in row:
            if(item == "0"):
                item_list = []
                item_list.extend(row_items(sudoku_table,row_number=row_counter))
                item_list.extend(col_items(sudoku_table,col_number=col_counter))
                item_list.extend(box_items(sudoku_table,row_number=row_counter,col_number=col_counter))
                unique_item_list = list(set(item_list)) # Removing repetitive elements
                if(len(unique_item_list) == 9): # If there are 9 numbers in a list, we can find the 10th number that is not given.
                    for answer in range(0,10):
                        if not(str(answer) in unique_item_list):
                            sudoku_table[row_counter][col_counter] = str(answer)
                            return sudoku_table,answer,row_counter+1,col_counter+1
            col_counter +=1
        row_counter +=1

def create_output_data(sudoku_table:list,step:int,answer:int,row:int,col:int,out:list):
    """
    Adds the data of the last solution in the appropriate format to the table to be written to output

    Args:
        sudoku_table (list): Sudoku table which comes from sudoku_bruteforcer()
        step (int): The number of steps taken so far in the solution process
        answer (int): Last found answer
        row (int): Row number of the solved square
        col (int): Column number of the solved square
        out (list): Results to be written to output.txt

    Returns:
        out (list): Updated version of the results to be written to output.txt with the last step sudoku_table
    """
    out.append("-"*18+"\n")
    out.append(f"Step {step} - {answer} @ R{row}C{col}\n")
    out.append("-"*18+"\n")
    for row in sudoku_table:
        index_counter = 0
        for item in row:
            if(index_counter != 8):
                out.append(item+" ")
                index_counter +=1
            else:
                out.append(item) # We don't need space for last element of row
                index_counter = 0
        out.append("\n")
    return out

def create_output_file(out:list):
    """
    Args:
        out (list): Results to be written to output.txt
    """
    with open(sys.argv[2],"w", encoding="utf-8") as f:
        f.writelines(out)
        f.write("-"*18)
        f.flush()

def main():
    fixed_sudoku_table = fix_data(read_input_file())
    max_step = find_step_count(read_input_file())
    output_data = []
    for step in range(max_step):
        solving_steps = sudoku_bruteforcer(fixed_sudoku_table)
        fixed_sudoku_table = solving_steps[0]
        output_data = create_output_data(fixed_sudoku_table,step+1,solving_steps[1],
                                         solving_steps[2],solving_steps[3],output_data)
    create_output_file(output_data)

if __name__ == "__main__":
    main()