import os
import dotenv
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ...utils.helper import firebase
from firebase_admin import auth
from ...dependencies import get_token_header
from ...utils.db import crud
from ...utils.helper import logging

dotenv.load_dotenv()

TEST = os.getenv("TEST")

router = APIRouter()

from pydantic import BaseModel

class SignUpSchema(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }


class LoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }

@router.post('/signup', dependencies=[Depends(get_token_header)])
async def create_an_account(user_data:SignUpSchema, jwt_token:str = Header(...)):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email = email,
            password = password
        )

        logging.info("Decoding firebase JWT token")
        decoded_token = {"uid": jwt_token}

        if TEST != "ON":
            decoded_token = auth.verify_id_token(jwt_token)

        elif jwt_token != "test":
            raise auth.InvalidIdTokenError("Invalid JWT token")

        logging.info(f"Firebase JWT Token decoded")

        logging.info("Inserting user into database")
        user = crud.create_user(firebaseId=decoded_token["uid"])
        logging.info("User inserted into database")
    
        return JSONResponse(content={"message" : f"User account created successfuly for user {user.id}"},
                            status_code= 201
               )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail= f"Account already created for the email {email}"
        )





@router.post('/login')
async def create_access_token(user_data:LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email = email,
            password = password
        )

        token = user['idToken']

        return JSONResponse(
            content={
                "token":token
            },status_code=200
        )

    except:
        raise HTTPException(
            status_code=400,detail="Invalid Credentials"
        )

@router.post('/ping', dependencies=[Depends(get_token_header)])
async def validate_token(jwt_token:str = Header(...)):

    user = auth.verify_id_token(jwt_token)

    return user["uid"]
