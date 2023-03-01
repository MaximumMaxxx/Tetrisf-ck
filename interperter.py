import json
import logging


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
    # Check if the code is empty
    if [" "] * 200 == code:
        # Return an empty string
        print("Empty code")
        return ""

    # Check if the brainfuck code is valid
    stack = []
    for i in range(len(code)):
        # Check if the current character is a valid brainfuck command
        if code[i] == "y":
            stack.append("[")
        elif code[i] == "c":
            if len(stack) != 0 and stack[len(stack) - 1] == "[":
                stack.pop()
            else:
                print("Invalid code")
                return "Invalid code"

    if len(stack) != 0:
        print("Invalid code")
        return "Invalid code"

    # Initialize variables
    output = ""
    code_pointer = 0
    memory = [0] * 30000
    memory_pointer = 0
    while code_pointer < len(code):
        try:
            # Check if the current character is a valid brainfuck command
            if code[code_pointer] == "r":
                # Move the pointer left
                memory_pointer -= 1
            elif code[code_pointer] == "o":
                # Move the pointer right
                memory_pointer += 1
            elif code[code_pointer] == "g":
                # Increment the memory
                memory[memory_pointer] += 1
            elif code[code_pointer] == "b":
                # Decrement the memory
                memory[memory_pointer] -= 1
            elif code[code_pointer] == "p":
                # Output the memory
                output += chr(memory[memory_pointer])
                print(chr(memory[memory_pointer]))
            elif code[code_pointer] == "P":
                # Input the memory
                ok = False
                while not ok:
                    inp = input()
                    try:
                        memory[memory_pointer] = ord(input())
                    except:
                        if inp == "exit":
                            break
                        print("Invalid input")
                    else:
                        ok = True

            elif code[code_pointer] == "y":
                # Check if the memory is 0
                if memory[memory_pointer] == 0:
                    # Move the pointer to the matching ]
                    while code[code_pointer] != "c":
                        code_pointer += 1
            elif code[code_pointer] == "c":
                # Check if the memory is not 0
                if memory[memory_pointer] != 0:
                    # Move the pointer to the matching [
                    while code[code_pointer] != "y":
                        code_pointer -= 1
        except:  # If something goes wrong get some logs
            logging.exception(f"Error at pointer: {code_pointer}")
            logging.exception(f"Memory pointer: {memory_pointer}")
            logging.exception(f"Memory: {memory}")
            logging.exception(f"Code: {code}")

        # Move the pointer forward
        code_pointer += 1

        if code_pointer >= len(code):
            break

    # Return the output
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


# Run this stuff when the file is run by game.py
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Load the board from json
    with open("board.json", "r") as file:
        board = json.load(file)
    # Convert the board to a single array
    single_array = boardToSingleArray(board)
    # Run the interpreter on the single array
    interpreter(single_array)
