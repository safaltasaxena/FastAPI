from pydantic import BaseModel,EmailStr,AnyUrl,Field
#custom data validators from Feild
#Feild is also used to attach metadata
#EmailStr is a data type provided by pydantic which is not a standard data type
from typing import List,Dict,Optional,Annotated

#importing basimodel in it to ensure pydantic schema
class Patient(BaseModel):
    #all are req by default
    name:Annotated[str,Field(max_length=50,title='Name of the patient',description='Give the name of the patient in less than 50 chars',examples=['safalta','astha'])]
    email:Optional[EmailStr]=None
    linkedin_url:Optional[AnyUrl]=None
    age:int=Field(gt=0,lt=120)
    #when we give a string it recognizes and makes it float itself inorder to stop that 
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:bool = False #setting default if not passed
    #making allegries optional give default too
    allergies:Optional[List[str]]=Field(default=None,max_length=5)
    #not just list bcz we just dont need to valdiate that this is list we need to validate all item in list is in str format
    contact_details:Dict[str,str]

def insert_paatient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')

def update_paatient_data(patient:Patient):
    print(patient.name)
    print(patient.email) 
    print(patient.age)
    print(patient.linkedin_url)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('updated')

patient_info={'name':'safalta','age':'30','weight':51.5,'married':True,'allergies':['pollen','dust'],'contact_details':{'email':'safaltasaxena7@gmail.com','phone':'98XXXXXXX'}}
patient_info1={'name':'safalta','email':'abs@gmail.com','linkedin_url':'http://linkedin.com/1234','age':'30','weight':51.5,'contact_details':{'phone':'98XXXXXXX'}}
patient2=Patient(**patient_info1)
patient1=Patient(**patient_info)

insert_paatient_data(patient1)
update_paatient_data(patient2)