import csv


def convert(file_name):
    try:

        with open(file_name) as f:
            reader = csv.DictReader(f)
        lst = list(reader)

    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        
        print(e)
    
    return lst


