
#senior programmer developed this code 
def insert_patient_data(name:str,age:int):
    #typehinting would still accept string 
        #we modify whole code
        if age<0:
             raise ValueError('age cantt be -ve')
             #data validation

        if type(name)==str and type(age)==int:
            print(name)
            print(age)
            print('inserted into db')
        else:
            raise TypeError('Incorrect data type')
        #type validation

        #this method is not good enuf not scalable

       # print(name)
       # print(age)
       # print('inserted into database')


#now junior programmer will use this code and for the time being that code is not visible to him
#insert_patient_data('safalta','thirty')
#now the problem comes age was expected to be int but he put string
#insert_patient_data('safalta','30')#still problem

def update_patient_data(name:str,age:int):

        if type(name)==str and type(age)==int:

            if age<0:
             raise ValueError('age cantt be -ve')
            
            print(name)
            print(age)
            print('updated')
        else:
            raise TypeError('Incorrect data type')
        
#so now wrote all that enforced error logic again we cant write it 100 times in prodution level work

#pydantic helps in avoiding writing so much boiler plate code to ensure type and data validation code