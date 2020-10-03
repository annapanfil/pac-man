import unittest
from .classes import Character

class TestCharacter(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.pattern1 = [[1, 1 , 1],
                    [1, 0 , 0],
                    [1, 0 , 1]]
        self.pattern2 = [[0, 0],
                    [0, 0]]
        print("setup")

    def test_valid_move(self):
        # hit the wall
        self.assertEqual(Character((1,1)).valid_move([-1,0], self.pattern1), False)
        self.assertEqual(Character((1,1)).valid_move([0,1], self.pattern1), (1,2))
        # hit the border
        self.assertEqual(Character((0,0)).valid_move([-1,0], self.pattern2), (1,0))
        self.assertEqual(Character((1,0)).valid_move([-1,0], self.pattern2), (0,0))
        self.assertEqual(Character((0,0)).valid_move([0,-1], self.pattern2), (0,1))
        self.assertEqual(Character((0,1)).valid_move([0,1], self.pattern2), (0,0))

if __name__ == '__main__': # w razie gdyby ktoś nie uruchomił jako moduł
    unittest.main()
