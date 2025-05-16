import csv

class CsvFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data

    def write(self, data):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

if __name__=='__main__':
    csv_file = CsvFile('data.csv')
    
    new_data = [
        ['Name', 'Age', 'Gender'],
        ['Alice', '25', 'Female'],
        ['Bob', '30', 'Male'],
    ]
    csv_file.write(new_data)
    
    data = csv_file.read()
    print(data)

    