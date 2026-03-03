from fastapi import FastAPI,Path,HTTPException,Query
import json

#creating a end point whoever hits this will get to see "hello"

app=FastAPI() #app is an object of fastAPI class

def load_data():
    with open('paitents.json','r') as f:
         data=json.load(f)
    return data
#loading the json data

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

