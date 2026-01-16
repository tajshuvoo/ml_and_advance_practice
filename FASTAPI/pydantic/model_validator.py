from pydantic import BaseModel , EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List,Dict, Optional, Annotated

class patient(BaseModel):
    
    name: str
    email:EmailStr
    age: int 
    weight: float 
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age >60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model

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