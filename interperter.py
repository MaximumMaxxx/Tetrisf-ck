import json

# Function that takes in an array of single characters and uses them to run brainfuck code
# "r" = <
# "o" = >
# "g" = +
# "b" = -
# "p" = .
# "P" = ,
# "y" = [
# "c" = ]


def interpreter(code: "list[str]"):
    """
    Takes in an array of single characters and uses them to run brainfuck code
    """
    # Initialize variables
    output = ""
    pointer = 0
    memory = [0] * 30000
    memory_pointer = 0
    while pointer < len(code):
        # Check if the current character is a valid brainfuck command
        if code[pointer] == "r":
            # Move the pointer left
            memory_pointer -= 1
        elif code[pointer] == "o":
            # Move the pointer right
            memory_pointer += 1
        elif code[pointer] == "g":
            # Increment the memory
            memory[memory_pointer] += 1
        elif code[pointer] == "b":
            # Decrement the memory
            memory[memory_pointer] -= 1
        elif code[pointer] == "p":
            # Output the memory
            output += chr(memory[memory_pointer])
        elif code[pointer] == "P":
            # Input the memory
            ok = False
            while not ok:
                inp = input()
                try:
                    memory[memory_pointer] = ord(input())
                except:
                    if inp == "exit":
                        return output
                    print("Invalid input")
                else:
                    ok = True
                    
        elif code[pointer] == "y":
            # Check if the memory is 0
            if memory[memory_pointer] == 0:
                # Move the pointer to the matching ]
                while code[pointer] != "c":
                    pointer += 1
        elif code[pointer] == "c":
            # Check if the memory is not 0
            if memory[memory_pointer] != 0:
                # Move the pointer to the matching [
                while code[pointer] != "y":
                    pointer -= 1
        # Move the pointer forward
        pointer += 1

        if pointer >= len(code):
            break
    return output


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


if __name__ == "__main__":
    # Load the board from json
    with open("board.json", "r") as file:
        board = json.load(file)
    # Convert the board to a single array
    single_array = boardToSingleArray(board)
    # Run the interpreter on the single array
    interpreter(single_array)
