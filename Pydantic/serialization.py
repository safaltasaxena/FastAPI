#exporting pydantic model objects as json or python dict
#multiple usecase such as fastapi to build api debugging logging etc
from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str


class Patient(BaseModel):
    name:str
    gender:str='Male'
    age:int
    address:Address

address_dict={'city':'mumbai','state':'maharasthra','pin':'751024'}
address1=Address(**address_dict)
Patient_dict={'name':'safalta','age':35,'address':address1}
patient1=Patient(**Patient_dict)

#Dict
temp=patient1.model_dump()
print(temp)
print(type(temp))

#json
temp1=patient1.model_dump_json()
print(temp1)
print(type(temp1))

#include
temp2=patient1.model_dump(include=['name','gender'])
print(temp2)

#exclude
temp3 = patient1.model_dump(
    exclude={
        "name": True,
        "gender": True,
        "address": {"state": True}
    }
)
print(temp3)

#exclude unset
temp4=patient1.model_dump(exclude_unset=True)
print(temp4)