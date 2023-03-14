'''
This program can hack messages encrypted 
with the Caesar cipher from the previous project, even 
if you don’t know the key. There are only 26 
possible keys for the Caesar cipher, so a computer can easily try all possible decryptions and display the results to the user. In cryptography, we call 
this technique a brute-force attack.
'''

def decrypt_caesar_cipher(encrypted_line, key):
    clear_text = ""
    for char in encrypted_line:
        # Decrypt the alpha letters a-z A-Z. 
        if char.isalpha():
            # lambda function to return the start index ('a' for lowercase characters or 'A' for upper uppercase characters)
            start_index = lambda c: ord('A') if c.isupper() else ord('a')
            # Lambda function to add 26 if the result is less than the start index. So we can have (a <= result <= z) or (A <= result <= Z)
            step_back = lambda x: x + 26 if x < start_index(char) else x          
            # Shift back by the key
            new_char = chr(step_back(ord(char) - key))
            clear_text+= new_char

        else:
            # Keep the none-alpha character
            clear_text += char

    return clear_text

try:
    # Open the file containing the caesar cipher content
    with open('enc.txt') as encrypted_file:
        encrypted_lines = encrypted_file.readlines()

    # Lambda function to return the line with the most characters so we can have enough cipher to brute-force
    return_max_length_line = lambda lines: max(lines, key=lambda line: len(line))
    encrypted_line = return_max_length_line(encrypted_lines)

    # If the max-char-line is small and less than the size of a word, then join all lines 
    if len(encrypted_line) < 2:
        encrypted_line = ' '.join(encrypted_lines)

        # If the result is still small, then exit the program
        if len(encrypted_line) < 4:
            print("The file has no sufficient content to brute-force") 
            exit(1)

    # Brute-force attack from 1 to 25
    for key in range(1,26):
        # To make the printed text easier to compare, I set the maximum length to 50 
        clear_text = decrypt_caesar_cipher(encrypted_line[:100], key)
        # Print the result so the user can choose which one is the correct key
        print(f"Key: {key}  result: {clear_text}\n")

    # Prompt the user for the key or exit 
    key = input("Enter the key value or enter (D)one to exit: ")
    if not key.isnumeric():
        # Exit if the input is not numeric
        exit(0)

    print("Decrypting the whole file..\n")
    for line in encrypted_lines:
        clear_text = decrypt_caesar_cipher(line, int(key))
        print(clear_text)

except FileNotFoundError as e:
    print("Error: enc.txt file is not found in the current directory")
except Exception as e:
    print("Error: " + str(e))
