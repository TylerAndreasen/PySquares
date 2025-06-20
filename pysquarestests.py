from pysquares import *
import numpy as np
from numpy import testing as npt
import unittest

class Test_PySquares(unittest.TestCase):
    
    def test_custom_pad(self):
        print("\n\nTEST: padding shapes\n")
        #print("full")
        full_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=int)
        padded_full_arr = custom_pad(full_arr)
        intended = np.array([[0, 0, 0, 0, 0,],
                             [0, 1, 2, 3, 0,],
                             [0, 4, 5, 6, 0,],
                             [0, 0, 0, 0, 0,],], dtype=int)
        npt.assert_array_equal(padded_full_arr, intended)

        #print("pad again")
        double_padded_full_arr = custom_pad(padded_full_arr)
        npt.assert_array_equal(double_padded_full_arr, intended)

        #print("\nempty")
        empty_arr = np.array([[0, 0, 0], [0, 0, 0]], dtype=int)
        padded_empty_arr = custom_pad(empty_arr)
        self.assertIsNone(padded_empty_arr)

        #print("\nsingle empty cell")
        a = np.array([[0]], dtype=int)
        b = custom_pad(a)
        self.assertIsNone(b)

        #print("\nsingle full cell")
        a = np.array([[1]], dtype=int)
        b = custom_pad(a)
        intended = np.array([[0,0,0],
                             [0,1,0],
                             [0,0,0],], dtype=int)
        npt.assert_array_equal(b, intended)
    
    def test_validate_shape(self):
        print("\n\nTEST: Validating shapes\n")
        #print("single cell")
        a = np.array([[1]], dtype=int)
        self.assertTrue(validate_shape(a))

        #print("\nkitty corner")
        a = np.array([[0,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,0],], dtype=int)
        self.assertFalse(validate_shape(a))

        #print("\nlarger shape")
        a = np.array([[0,0,0,0,0],
                    [0,1,1,1,0],
                    [0,0,1,0,0],
                    [0,0,0,0,0]], dtype=int)
        self.assertTrue(validate_shape(a))

        #print("\nisolated shape")
        a = np.array([[0,0,0,0,0],
                    [0,1,1,1,0],
                    [0,0,0,0,0],
                    [0,0,1,0,0],
                    [0,0,0,0,0]], dtype=int)
        self.assertFalse(validate_shape(a))
    
    def test_encode_shape(self):
        print("\n\nTEST: Encode shapes")
        #print("\n small square")
        a = np.array([[0,0,0,0],
                      [0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],], dtype=int)
        self.assertEqual(encode_shape(a), "4,4,4,-5,2,-2,2,-5")

        #print("\n hollow square")
        a = np.array([[0,0,0,0,0,0],
                      [0,1,1,1,1,0],
                      [0,1,0,0,1,0],
                      [0,1,0,0,1,0],
                      [0,1,1,1,1,0],
                      [0,0,0,0,0,0],], dtype=int)
        self.assertEqual(encode_shape(a), "12,6,6,-7,4,-2,1,-2,1,-2,1,-2,1,-2,4,-7")
    
    def test_create_shape(self):
        print("\n\nTEST: Create shapes from encodings")

        a = "4,4,4,-5,2,-2,2,-5"
        b = np.array([[0,0,0,0],
                      [0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],], dtype=int)
        npt.assert_array_equal(create_shape(a), b)
    
    def test_involved_encoding(self):
        print("\n\nTEST: Decode then re-encode shapes")

        #print("\nSimple encoding, to shape, back to encoding")
        a = "4,4,4,-5,2,-2,2,-5"
        b = encode_shape(create_shape(a))
        self.assertEqual(b,a)

        #print("\nLarge encoding, to shape, back to encoding")
        a = "10,5,5,-5,7,-5,3,-5"
        b = encode_shape(create_shape(a))
        self.assertEqual(b,a)

        #print("\nLarge shape, to encoding, back to shape")
        a = np.array([[0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [1,1,0,0,0,1,0,0],
                    [0,1,0,1,1,1,0,0],
                    [0,1,1,1,0,0,0,0],
                    [0,1,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0],], dtype=int)
        b = create_shape(encode_shape(a))
        npt.assert_array_equal(b,a)
    
    def test_cull(self):
        print("\n\nTEST: Cull 0-only edges from shapes")
        
        #print("\n single cell")
        a = np.array([[1]], dtype=int)
        b = cull(a)
        npt.assert_array_equal(b,a)

        #print("\n tiny shape")
        a = np.array([[1,1,0,0]], dtype=int)
        b = cull(a)
        npt.assert_array_equal(b,np.array([[1,1]], dtype=int))

        #print("\n small square")
        a = np.array([[0,0,0,0],
                    [0,1,1,0],
                    [0,1,1,0],
                    [0,0,0,0],], dtype=int)
        b = cull(a)
        npt.assert_array_equal(b, np.array([[1,1], [1,1]], dtype=int))

        #print("\n hollow square")
        a = np.array([[0,0,0,0,0,0],
                    [0,1,1,1,1,0],
                    [0,1,0,0,1,0],
                    [0,1,0,0,1,0],
                    [0,1,1,1,1,0],
                    [0,0,0,0,0,0],], dtype=int)
        b = cull(a)
        npt.assert_array_equal(b, np.array([[1,1,1,1], [1,0,0,1], [1,0,0,1], [1,1,1,1]], dtype=int))
        

        #print("\nLarge shape")
        a = np.array([[0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [1,1,0,0,0,1,0,0],
                    [0,1,0,1,1,1,0,0],
                    [0,1,1,1,0,0,0,0],
                    [0,1,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0],], dtype=int)
        b = cull(a)
        npt.assert_array_equal(b, np.array([[1,1,0,0,0,1],
                                            [0,1,0,1,1,1],
                                            [0,1,1,1,0,0],
                                            [0,1,0,1,0,0]], dtype=int))
    
    def test_generate_shell(self):
        print("\n\nTEST: Shell Construction around shapes.")

        #print("\nSingle Cell shape")
        a = np.array([[1]], dtype=int)
        b = generate_shell(a)
        npt.assert_array_equal(b, np.array([[0,1,0],
                                           [1,0,1],
                                           [0,1,0],], dtype=int))
        
        #print("\nSmall shape")
        a = np.array([[1,1],
                      [1,1],], dtype=int)
        b = generate_shell(a)
        npt.assert_array_equal(b, np.array([[0,1,1,0],
                                            [1,0,0,1],
                                            [1,0,0,1],
                                            [0,1,1,0],], dtype=int))

        #print("\nLarge Shape")
        a = np.array([[1,0,1,0],
                      [1,1,1,1],
                      [1,0,1,1],
                      [0,1,0,0],])
        b = generate_shell(a)
        npt.assert_array_equal(b, np.array([[0,1,0,1,0,0],
                                              [1,0,1,0,1,0],
                                              [1,0,0,0,0,1],
                                              [1,0,1,0,0,1],
                                              [0,1,0,1,1,0],
                                              [0,0,1,0,0,0],], dtype=int))
    
    def test_get_n_from_encoding(self):
        print("\n\nTEST: Get value of n from encoded shape")

        #print("\nSimple encoding")
        a = "4,4,4,-5,2,-2,2,-5"
        b = get_n_from_encoding(a)
        self.assertEqual(b, 4)

        #print("\nLarge encoding")
        a = "10,5,5,-5,7,-5,3,-5"
        b = get_n_from_encoding(a)
        self.assertEqual(b, 10)

    def test_get_n_from_shape(self):
        print("\n\nTEST: Get value of `n` from enoding")
        
        #print("\nsmall square")
        a = np.array([[0,0,0,0],
                      [0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],], dtype=int)
        b = get_n_from_shape(a)
        self.assertEqual(b, 4)

        #print("\nhollow square")
        a = np.array([[0,0,0,0,0,0],
                      [0,1,1,1,1,0],
                      [0,1,0,0,1,0],
                      [0,1,0,0,1,0],
                      [0,1,1,1,1,0],
                      [0,0,0,0,0,0],], dtype=int)
        b = get_n_from_shape(a)
        self.assertEqual(b, 12)
        

        #print("\nLarge shape")
        a = np.array([[0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [1,1,0,0,0,1,0,0],
                      [0,1,0,1,1,1,0,0],
                      [0,1,1,1,0,0,0,0],
                      [0,1,0,1,0,0,0,0],
                      [0,0,0,0,0,0,0,0],], dtype=int)
        b = get_n_from_shape(a)
        self.assertEqual(b, 12)
    """
    def test_generate_first_novel_encoding(self): #############
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

    def test_generate_all_encodings_after_first(self): ##################
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
    """

if __name__ == '__main__':
    unittest.main()


#TPS = Test_PySquares()

#TPS.test_custom_pad()
#TPS.test_validate_shape()
#TPS.test_encode_shape()
#TPS.test_create_shape()
#TPS.test_involved_encoding()
#TPS.test_cull()
#TPS.test_generate_shell()
#TPS.test_get_n_from_encoding()
#TPS.test_get_n_from_shape()