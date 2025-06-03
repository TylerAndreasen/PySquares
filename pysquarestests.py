from pysquares import *
import numpy as np
def custom_pad_test():
    print("\n\nTEST: padding shapes\n")
    print("full")
    full_arr = np.array([[1, 2, 3], [4, 5, 6]])
    padded_full_arr = custom_pad(full_arr)
    print(full_arr)
    print(padded_full_arr)
    print("pad again")
    double_padded_full_arr = custom_pad(padded_full_arr)
    print(double_padded_full_arr)

    print("\nempty")
    empty_arr = np.array([[0, 0, 0], [0, 0, 0]])
    padded_empty_arr = custom_pad(empty_arr)
    print(empty_arr)
    print(padded_empty_arr)

    print("\nsingle empty cell")
    a = np.array([[0]])
    b = custom_pad(a)
    print(a)
    print(b)

    print("\nsingle full cell")
    a = np.array([[1]])
    b = custom_pad(a)
    print(a)
    print(b)

def validate_shape_test():
    print("\n\nTEST: Validating shapes\n")
    print("single cell")
    a = np.array([[1]])
    print(a)
    print(validate_shape(a))

    print("\nkitty corner")
    a = np.array([[0,0,0,0],
                  [0,1,0,0],
                  [0,0,1,0],
                  [0,0,0,0],])
    print(a)
    print(validate_shape(a))

    print("\nlarger shape")
    a = np.array([[0,0,0,0,0],
                  [0,1,1,1,0],
                  [0,0,1,0,0],
                  [0,0,0,0,0]])
    print(a)
    print(validate_shape(a))

    print("\nisolated shape")
    a = np.array([[0,0,0,0,0],
                  [0,1,1,1,0],
                  [0,0,0,0,0],
                  [0,0,1,0,0],
                  [0,0,0,0,0]])
    print(a)
    print(validate_shape(a))

def encode_shape_test():
    print("\n\nTEST: Encode shapes")
    print("\n small square")
    a = np.array([[0,0,0,0],
                  [0,1,1,0],
                  [0,1,1,0],
                  [0,0,0,0],])
    print(a)
    print(encode_shape(a))

    print("\n hollow square")
    a = np.array([[0,0,0,0,0,0],
                  [0,1,1,1,1,0],
                  [0,1,0,0,1,0],
                  [0,1,0,0,1,0],
                  [0,1,1,1,1,0],
                  [0,0,0,0,0,0],])
    print(a)
    print(encode_shape(a))

def create_shape_test():
    print("\n\nTEST: Create shapes from encodings")

    a = "4,4,4,-5,2,-2,2,-5"
    print(a)
    print(create_shape(a))

def involved_encoding_test():
    print("\n\nTEST: Decode then re-encode shapes")

    print("\nSimple encoding, to shape, back to encoding")
    a = "4,4,4,-5,2,-2,2,-5"
    print(a)
    print(create_shape(a))
    b = encode_shape(create_shape(a))
    print(b)
    print(b == a)

    print("\nLarge encoding, to shape, back to encoding")
    a = "10,5,5,-5,7,-5,3,-5"
    print(a)
    print(create_shape(a))
    b = encode_shape(create_shape(a))
    print(b)
    print(b == a)

    print("\nLarge shape, to encoding, back to shape")
    a = np.array([[0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [1,1,0,0,0,1,0,0],
                  [0,1,0,1,1,1,0,0],
                  [0,1,1,1,0,0,0,0],
                  [0,1,0,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0],])
    print(a)
    print(encode_shape(a))
    b = create_shape(encode_shape(a))
    print(b)
    print(b == a)


def cull_test():
    print("\n\nTEST: Cull 0-only edges from shapes")
    
    print("\n small square")
    a = np.array([[0,0,0,0],
                  [0,1,1,0],
                  [0,1,1,0],
                  [0,0,0,0],])
    print(a)
    b = cull(a)
    print(b)
    print(b.shape == (2,2))

    print("\n hollow square")
    a = np.array([[0,0,0,0,0,0],
                  [0,1,1,1,1,0],
                  [0,1,0,0,1,0],
                  [0,1,0,0,1,0],
                  [0,1,1,1,1,0],
                  [0,0,0,0,0,0],])
    print(a)
    b = cull(a)
    print(b)
    print(b.shape == (4,4))
    

    print("\nLarge shape")
    a = np.array([[0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [1,1,0,0,0,1,0,0],
                  [0,1,0,1,1,1,0,0],
                  [0,1,1,1,0,0,0,0],
                  [0,1,0,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0],])
    print(a)
    b = cull(a)
    print(b)
    print(b.shape == (4,6))

def generate_shell_test():
    print("\n\nTEST: Shell Construction around shapes.")

    print("\nSingle Cell shape")
    a = np.array([[1]])
    print(a)
    b = generate_shell(a)
    print(b)
    print(b == np.array([[0,1,0],
                         [1,0,1],
                         [0,1,0],]))
    
    print("\nSmall shape")
    a = np.array([[1,1],
                  [1,1],])
    print(a)
    b = generate_shell(a)
    print(b)
    print(b == np.array([[0,1,1,0],
                         [1,0,0,1],
                         [1,0,0,1],
                         [0,1,1,0],]))

    print("\nLarge Shape")
    a = np.array([[1,0,1,0],
                  [1,1,1,1],
                  [1,0,1,1],
                  [0,1,0,0],])
    print(a)
    b = generate_shell(a)
    print(b)
    print(b == np.array([[0,1,0,1,0,0],
                         [1,0,1,0,1,0],
                         [1,0,0,0,0,1],
                         [1,0,1,0,0,1],
                         [0,1,0,1,1,0],
                         [0,0,1,0,0,0],]))

def get_n_from_encoding_test():
    print("\n\nTEST: Get value of n from encoded shape")

    print("\nSimple encoding")
    a = "4,4,4,-5,2,-2,2,-5"
    print(a)
    b = get_n_from_encoding(a)
    print(b)
    print(b == 4)

    print("\nLarge encoding, to shape, back to encoding")
    a = "10,5,5,-5,7,-5,3,-5"
    print(a)
    b = get_n_from_encoding(a)
    print(b)
    print(b == 10)

def get_n_from_shape_test():
    print("\n\nTEST: Get value of `n` from enoding")
    
    print("\n small square")
    a = np.array([[0,0,0,0],
                  [0,1,1,0],
                  [0,1,1,0],
                  [0,0,0,0],])
    print(a)
    b = get_n_from_shape(a)
    print(b)
    print(b == 4)

    print("\n hollow square")
    a = np.array([[0,0,0,0,0,0],
                  [0,1,1,1,1,0],
                  [0,1,0,0,1,0],
                  [0,1,0,0,1,0],
                  [0,1,1,1,1,0],
                  [0,0,0,0,0,0],])
    print("a is {}".format(a))
    b = get_n_from_shape(a)
    print("b is {}".format(b))
    print(b == 12)
    

    print("\nLarge shape")
    a = np.array([[0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [1,1,0,0,0,1,0,0],
                  [0,1,0,1,1,1,0,0],
                  [0,1,1,1,0,0,0,0],
                  [0,1,0,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0],])
    print("a is {}".format(a))
    b = get_n_from_shape(a)
    print("b is {}".format(b))
    print(b == 12)

def generate_first_novel_encoding_test():
    print("\n\nTEST: Generate 'first' shape from an existing shape.")

    print("\nSmall shape")
    a = np.array([[1,1],
                  [1,1],])
    print("a is {}".format(a))
    b = generate_first_novel_encoding(a)
    print("b is {}".format(b))
    print(b == "5,3,2,1,-1,4")

    print("\nLarge Shape")
    a = np.array([[1,0,1,0],
                  [1,1,1,1],
                  [1,0,1,1],
                  [0,1,0,0],])
    print("a is {}".format(a))
    b = generate_first_novel_encoding(a)
    print("b is {}".format(b))
    print(b == "11,5,4,1,-3,1,-1,1,-1,5,-1,2,-1,1,-2")

def generate_all_encodings_after_first_test():
    print("\n\nTEST: Generates encodings of shapes from shell, excludes first shape.")
    print("\nSingle Cell shape")
    a = np.array([[1]])
    print(a)
    c = generate_all_encodings_after_first(a, generate_shell(a))
    for b in c:
        print(b)
    d = set(["2,1,2,2", "2,2,1,2"])
        # Note, this should still find a vertical pair, but the original shape should be the top cell, not that we can easily know that.
    for e in d:
        if (not e in c):
            print("\n Below shape NOT found in output")
            print(e)  
    
    print("\nSmall shape")
    a = np.array([[1,1],
                  [1,1],])
    print(a)
    c = generate_all_encodings_after_first(a, generate_shell(a))
    for b in c:
        print(b)
    d = set(["5,2,3,3,-1,2","5,2,3,-1,5","5,2,3,5,-1","5,2,3,2,-1,3","5,3,2,-1,5","5,3,2,5,-1","5,3,2,4,-1,1"])

    for e in d:
        if not e in c:
            print("\n Below shape NOT found in output")
            print(e)

    f = "5,3,2,1,-1,4"
    if f in c:
        print("\nError: Located first shape in list when it should not have been present")

#custom_pad_test()
#validate_shape_test()
#encode_shape_test()
#create_shape_test()
#involved_encoding_test()
#cull_test()
#generate_shell_test()
#get_n_from_encoding_test()
#get_n_from_shape_test()
#generate_first_novel_encoding_test()
#generate_all_encodings_after_first_test()