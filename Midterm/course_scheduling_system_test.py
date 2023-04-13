import unittest
from unittest.mock import Mock
import course_scheduling_system as css

class CssTest(unittest.TestCase):
    css = css.CSS()

    def test_q1_1(self) :
        self.css.check_course_exist = Mock( return_value= True)
        course = ('Algorithms', 'Monday', 3, 4)
        ans = self.css.add_course(course)
        self.assertEqual(ans,True)


    def test_q1_2(self):
        self.css.check_course_exist = Mock( return_value= True)
        course = ('Algorithms', 'Monday', 3, 4)
        ans = self.css.add_course(course)
        self.assertEqual(ans,False)


    def test_q1_3(self):
        self.css.check_course_exist = Mock( return_value= False)
        course = ('DS', 'Tuesday', 3, 4)
        ans = self.css.add_course(course)
        self.assertEqual(ans,False)

    def test_q1_4(self):
        self.css.check_course_exist = Mock( return_value= True)
        course = (3, 'Tuesday', 3, 4)
        with self.assertRaises(TypeError) as ctx:
            self.css.add_course(course)

    # def print_list( self,course_list ):
    #     workdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #     sch= '\nMonday\tTuesday\tWednesday\tThursday\tFriday\n'
    #     for i in range(1,7) :
    #         have = False
    #         line = ''
    #         for j in range(len(workdays)) :
    #             for cus in course_list :
    #                 if ( cus[1] == workdays[j]  and (cus[3] == i or cus[2] == i) ) :
    #                     line += cus[0] + '|\t'
    #                     have = True
    #             if not have :
    #                 line += '|\t'
    #         sch += line +'\n'
    #     print(sch)        


    def test_q1_5(self):
        self.css.check_course_exist = Mock( return_value= True)
        course1 = ('DS', 'Tuesday', 3, 4)
        self.css.add_course(course1)
        course2 = ('UNIX', 'Thursday', 3, 4)
        self.css.add_course(course2)
        self.css.remove_course(course1)
        course_list = self.css.get_course_list()
        print(self.css)
        self.assertEqual( [('Algorithms', 'Monday', 3, 4),('UNIX', 'Thursday', 3, 4)], course_list)
        self.assertEqual( 3,  self.css.check_course_exist.call_count)


 




if __name__ == "__main__":
    unittest.main()    
