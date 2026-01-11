from typing import TypedDict

class Person(TypedDict):
    name : str
    age : int
    
new_p : Person= {'name':'shuvo', 'age':25}

print(new_p)