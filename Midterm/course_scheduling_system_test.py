import unittest
from unittest.mock import Mock
import course_scheduling_system as css

class CssTest(unittest.TestCase):
    css = css.CSS()

    def test_q1_1(self) :
        self.css.check_course_exist = Mock( return_value= True)
        course = ('Algorithms', 'Monday', 3, 4)
        ans = self.css.add_course(course)
        with self.subTest():
            self.assertEqual(ans,True)


    def test_q1_2(self):
        self.css.check_course_exist = Mock( return_value= True)
        course = ('Algorithms', 'Monday', 3, 4)
        ans = self.css.add_course(course)
        with self.subTest():
            self.assertEqual(ans,False)


    def test_q1_3(self):
        self.css.check_course_exist = Mock( return_value= False)
        course = ('DS', 'Tuesday', 3, 4)
        ans = self.css.add_course(course)
        with self.subTest():
            self.assertEqual(ans,False)

    def test_q1_4(self):
        self.css.check_course_exist = Mock( return_value= True)
        course = (3, 'Tuesday', 3, 4)
        course2 = ('DS', '3', 3, 4)   
        course3 = ('DS', 'Tuesday', '2', 4)
        course4 = ('DS', 'Tuesday', '2')   
        with self.subTest():                  
            with self.assertRaises(TypeError) as ctx:
                self.css.add_course(course)
            with self.assertRaises(TypeError) as ctx:            
                self.css.add_course(course2)
            with self.assertRaises(TypeError) as ctx:
                self.css.add_course(course3) 
            with self.assertRaises(TypeError) as ctx:           
                self.css.add_course(course4)            
     
    def test_q1_5(self):
        self.css.check_course_exist = Mock( return_value= True)
        course1 = ('DS', 'Tuesday', 3, 4)
        self.css.add_course(course1)
        course2 = ('UNIX', 'Thursday', 3, 4)
        self.css.add_course(course2)
        self.css.remove_course(course1)
        course_list = self.css.get_course_list()
        print(self.css)
        with self.subTest():
            self.assertEqual( [('Algorithms', 'Monday', 3, 4),('UNIX', 'Thursday', 3, 4)], course_list)
            self.assertEqual( 3,  self.css.check_course_exist.call_count)

    def test_q1_6(self):
        self.css.check_course_exist = Mock( return_value= True)
        course1 = ('DS', 'Tuesday', 3, 4)
        ans = self.css.remove_course(course1)
        with self.subTest():
            self.assertEqual(ans,False)
        self.css.check_course_exist = Mock( return_value= False) 
        ans = self.css.remove_course(course1)
        with self.subTest():        
            self.assertEqual(ans,False)

if __name__ == "__main__":# pragma: no cover
    unittest.main()    
