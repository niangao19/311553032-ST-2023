import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        #TODO
        print('Start set_name test\n')
        for i in range( len( self.user_name ) ) :
            k = self.students.set_name( self.user_name[i] )
            self.assertEqual(i, k)
            self.user_id.append(i)
            print(f'{i}  {self.user_name[i]}')
        print('\nFinish set_name test\n\n')    
        pass

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        #TODO
        print('Start get_name test\n')
        k = len( self.user_id)
        print(f'user_id length =  {k}')
        print(f'user_name length =  {len( self.user_name )}\n')
        men = 0
        for i in range( k  ) :
            id = self.user_id[i]
            name = self.students.get_name(id)
            self.assertEqual( name, self.user_name[i] )
            if men == i :
                men = men + 1
            print( f'id {id} : {name}' )  
        name = self.students.get_name(men)
        self.assertEqual( 'There is no such user', name )
        print( f'id {men} : {name}' ) 
        print('\nFinish get_name test')       
        pass
