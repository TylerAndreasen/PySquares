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
    for i in range(dims[1]):
        for j in range(dims[0]):
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
    if (is_empty_shape(cur_shape)):
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
    out = {}
    to_make_count = shell.sum()
    first_found = False
    cur_shape = custom_pad(cur_shape)
    dims = cur_shape.shape
    if (dims != shell.shape):
        print("Area reserved for shape and shell are different, implementation logic is broken")
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
    return set.issubset({elem})





                    
#print(current_shape[0])





























