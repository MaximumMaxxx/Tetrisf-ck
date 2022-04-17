# Function that takes in an array of single characters and uses them to run brainfuck code
# "r" = <
# "o" = >
# "g" = +
# "b" = -
# "p" = .
# "y" = [
# "c" = ]

def interpreter(code: list[str]):
    """
    Takes in an array of single characters and uses them to run brainfuck code
    """
    # Initialize variables
    pointer = 0
    memory = [0] * 30000
    memory_pointer = 0
    while pointer < len(code):
        # Check if the current character is a valid brainfuck command
        if code[pointer] == "r":
            # If it is, move the memory pointer to the left
            memory_pointer -= 1
        elif code[pointer] == "o":
            # If it is, move the memory pointer to the right
            memory_pointer += 1
        elif code[pointer] == "g":
            # If it is, increment the value at the memory pointer
            memory[memory_pointer] += 1
        elif code[pointer] == "b":
            # If it is, decrement the value at the memory pointer
            memory[memory_pointer] -= 1
        elif code[pointer] == "p":
            # If it is, print the value at the memory pointer
            print(chr(memory[memory_pointer]), end="")
        elif code[pointer] == "y":
            # If it is, loop until the next matching ] is found
            loop_count = 1
            while loop_count > 0:
                pointer += 1
                if code[pointer] == "y":
                    loop_count += 1
                elif code[pointer] == "c":
                    loop_count -= 1
        elif code[pointer] == "c":
            # If it is, loop until the next matching [ is found
            loop_count = 1
            while loop_count > 0:
                pointer -= 1
                if code[pointer] == "y":
                    loop_count -= 1
                elif code[pointer] == "c":
                    loop_count += 1
        # Move to the next character
        pointer += 1
    # Print a newline
    print()
    

def boardToSingleArray(board):
    """
    Takes in a board and returns a single array of characters
    """
    # Initialize variables
    single_array = []
    # Loop through the board
    for i in range(20):
        for j in range(10):
            # Add the current character to the single array
            single_array.append(board[i][j])
    # Return the single array
    return single_array
    