

import json
import os
import time
from sys import getsizeof,exit





class File_storage:    
    #Assigning Value for objects
    def __init__(self ):
        self.key = None
        self.value = None
        self.dict = {}
        self.path = None
    
   #select your path if you need to be change
    def selected_path(self):
        print("1.Choose Current Working Directory") #
        print("2.Enter your own directory")
        x = int(input())
        if x == 1:
            self.path = os.getcwd()
        elif x== 2:
            self.path = input()
        #return self.path
    #Database updation Function
    def file_write(self , data):
        with open(os.path.join(self.path , "message.json") , "w") as file:
            json_object = json.dump(data,file,indent = 4)
            return True
            #print("file writed Successfully")
            
    
        
    def view(self):
        with open(os.path.join(self.path , "message.json") , "r") as file:
            data = json.load(file)
            for key ,value in data.items():
                if time.time() < value[1]:
                    
                    print("{0}  : {1}".format(key , value[0]))
                else:
                    print("Key Already Expired")
            

# create operation 
#use syntax "create(key_name,value,timeout_value)" timeout is optional you can continue by passing two arguments without timeout    
    def create(self ,key , value , time_expired):
        self.key = key
        self.value = value
        timeout = 0
        if self.key not in self.dict:
            if (self.key.isalpha()):
                if len(self.key) < 32: #length of key 32 chars
                    if(getsizeof(value) < (16000)): #value for data is less than 16MB
                        with open(os.path.join(self.path , "message.json"),'r') as file: #opening database
                            self.dict = json.load(file)
                            if time_expired == 0:
                                self.dict[self.key] = [self.value , time_expired]
                                data = self.dict
                                self.file_write(data)
                            else:
                                self.dict[self.key] = [self.value , time.time() + time_expired] # creating key,value with expiration time
                                data = self.dict
                                self.file_write(data)

                    else:
                        print("..........Value Limit Exists.............") #value limit exists 
                else:
                    print("Please provide the key support length 32 character only ")#error:provide key less than 32 char
                    
            else:
                print("Invalid Key ,Key must Provide only Alphebet Not Numbers and Special character") #error:create a key only Alphabet
        else:
            print("Key Already Exist in the Database") # error: key Exists in the Database 
            time.sleep(2)
            
            
            
    #Read operation performing read operation if the exist in the DataBase if exist return the Value,otherwise Key should be expired
    #use syntax def funtion(reference_obj ,paramater key)
    def read(self ,key):
        #paramater key:string
        with open(os.path.join(self.path , "message.json") , 'r') as file:
            data = json.load(file)
        if  key not in data:
            
            print("Key Cannot Exists in the DataBase") #error: key not exist in the Database
        else:
            current_time = time.time()
            if current_time < data[key][1]:
                string = str(key) +':'+ str(data[key][0]) 
                return string
            else:
                self.delete(key)
                print("Time to live key already expired ") # error Time-to-live key expired
        
        
        
        
        
    # Delete Operation: performing delete operation if the exist in the DataBase if exist delete the key Value,otherwise Key should be expired
    def delete(self ,key):
        self.key = key
        with open(os.path.join(self.path , "message.json") , 'r') as file:
            data = json.load(file)
            if self.key not in data:
                str = "Key Not Exists In The Database" #error: key not exist in the Database
                return str
            else:
                if self.key in data:
                    
                    if time.time() < data[self.key][1]: #comparing current time and expired time 

                        del data[self.key]
                        self.file_write(data)
                        str = "key Delected Successfully"
                        return str
                    else:
                        del data[self.key]
                        self.file_write(data) #update database
                        print("Time to live key already expired ") # error Time-to-live key expired
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Delete Operation: performing delete operation if the exist in the DataBase if exist Modify the key,otherwise Key  expired cannot Modified
    
    def modify(self , key , value):
        self.key = key
        self.value = value
        with open(os.path.join(self.path , "message.json") , 'r') as file:
            data = json.load(file)
            if key not in data:
                print("Key Not Exists in the Database") #
                
            else:
                if time.time() < data[self.key][1]: #comparing current_time is less than expired time
                    
                    data[self.key][0] = self.value
                    modify_ = self.file_write(data)
                    if modify_:
                        print("Value Updated Successfully") 
                else:
                    print("Time-to-live Key Expired Already key cannot Modified") # error Time-to-live key expired
                

dictobj = File_storage()
print(".....Local File Storage System.......")
dictobj.selected_path()
time.sleep(2)

while(1):
    time.sleep(2)
    print("1.Create Data")
    print("2.Read Data")
    print("3.Delete Data")
    print("4.Modify Data")
    print("5.View Data")
    print("6.Exit")
    user = int(input("Please Select what Operation you should Perform ?:"))
    time.sleep(1)
    if user == 1:
        key = input("Please Enter the Key:")
        value = input("Please Enter the Value:")
        time_expire = int(input("Please Enter the Time to Expire the key:"))
        dictobj.create(key , value , time_expire)
    elif user == 2:
        key = input("Enter the  key to Read:")
        read = dictobj.read(key)
        if read:
            print(read)
            print("Key Readed Successfully")
        time.sleep(1)
            #print("Key is Readed Succesfully")
    elif user == 3:
        key = input("Enter the key to Delete:")
        result = dictobj.delete(key)
        print(result)
        time.sleep(1)
    elif user == 4:
        key = input("Enter which key to be Modified:")
        value = input("Enter the New Value:")
        dictobj.modify(key , value)
        time.sleep(1)
    elif user == 5:
        #print(dictobj.view1())
        dictobj.view()
    elif user == 6:
        exit()


