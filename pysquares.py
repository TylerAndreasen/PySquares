'''

This program is an attempt to create a polyonimo generator in Python.
The goal is to allow the program to output the number of unique polyominos that can be made with n squares when given n.
When available, the program will bootstrap itself from files on disc that store encodings of shapes.

Things I will need to learn to do in Python for this project:
    File Manipulation
        https://numpy.org/doc/stable/user/absolute_beginners.html#how-to-save-and-load-numpy-objects
    NumPy interfacing
        a.shape() returns a list of the size of an ndarray in a list
    String Manipulation

Rules:
    Shapes will be numpy arrays in which 1_s denote squares being in a shape, where 0_s denote empty cells.
    Negative values or values greater than 1 will break the program.
    Shapes must have all included cells be contiguous.
    The 'shell' of a shape is shape that contains all cells which are adjscent to, but not included in, the provided shape.

'''

import numpy as np
#print(np.__version__)

def custom_pad(cur_shape):
    dims = cur_shape.shape
    if (len(dims) != 2):
        print("Attempted to pad a shape of size {}".format(dims))
        return object()
    else:
        vert = 0
        horiz = 0
        zer = np.zeros(dims[1], dtype=int)
        if (not np.array_equal(cur_shape[0], zer) or not np.array_equal(cur_shape[-1], zer)):
            vert = 1
        t_cur_shape = np.transpose(cur_shape)
        zer = np.zeros(dims[0], dtype=int)
        if (not np.array_equal(t_cur_shape[0], zer) or not np.array_equal(t_cur_shape[-1], zer)):
            horiz = 1
        if (horiz + vert > 0):
            cur_shape = np.pad(cur_shape, (horiz, vert), 'constant', constant_values=(0))
        return cur_shape

# Will depreciate
def is_empty_shape(cur_shape):
    if (cur_shape.sum() > 0):
        return False
    dims = cur_shape.shape
    for i in range(dims[1]):
        for j in range(dims[0]):
            if (cur_shape[i][j] > 0):
                return False
    return True

def validate_shape(cur_shape):
    count = cur_shape.sum()
    if (count < 0):
        return False
    if (count < 2):
        return True
    dims = cur_shape.shape
    found = 0
    for i in range(1, dims[1]-1):
        if (found == count):
            break
        for j in range(1, dims[0]-1):
            if (found == count):
                break
            if (cur_shape[i][j] == 1): # Found active cell
                # Look at neighbors
                found += 1
                if (not (cur_shape[i-1][j] == 1 or cur_shape[i+1][j] == 1 or cur_shape[i][j-1] == 1 or cur_shape[i][j+1] == 1)):
                    return False
                
            
    return True      

def encode_shape(cur_shape):
    out = "" + str(cur_shape.sum()) + ","
    dims = cur_shape.shape
    out += str(dims[0]) + "," + str(dims[1])+","
    counter = 0
    for i in range(dims[0]):
        for j in range(dims[1]):
            if (cur_shape[i][j] == 0):
                if (counter < 1):
                    counter -= 1
                else:
                    out += str(counter) + ","
                    counter = -1
            else: # cur_shape[i][j] == 1
                if (counter > -1):
                    counter += 1
                else:
                    out += str(counter) + ","
                    counter = 1
    out += str(counter)
    return out

def valid_encoding(encoded):
    if (len(encoded.split(",")) < 4):
        return False
    return True

def create_shape(encoded):
    numbers = encoded.split(",")
    count = int(numbers[0])
    dims = (int(numbers[1]),int(numbers[2]))
    new_shape = np.zeros((dims[0],dims[1]), dtype=int)
    index = 3
    current = int(numbers[index])
    for i in range(dims[1]):
        for j in range(dims[0]):
            if (current > 0):
                new_shape[i][j] = 1
                current -= 1
            elif (current < 0):
                current += 1
            if (current == 0 and not index + 1 == len(numbers)):
                index += 1
                current = int(numbers[index])
    return new_shape

def cull(cur_shape):
    if (np.all(cur_shape == 0)):
        return np.zeros((1,1))
    top = 0
    right = 0
    bottom = 0
    left = 0
    dims = cur_shape.shape
    for i in range(dims[1]):
        if (cur_shape[i].sum() == 0):
            top += 1
        else:
            break

    for i in range(dims[1]-1, 0, -1):
        if (cur_shape[i].sum() == 0):
            bottom += 1
        else:
            break

    for i in range(dims[0]-1, 0, -1):
        ls = np.sum(cur_shape, 0, dtype=int) 
        if (ls[i] == 0):
            right += 1
        else:
            break

    for i in range(dims[0]):
        if (np.sum(cur_shape, 0, dtype=int)[i] == 0):
            left += 1
        else:
            break

    if (top +  bottom + right + left > 0):
        new_shape = np.zeros(( dims[1]-top-bottom, dims[0]-left-right), dtype=int)
        ndims = new_shape.shape
        print(ndims)
        for i in range(ndims[0]):
            for j in range(ndims[1]):
                new_shape[i][j] = cur_shape[i+top][j+left]
        return new_shape
    else:
        return cur_shape
        
def generate_shell(cur_shape):
    cur_shape = custom_pad(cull(cur_shape))
    dims = cur_shape.shape
    shell = np.zeros((dims[0],dims[1]), dtype=int)

    for i in range(1,dims[0]-1):
        for j in range(1,dims[1]-1): # Loop through all non-padding cells
            if (cur_shape[i][j] == 0):
                continue
            else: # We care about this cell

                # UP
                if ( (cur_shape[i][j-1] == 1) or (shell[i][j-1] == 1) ):
                    pass
                else:
                    shell[i][j-1] = 1

                # DOWN
                if ( (cur_shape[i][j+1] == 1) or (shell[i][j+1] == 1) ):
                    pass
                else:
                    shell[i][j+1] = 1

                # LEFT
                if ( (cur_shape[i-1][j] == 1) or (shell[i-1][j] == 1) ):
                    pass
                else:
                    shell[i-1][j] = 1

                # RIGHT
                if ( (cur_shape[i+1][j] == 1) or (shell[i+1][j] == 1) ):
                    pass
                else:
                    shell[i+1][j] = 1
    return shell         

def get_n_from_shape(cur_shape):
    return cur_shape.sum()

def get_n_from_encoding(encoding):
    if len(encoding) < 1:
        return 0
    a = encoding.split(",")
    if (a[0].isdecimal()):
        return int(a[0])
    else:
        return 0

def generate_first_novel_encoding(cur_shape):
    dims = cur_shape.shape
    new_shape = custom_pad(np.copy((cur_shape)))
    flag = False
    for i in range(dims[0]):
        if flag:
            break
        for j in range(dims[1]):
            if cur_shape[i][j] == 1:
                flag = True
                new_shape[i][j+1] = 1
                break
    return encode_shape(cull(new_shape))

def generate_all_encodings_after_first(cur_shape, shell):
    out = set()
    to_make_count = shell.sum()
    first_found = False
    cur_shape = custom_pad(cur_shape)
    dims = cur_shape.shape
    if (dims != shell.shape):
        print("Area reserved for shape and shell are different, implementation logic is broken")

    # TODO The logic of the below is sound, but does not account for rotations and reflections.
    #       It will behoove me to take a step back, think through how to write a series of steps that will effeciently generate rotations and reflections
    #       Further, doing some research about where it is most effecient to try to test for repetition.

    for i in range(dims[0]):
        for j in range(dims[1]):
            if shell[i, j] == 1:
                if first_found == False:
                    first_found = True
                    continue
                else:
                    new_shape = np.copy(cur_shape)
                    new_shape[i, j] = 1
                    out.add(encode_shape(cull(new_shape)))
    return out

def set_contains(set, elem):
    return {elem}.issubset(set)


if __name__ == "__main__":
    
    n = 0
    # Ask for user input
    while True:
        print("How many squares to include in free polyomino generation, called `n`: ")
        temp = input().strip()
        if not temp.isdecimal():
            print("Please enter a number.\n\n")
            continue
        temp = int(temp)
        if temp < 1:
            print("Please enter a value of at least 1 square to generate into shapes.")
            continue
        n = temp
        if n > 64:
            print("If you wish to know the answer to the number of shapes made with n squares,")
            print("You should likely not be running Python that you found on the internet")
            print("As the code will not be nearly effecient enough to complete in anything short of geologic time scales")
            print("on the hardware available to the original developer.")
            print("The developer advises you to stop the program and find a more effecient means of calculating.")
            print("If you continue, you have been warned, don't expect to see the final answer in your lifetime.")
        elif n > 27:
            print("As of writing this program, humans have not calculated beyond 27 squares.")
            print("You are unlikely to reach the end of this program quickly.")
        break
    
    if n < 3:
        print("There exists only 1 polyonimo with {} square(s)".format(n))
    else:
        init = np.ones((2,1))

        small_shapes = [init]

        large_shape_encodings = set([])

        m = 2
        while m < n:
            print("Shapes of size {}".format(m) + "are counted to be {}.".format(len(small_shapes)))

            for shape in small_shapes:
                fne = generate_first_novel_encoding(shape)
                if (set_contains(large_shape_encodings, fne)):
                    continue # Don't bother generating anything else
                else: # We can legally add the fne to the set
                    shell = generate_shell(shape)

                    remaining_novel_shapes = generate_all_encodings_after_first(shape, shell)

                    add_flag = True
                    for novel_shape in remaining_novel_shapes:
                        if ({novel_shape}.issubset(large_shape_encodings)):
                            add_flag = False
                            break
                    if add_flag:
                        large_shape_encodings.add(fne)
            #END FOR
            if m == n:
                print("There are {} polyonimos of size {}".format(len(large_shape_encodings), n))
                break
            else:
                small_shapes = ()
                for encoding in large_shape_encodings:
                    small_shapes.add(create_shape(encoding))
                large_shape_encodings.empty()
                m += 1
        # END WHILE
    # END ELSE
    print("Thank you for your work in recreational mathematics")








