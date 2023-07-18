import csv

# Written by Michel Thomasius - Copyright (C) 2023.
# Parses a simple text file with a repeating pattern of lines, inserts the text lines into variables, 
# strips any leading and trailing white spaces and then inserts the data into columns in a CSV file
# Example source txt file:
# 18/07/2023
#
#
# Company 1
#
#
#  16.32
#
#
#  1234.00
#
# 17/07/2023
#
#
# company 2
#
#
#  221.74
#
#
#  2345.00
#
# 17/07/2023
#
#
# company 3
#
#
#  14.04
#
#
#  3456.00

def transform_text_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    i = 0
    # iterate through the lines in the text file:
    while i < len(lines):
        if lines[i].strip() != '': # find the first line of text with data
            date = lines[i].strip()  # find the date and strip leading and trailing white spaces
            location = lines[i+3].strip() # Skip forward 3x lines, then find the company info and strip leading and trailing white spaces
            value1 = lines[i+6].strip() # Skip forward 3x more lines, then find value1 and strip leading and trailing white spaces
            value2 = lines[i+9].strip() # Skip forward a further 3x lines, then find value2 and strip leading and trailing white spaces

            data.append([date, location, value1, value2]) # insert all values into a list

        i += 11 # skip forward to line 11 before start the above iteration again

    with open(output_file, 'w', newline='') as file: # write the CSV output file and create one new row for each iteration captured above from the text file
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file '{output_file}' has been created.")

# Usage example
input_file = 'input.txt'  # Replace with the path to your input text file
output_file = 'output.csv'  # Replace with the desired path and name for the output CSV file
transform_text_to_csv(input_file, output_file)

