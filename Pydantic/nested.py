from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str


class Patient(BaseModel):
    name:str
    gender:str
    age:int
    #if add is str then eg 'house no 2, sec 66 , gurugram,pin,harayana'
    #problem arises if i need to extract only city or pin from this address
    address:Address

address_dict={'city':'mumbai','state':'maharasthra','pin':'751024'}
address1=Address(**address_dict)
Patient_dict={'name':'safalta','gender':'female','age':35,'address':address1}
patient1=Patient(**Patient_dict)
print(patient1)
#usecase
print(patient1.address.city)