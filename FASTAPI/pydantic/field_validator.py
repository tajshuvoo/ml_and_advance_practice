from pydantic import BaseModel , EmailStr, AnyUrl, Field, field_validator
from typing import List,Dict, Optional, Annotated

class patient(BaseModel):
    
    name: str
    email:EmailStr
    age: int 
    weight: float 
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com']
        
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()
    
    @field_validator('age' , mode='after')#type coersion with mode
    @classmethod
    def age_validator(cls, value):
        if 0<value <100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')

def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')
 
def update_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print('inserted')   

patient_info = {'name':'shuvo','email':'ahh@hdfc.com', 'age':'30', 'weight':65.06, 'married':True, 'allergies' :['pollen'] ,'contact_details':{'email':'abc@gmail.com', 'phone':'01837739373'}}

patient1 = patient(**patient_info)

insert_patient_data(patient1)