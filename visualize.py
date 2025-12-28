from pysquares import *
from pathlib import Path

n = 0

while True:
        print("Enter a number, and if that file is present, this will output the visuals of each shape of said size, take entering large numbers.")
        
        
        temp = input().strip()
        #temp = "5"

        
        if not temp.isdecimal():
            print("Please enter a number.\n\n")
            continue
        temp = int(temp)
        if temp < 3:
            print("Please enter a value of at least 3 square to show from files.")
            continue
        n = temp
        break

file_path = Path(generate_file_name_from_n(n))
if not file_path.exists():
    print("File containing shapes of requested size not found")
else:
    encodings = set_from_filename(file_path)
    for line in encodings:
        print(create_shape(line))
        print("\n")