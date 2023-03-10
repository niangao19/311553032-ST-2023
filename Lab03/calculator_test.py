import unittest
from calculator import Calculator
import math

class ApplicationTest(unittest.TestCase):
    cal = Calculator
    def test_add(self):
        test_ans = [ ( 1 , 2 , 3 ) , ( 2 , 3 , 5  ) , (1 ,1 , 2), ( 2 ,2 ,4) , ( 3 , 100 , 103 ) ]
        for x, y, ans in test_ans:
            self.assertEqual( self.cal.add(x,y) , ans )
        with self.assertRaises(TypeError) as ctx:
            self.cal.add( 'error', 1 )

        self.assertEqual( 'can only concatenate str (not "int") to str', str(ctx.exception ))     
        pass

    def test_divide(self):
        test_ans = [ ( 2, 2 , 1 ) , ( 6, 3 , 2) , (4 ,2 , 2), ( 2 ,2 ,1) , ( 99, 3, 33 ) ]
        for x, y, ans in test_ans:
            self.assertEqual( self.cal.divide(x,y) , ans )

        with self.assertRaises(ZeroDivisionError) as ctx:        
            self.cal.divide( 30, 0 )
        
        self.assertEqual( 'division by zero', str(ctx.exception )) 
        pass

    def test_sqrt(self):
        test_ans = [ ( 2, math.sqrt(2) ) , ( 6, math.sqrt(6)) , (4 , math.sqrt(4)), ( 2 ,math.sqrt(2)) , ( 99, math.sqrt(99) ) ]
        for x, ans in test_ans:
            self.assertEqual( self.cal.sqrt(x) , ans )
        with self.assertRaises(TypeError) as ctx:
            self.cal.sqrt( 'error')

        self.assertEqual( 'must be real number, not str', str(ctx.exception )) 
        
        pass

    def test_exp(self):
        test_ans = [ ( 2, math.exp(2) ) , ( 6, math.exp(6)) , (4 , math.exp(4)), ( 2 ,math.exp(2)) , ( 99, math.exp(99) ) ]
        for x, ans in test_ans:
            self.assertEqual( self.cal.exp(x) , ans )    

        with self.assertRaises(TypeError) as ctx:
            self.cal.exp( 'error')

        self.assertEqual( 'must be real number, not str', str(ctx.exception ))      
        pass

if __name__ == '__main__':
    unittest.main()