# Create Excel

This Package will help you to create Excel file more quickly and efficiently.

## How to Install it?

On Windows:
```
pip install nestap_excel_create
```

On Linux:
```
sudo pip3 install nestap_excel_create
```

## How to Use it?

### Initializing The Package

```
from nestap_excel_create.create_excel_helper import create_excel
     
     data1 = Employee.objects.values('eno', 'ename', 'esal', 'eaddr').all()
     
     data2 = Student.objects.values('roll_no', 'name', 'school', 'addr').all()
     
     columns1 = [
                  ('eno', 'Employee Number'),
                  ('ename', 'Employee Name'),
                  ('esal', 'Employee Salary'),
                  ('eaddr', 'Employee Address')

              ]
              
     columns2 = [
                  ('roll_no', 'Roll Number'),
                  ('name', 'Student Name'),
                  ('school', 'School'),
                  ('addr', 'Address')

              ]         
        
     create_excel([
        {
            'sheet_name': Your sheet name 1,
            'columns_keys': columns1 
            'data_list': list(data1)
        },
        {
            'sheet_name': Your sheet name 2,
            'columns_keys': columns2 
            'data_list': list(data2)
        }
    ]) # Provide the list of the dictionary while Initializing
    
```

### This Nestap Excel package create 1 and more than 1 excel sheet in same excel file

### This Nestap Excel Package create excel file more quickly and efficiently.