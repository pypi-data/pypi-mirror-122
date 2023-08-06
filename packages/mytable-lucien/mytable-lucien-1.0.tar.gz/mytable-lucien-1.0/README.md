# MYTABLE
A simple package for processing data in the form of a table.
To install:
```shell
pip install mytable-lucien
```
To import:
```python
import mytable
```
## MYCSV
This is a simple reader and writer for CSV files by Lucien Shaw.
It consumes less resource and processes more quickly than the current csv module, though a lot less functional.

It reads CSV files as plain texts and stores the table in a list, whose elements are lists of cells of the current row. The list is the value to the key 'full' of a dict, which is the returned value of the function.

Here is the guidance.
### To import
```python
from mytable import mycsv
```
### Function: read()
- usage
```python
from mytable import mycsv
mycsv.read(filname, has_header, delimiter=',')
```
- arguments
  - filename
  
    A string value. The filename of the CSV file.
  - has_header
  
    A bool value. Whether the table has a header.
  - delimiter
  
    A char value. Comma by default. The character which is used to delimit the columns.
- returned value
  - dict
    - 'full'
    
        List of rows. Each row is a list of columns, aka. cells, which contains strings. 
    - 'data'
    
        Full table without header. Same with 'full' if there is no header.
    - 'has_header'
    
        A bool value. Whether the table has a header. Copied from the same argument.
    - 'columns'
    
        Total columns of the table.
    - 'rows'
    
        Total rows of the full table.
    - 'rows_data'
    
        Total rows of the table (without header row). Same with 'rows' if there is no header.
### Function: write()
- usage
```python
from mytable import mycsv
mycsv.write(filename, table, delimiter=',')
```
- arguments
  - filename
    
    A string value. The filename of the CSV file be written.
  - table
  
    A list, the structure of which is the same with the value wo the key 'full' of the returned dict of function read().
    
    All values shall be **strings**.
  - delimiter
  
    A char value. Comma by default. The character which is used to delimit the columns.
- returned value

    There is no returned value.