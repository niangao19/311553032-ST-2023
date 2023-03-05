import unittest
from unittest.mock import Mock
from unittest.mock import patch
import app


class FakeMail:
    def write(name) :
        context = 'Congrats, ' + name + '!'
        return context
    
    def send( name, context): 
        print(f'{context}')

class ApplicationTest(unittest.TestCase):
    i = 0
    mock_file_content = "William\nOliver\nHenry\nLiam"
    people = ["William" ,"Oliver" ,"Henry","Liam"]
    selected = ["William" ,"Oliver" ,"Henry"]
    def setUp(self):
        # stub
        app.Application.get_names = Mock( return_value= (self.people,self.selected))
        self.app = app.Application()
        pass
#        with unittest.mock.patch(
#               'builtins.open',
#                new=unittest.mock.mock_open(read_data=self.mock_file_content),
#               create=True
#        ) as file_mock:
#           self.app = app.Application()

#        for i in range(3) :
#             self.app.selected.append(self.people[i])
    
    
 
    def test_app(self):
        # mock
        self.app.get_random_person = Mock(side_effect= ["William" ,"Oliver" ,"Henry","Liam"])
        name = self.app.select_next_person()
        print(f'{name} selected')
        self.assertEqual(name,'Liam')
        
        # spy
        app.MailSystem.write = Mock(side_effect=FakeMail.write)
        #self.app.mailSystem.write.return_value = 'Congrats, ' + name + '!'
        app.MailSystem.send = Mock(side_effect=FakeMail.send)
        self.app.notify_selected()
        self.assertEqual( len(self.people), self.app.mailSystem.write.call_count)
        
        print(self.app.mailSystem.write.call_args_list)
        self.assertEqual( len(self.people), self.app.mailSystem.send.call_count)
        print(self.app.mailSystem.send.call_args_list)
        pass


if __name__ == "__main__":
    unittest.main()
