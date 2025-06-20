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
    """A method to pad a Numpy 2 dimensional array with zeros, if any of the
    outer edges are zeros. 
    On looking back at this method, I realize that I should really just use
    the Numpy pad method after culling the shape, which would guarentee the
    built-in returns the expected values (ie, not having multiple lines of
    zeros).
    """
    dims = cur_shape.shape
    if (len(dims) != 2):
        #print("Attempted to pad a shape of size {}".format(dims))
        return None
    elif (cur_shape.sum() == 0):
        #print("Attempted to pad an empty shape")
        return None
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

def validate_shape(cur_shape):
    """
    
    IMPORTANT: This method is not complete, there is no checking for a shape that exists as two or more sections what happen to have multiple cells in contact.
    This will be non-trivial to implement, as I basically need to check if the graph implied by the shape is connected (using the graph theory definition).
    My initial though was that I needed to check a shape to determine if it had rows/columns that were full separated by rows/columns that are empty,
    meaning there are disconnected subgraphs. Honestly, this makes me question how important the shape and encoding validations are, as the only situation
    (after developing the logic ends) that questionable shapes are entering the system is if the user inputs  
    
    Accepts a Numpy ndarray for validation according to the rules
    necessary for polyomino creation.

    Shapes indicate that a cell is included by setting the element of the
    nested array to 1, leaving empty cells as 0s.
    Shapes must have at least one cell filled.
    All cells must be adjacent to at least one other cell.
    """
    count = cur_shape.sum()
    if (count < 1):
        return False
    dims = cur_shape.shape
    found = 0
    for i in range(1, dims[1]-1):
        if (found == count):
            break
        for j in range(1, dims[0]-1):
            if (cur_shape[i][j] < 0 or cur_shape[i][j] > 1):
                return False
            if (found == count):
                break
            if (cur_shape[i][j] == 1): # Found active cell
                # Look at neighbors
                found += 1
                if (not (cur_shape[i-1][j] == 1 or cur_shape[i+1][j] == 1 or cur_shape[i][j-1] == 1 or cur_shape[i][j+1] == 1)):
                    return False
    return True      

def encode_shape(cur_shape):
    """Accepts Accepts a Numpy ndarray for encoding into the following
    pattern.

    An encoding of a shape will be a String containing at least four comma
    separated integers represented in decimal.
    The first value will be the total number of cells present in the shape.
    The second and third values will be the number of rows and columns present
    in the shape.
    All following values will adhere to a rasterized reading of the shape
    being encoded. Reading from [0][0] (which I conceptualize as the top 
    right), count the number of fill/unfilled cells, counting up or down
    respectively. When the fill/unfilled status changes, write the current
    count to the encoding, followed by a comma, then reset the count to
    positive or negative 1 based on which cell was just found.

    These rules mean that after the first three values, values should
    alternate their signs.
    Further, the sum of all positive values from the raster should equal the
    first value, and the sum of the absolute value of all raster values should
    equal the product of the second and third values.
    In theory, a short-cut could be taken by not including a final negative
    element, as decoding a shape assigns 0 to all cells before reading the
    raster values.
    As a logical consequence, no values in a valid shape should be 0
    """
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
    """Validates a String encoding of a polyomino is correct.
    
    For a description of the rules that create encodings, see docs for
    def encode_shape(cur_shape):
    
    Encodings must have at least 4 values.
    The sum of positive raster values must be equal to the first value.
    The absolute sum of all raster values must be equal to the product of the
    second and third values.
    Logically, the first value cannot be greater than the product of the
    second and third values.


    """
    numbers = encoded.split(",")
    if (len(numbers) < 4):
        return False
    if (numbers[0] > numbers[1]*numbers[2]):
        return False
    cell_count = 0
    area = 0
    for num in numbers:
        check = int(num)
        if check == 0:
            return False
        if check > 0:
            cell_count += check
            area += check
        else:
            area += abs(check)
    
    if (cell_count != numbers[0]):
        return False
    
    if (area != numbers[1]*numbers[2]):
        return False
    #TODO Implement commandline param that control if all used/generated encodings are validated before being used
    return True

def create_shape(encoded):
    """Accepts an encoded shape and generates the implied shape.
    
    For a description of the rules that create encodings, see docs for
    def encode_shape(cur_shape):
    
    Encoding an existing shape, and then decoding the resultant String should
    result in an equivalent shape being created by this method.

    This method creates a Numpy 2 dimensional array based on the size
    specified in the encoding, then fills cells with one_s as the raster
    pattern specifies.
    """
    numbers = encoded.split(",")
    count = int(numbers[0])
    check = 0
    dims = (int(numbers[1]),int(numbers[2]))
    new_shape = np.zeros((dims[0],dims[1]), dtype=int)
    index = 3
    current = int(numbers[index])
    for i in range(dims[0]):
        for j in range(dims[1]):
            if (current > 0):
                new_shape[i][j] = 1
                check += 1
                current -= 1
            elif (current < 0):
                current += 1
            if (current == 0 and index < len(numbers)-1):
                index += 1
                current = int(numbers[index])

    if (check != count):
        print("Logic Error: Shape of size {},{} with {} cells was assigned {} cells.".format(dims[0], dims[1], count, check))
    return new_shape

def cull(cur_shape):
    """Accepts a Numpy 2 dimensional array to remove excess space from the 
    shape.
    
    In the case that entire rows or columns along the outside are filled
    entirely with zeros, they do not encode meaningful information and can be
    culled from the output shape before encoding.
    This method counts the number of rows and columns that can be ignored,
    and if any are present, creates a new Numpy array to store the smaller
    shape within.
    """
    if (np.all(cur_shape == 0)):
        return np.zeros((1,1))
    top = 0
    right = 0
    bottom = 0
    left = 0
    dims = cur_shape.shape
    #("{}".format(cur_shape))
    for i in range(dims[0]):
        if (cur_shape[i].sum() == 0):
            top += 1
        else:
            break

    for i in range(dims[0]-1,-1,-1):
        if (cur_shape[i].sum() == 0):
            bottom += 1
        else:
            break

    for i in range(dims[1]-1,-1,-1):
        ls = np.sum(cur_shape, 0, dtype=int) 
        if (ls[i] == 0):
            right += 1
        else:
            break

    for i in range(dims[1]):
        if (np.sum(cur_shape, 0, dtype=int)[i] == 0):
            left += 1
        else:
            break

    if (top +  bottom + right + left > 0):
        new_shape = np.zeros(( dims[0]-top-bottom, dims[1]-left-right), dtype=int)
        ndims = new_shape.shape
        #print(ndims)
        for i in range(ndims[0]):
            for j in range(ndims[1]):
                new_shape[i][j] = cur_shape[i+top][j+left]
        return new_shape
    else:
        return cur_shape
        
def generate_shell(cur_shape):
    """Accepts a Numpy 2 dimensional array, from which it creates a shell.
    
    The logic of the program requires that a 'shell' of a given shape is 
    created. This shell specifies all spaces that a given shape could have a
    cell added and become a valid shape of the next largest size.
    Cells included in the shell are those that don't exist in the supplied
    shape, but are adjascent to at least one cell in that shape.
    Because cells within this process can be added to beyond all four edges of
    a given shape, the shape must be culled down to the actual size of the 
    shape (as to not grow the bounding box of the shape overtime), and then
    padded to ensure that there is room around the shape in the shell to insert
    cells beyond the extreme most cells
    
    """
    trimmed = cull(cur_shape)
    cur_shape = custom_pad(trimmed)
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
    """Returns the number of active cells in the shape."""
    return cur_shape.sum()

def get_n_from_encoding(encoding):
    """Returns the size of the shape implied by the encoding."""
    if len(encoding) < 1:
        return 0
    a = encoding.split(",")
    if (a[0].isdecimal()):
        return int(a[0])
    else:
        return 0

def generate_reflected_encodings(cur_shape):
    """Accepts a shape to generate encodings of.
    
    Function generates encodings for the four reflections of a given shape,
    it does not rotate said shape. This could be done using the rotate method
    supplied by Numpy, but it seems cleaner not to do so in an already
    non-trivial function such as this.
    """
    cur_shape = cull(cur_shape)
    out = set()
    dims = cur_shape.shape
    encoding = ""
    init_axis = str(cur_shape.sum()) + "," + str(dims[0]) +  "," + str(dims[1]) + ","
    
    # Canonical View
    encoding = init_axis
    counter = 0
    for i in range(dims[0]):
        for j in range(dims[1]):
            if (cur_shape[i][j] == 0):
                if (counter < 1):
                    counter -= 1
                else:
                    encoding += str(counter) + ","
                    counter = -1
            else: # cur_shape[i][j] == 1
                if (counter > -1):
                    counter += 1
                else:
                    encoding += str(counter) + ","
                    counter = 1
    encoding += str(counter)
    out.add(encoding)

    # Reflect Vertical
    encoding = init_axis
    counter = 0
    for i in range(dims[0]):
        for j in range(dims[1]-1,-1,-1):
            if (cur_shape[i][j] == 0):
                if (counter < 1):
                    counter -= 1
                else:
                    encoding += str(counter) + ","
                    counter = -1
            else: # cur_shape[i][j] == 1
                if (counter > -1):
                    counter += 1
                else:
                    encoding += str(counter) + ","
                    counter = 1
    encoding += str(counter)
    out.add(encoding)

    # Reflect Horizontal
    encoding = init_axis
    counter = 0
    for i in range(dims[0]-1,-1,-1):
        for j in range(dims[1]):
            if (cur_shape[i][j] == 0):
                if (counter < 1):
                    counter -= 1
                else:
                    encoding += str(counter) + ","
                    counter = -1
            else: # cur_shape[i][j] == 1
                if (counter > -1):
                    counter += 1
                else:
                    encoding += str(counter) + ","
                    counter = 1
    encoding += str(counter)
    out.add(encoding)

    # Reflect Vertical and Horizontal
    encoding = init_axis
    counter = 0
    for i in range(dims[0]-1,-1,-1):
        for j in range(dims[1]-1,-1,-1):
            if (cur_shape[i][j] == 0):
                if (counter < 1):
                    counter -= 1
                else:
                    encoding += str(counter) + ","
                    counter = -1
            else: # cur_shape[i][j] == 1
                if (counter > -1):
                    counter += 1
                else:
                    encoding += str(counter) + ","
                    counter = 1
    encoding += str(counter)
    out.add(encoding)
    return out

def set_contains(set, elem):
    """Determines if a single element is a subset of a set."""
    return {elem}.issubset(set)

if __name__ == "__main__":
    
    n = 0
    # Ask for user input
    while True:
        print("How many squares to include in free polyomino generation, called `n`: ")
        
        
        temp = input().strip()
        #temp = "5"

        
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
        init = np.ones((2,1), dtype=int) # dtype=int ??
        small_shape_encodings = ([encode_shape(init)])

        large_shape_encodings = set([])

        m = 2
        while m <= n:
            #print("Shapes of size {}".format(m) + " are counted to be {}.".format(len(small_shape_encodings))) # of size len(small_shapes)

            for shape_encoding in small_shape_encodings:
                shape = create_shape(shape_encoding)
                shell = generate_shell(shape)
                shape = custom_pad(shape)
                sdims = shell.shape
                for i in range(sdims[0]): # rows
                    for j in range(sdims[1]): #columns
                        if shell[i][j] == 1:
                            new_shape = np.copy(shape)
                            new_shape[i][j] = 1
                            reflected = generate_reflected_encodings(new_shape)
                            rotated_and_reflected = generate_reflected_encodings(np.rot90(new_shape))
                            rnr = reflected.union(rotated_and_reflected)
                            if len(rnr & large_shape_encodings) > 0:
                                # Overlap with this place in the shell
                                continue
                            else:
                                large_shape_encodings.add(rnr.pop())
            #END FOR
            if m == n-1:
                print("There are {} polyonimos of size {}".format(len(large_shape_encodings), n))

                #for encoding in large_shape_encodings:
                #    print(create_shape(encoding))
                #    print()
                break
            else:
                small_shape_encodings = large_shape_encodings
                large_shape_encodings = set()
                m += 1
        # END WHILE
    # END ELSE

    print("Thank you for your work in recreational mathematics")








