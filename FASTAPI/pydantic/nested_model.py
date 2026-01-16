from pydantic import BaseModel


class Address(BaseModel):
    city:str
    district:str
    division:str
    pin:int
    

class Patient(BaseModel):
    
    name: str
    gender:str
    age:int
    address: Address
    
address_dict = {'city':'dupchanchia', 'district':'bogura','division':'rajshahi', 'pin':5880}
address1 = Address(**address_dict)

patient_dict = {'name':'shuvo','gender':'male', 'age':25, 'address':address1}

patient1 =Patient(**patient_dict)

print(patient1)