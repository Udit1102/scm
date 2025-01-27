from typing import Union
from pydantic import BaseModel

#defining the models - registration, login, shipment

class User(BaseModel):
	first_name: str
	last_name: str
	username: str
	role: str= "User"

class UserInDB(User):
    hashed_password: str

class ShipmentCreation(BaseModel):
	shipment_no: str
	container_no: str
	route: str
	goods_type: str
	expected_delivery_date: str
	po_no: str
	device: str
	delivery_no: str
	ndc_no: str
	batch_id: str
	serial_no: str
	shipment_description: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None


