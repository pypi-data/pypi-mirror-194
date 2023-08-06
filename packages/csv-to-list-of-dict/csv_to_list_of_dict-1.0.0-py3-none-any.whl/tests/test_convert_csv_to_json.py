import unittest
import csv

def convert(file_name):
    try:

        with open(file_name) as f:
            reader = csv.DictReader(f)
            lst = list(reader)
            print(lst)
            return lst

    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(e)
    
    

new_list = [['Paul','Jones'],['Steve','Hawkins']]
file_name = 'student.csv'

myFile = open(file_name, 'w')
writer = csv.writer(myFile)
writer.writerow(['first_name',"last_name"])
for data_list in new_list:
    writer.writerow(data_list)
myFile.close()

convert_file = convert(file_name)



class TestConvertCsvToJson(unittest.TestCase):

    def test_convert(self):
        self.assertEqual(convert_file[0]["first_name"],"Paul")
        self.assertEqual(convert_file[0]["last_name"],"Jones")
        self.assertEqual(convert_file[1]["first_name"],"Steve")
        self.assertEqual(convert_file[1]["last_name"],"Hawkins")
        
    

unittest.main()