from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

#creating a end point whoever hits this will get to see "hello"

app=FastAPI() #app is an object of fastAPI class

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

#id is passed as query so not here
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open('paitents.json','r') as f:
         data=json.load(f)
    return data
#loading the json data

#related to post req
def save_data(data):
    with open('paitents.json','w') as f:
       json.dump(data,f) 

@app.get("/")
#defined a route over here 
#get signifies that if want to fetch any data from server we do get req
#our path rn is / so if anyone hits / url they get to this my api endpt

#for this end pt we create a method now
def hello():
    return {'message':'Paitent Managmenet System API'}

#uvicorn main:app --reload
#uvicorn server now listens http req

@app.get('/about')
def about():
    return {'message':'A Fully functional API to manage your paitent records'}


@app.get('/view')
def view():
    data=load_data()
    return data


#path parameters
@app.get('/patient/{patient_id}')
#enhancing the readibility for the client
def view_patient(patient_id:str=Path(...,description="ID of the patient in the DB",example='P001')):
   #load all the paitents
   data=load_data()

   if patient_id in data:
     return data[patient_id]
   #return {'error':'patient not found'}
   #the problem comes is that this message comes and 200 code but thats wrong code should be 400 thus we raise exception
   raise HTTPException(status_code=404,detail='Patient not found')
  

  #query parameters
  #     query
  #    ____|____
  #    |        |
  #  sortby    order
  #___|___    ___|___
  #|  |   |   |      |
  #weight     asc    desc
  #height 
  #BMI

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height , weight or bmi'),order:str=Query('asc',description='Sort in asc or desc order')):
    valid_feilds=['height','weight','bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f'Invalid feild select from{valid_feilds}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid order select from asc or desc')
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data


#post request
#sending info req body in json format
@app.post('/create')
def create_patient(patient:Patient):
    #load exisiting data
    data=load_data()
    #check if the patient alr exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient alr exists')
    #new patient added to db
    #exisiting data is py dict and new data is pydantic object
    #so we gotta make pydantic object into a dict py
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save the pyhton dict to json file
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})


#update endpoint
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,pateint_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient  not found')
    
    existing_patient_info=data[patient_id]
    
    #converting pydantic object to dictorny for mutation
    updated_patient_info=pateint_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value

    #to handle computed feilds we will work as follows
    #existing_patient_info->pydantic object->update bmi+verdict->pydantic object->dict->save
    existing_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')


    data[patient_id]=existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient updated'})

#delete(query para,pateint id)
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient delted'})
