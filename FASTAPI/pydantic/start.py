from pydantic import BaseModel , EmailStr, AnyUrl, Field
from typing import List,Dict, Optional, Annotated

class patient(BaseModel):
    
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['shuvo', 'tajbir'])]
    email:EmailStr
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float , Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False , description='Is the patient married or not!')]
    allergies: Annotated[Optional[List[str]], Field(default=None ,max_length=5)]
    contact_details: Dict[str, str]


def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')
 
def update_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print('inserted')   

patient_info = {'name':'shuvo','email':'ahh@gmail.com', 'age':'300', 'weight':65.06, 'married':True, 'contact_details':{'email':'abc@gmail.com', 'phone':'01837739373'}}

patient1 = patient(**patient_info)

insert_patient_data(patient1)