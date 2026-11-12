from pydantic import BaseModel, ConfigDict

class Usercreate(BaseModel):
    name:str
    username:str
    password:str
    
class Userread(BaseModel):
    id: int
    name:str
    username:str
    
    model_config = ConfigDict(from_attributes=True)

class Createpost(BaseModel):
    title: str
    
class Readpost(BaseModel):
    id: str
    title: str
    userid: str
    model_config = ConfigDict(from_attributes=True)

class RefreshRequest(BaseModel):
    refresh_token=str
    
     
    
    