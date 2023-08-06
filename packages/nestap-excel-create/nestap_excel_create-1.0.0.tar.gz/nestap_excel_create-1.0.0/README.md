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

     columns = [
                  ('eno', 'Employee Number'),
                  ('ename', 'Employee Name'),
                  ('esal', 'Employee Salary'),
                  ('eaddr', 'Employee Address')

              ],
              
     create_excel([
        {
            'sheet_name': Your sheet name,
            'columns_keys': columns 
            'data_list': list(data)
        }
    ]) # Provide the list of the dictionary while Initializing
    
```

### This Nestap Excel Package create excel more quickly and efficiently.