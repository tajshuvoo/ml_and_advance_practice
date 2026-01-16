from pydantic import BaseModel , EmailStr, AnyUrl, computed_field
from typing import List,Dict, Optional, Annotated

class patient(BaseModel):
    
    name: str
    email:EmailStr
    age: int 
    weight: float
    height:float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.bmi)
    print('inserted')
 
def update_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print('inserted')   

patient_info = {'name':'shuvo','email':'ahh@hdfc.com', 'age':'30', 'weight':65.06,'height':1.69, 'married':True, 'allergies' :['pollen'] ,'contact_details':{'email':'abc@gmail.com', 'phone':'01837739373'}}

patient1 = patient(**patient_info)

insert_patient_data(patient1)