from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
#Feild_validator is used for making custom validation checks and for transformation too
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

    name:str
    email:EmailStr
    age:int
    weight:float
    height:float
    married:bool
    allergeies:List[str]
    contact_details:Dict[str,str]

    #computed feild(dynamic,usese other feilds)
    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    #custom complex data validation
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icic.com']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    #transform
    @field_validator('name',mode='after')#by default after
    @classmethod
    def transform_name(ls,value):
        return value.upper()
    
    #modes of feild validator
    @field_validator('age',mode='after')#dosent work with before
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        else:
            raise ValueError('age should be in between 0 to 100')
    
    #when data validation depends on multiple feilds
    #gonna use model validator
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
           raise ValueError('Patients older than 60 must have an emergency contact')
        return model 


def update_paatient_data(patient:Patient):
    print(patient.name)
    print(patient.email) 
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergeies)
    print(patient.contact_details)
    print(patient.calculate_bmi)
    print('updated')

patient_info={'name':'safalta','height':1.72,'allergeies':['pollen','dust'],'email':'abs@hdfc.com','age':'70','weight':51.5,'married':True,'allergies':['pollen','dust'],'contact_details':{'email':'safaltasaxena7@gmail.com','phone':'98XXXXXXX','emergency':'99XXXXXXX'}}
patient=Patient(**patient_info)# validation,type coercion

update_paatient_data(patient)