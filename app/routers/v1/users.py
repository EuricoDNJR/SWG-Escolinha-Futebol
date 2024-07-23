import os
import dotenv
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional
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
    cargo:str
    nome:str

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email:str
    password:str

    model_config = ConfigDict(from_attributes=True)

@router.post('/signup/', dependencies=[Depends(get_token_header)])
async def create_an_account(user_data:SignUpSchema, jwt_token:str = Header(...)):
    """
    Create an account for the user.
    E.g:

        {
            "email": "soumteste2@gmail.com",
            "password": "bombadorato1",
            "cargo": "Professor",
            "nome": "João"
        }

    """
    email = user_data.email
    password = user_data.password
    cargo = user_data.cargo

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
        user = crud.create_user(firebaseId=user.uid, firebaseIdWhoCreated=decoded_token["uid"], email=user.email, cargo=cargo, nome=user_data.nome)
        logging.info("User inserted into database")
    
        return JSONResponse(content={"message" : f"User account created successfuly for user {user.id}"},
                            status_code= 201
               )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail= f"Account already created for the email {email}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail= f"Error creating account for email {email} {e}"
        )




@router.post('/login/')
async def create_access_token(user_data:LoginSchema):
    """
    Create an access token for the user.
        E.g:

        {
            "email": "joaocesar@gmail.com",
            "password": "bombadorato1"
        }

    """
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

@router.get('/all_users/', dependencies=[Depends(get_token_header)])
async def get_all_users(jwt_token:str = Header(...)):

    logging.info("Decoding firebase JWT token")
    try:
        if TEST != "ON":
            decoded_token = auth.verify_id_token(jwt_token)

        elif jwt_token != "test":
            raise auth.InvalidIdTokenError("Invalid JWT token")

        logging.info(f"Firebase JWT Token decoded")

        logging.info("Getting all users from database")
        users = crud.get_all_users()
        
        if users is not None:
            logging.info("Users found successfully")
            return JSONResponse(status_code=200, content=users)
        else:
            logging.error("No users found")
            return JSONResponse(status_code=404, content={"message": "Nenhum usuario encontrado!"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={"message": "Erro ao buscar os usuarios: " + str(e)}
        )

@router.get('/all_teachers/', dependencies=[Depends(get_token_header)])
async def get_all_teachers(jwt_token:str = Header(...)):

    logging.info("Decoding firebase JWT token")
    try:
        if TEST != "ON":
            decoded_token = auth.verify_id_token(jwt_token)

        elif jwt_token != "test":
            raise auth.InvalidIdTokenError("Invalid JWT token")

        logging.info(f"Firebase JWT Token decoded")

        logging.info("Getting all teachers from database")
        teachers = crud.get_all_teachers()
        
        if teachers is not None:
            logging.info("Teachers found successfully")
            return JSONResponse(status_code=200, content=teachers)
        else:
            logging.error("No teachers found")
            return JSONResponse(status_code=404, content={"message": "Nenhum professor encontrado!"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={"message": "Erro ao buscar os professores: " + str(e)}
        )

@router.get('/user_by_id/{id}', dependencies=[Depends(get_token_header)])
async def get_user_by_id(id:str, jwt_token:str = Header(...)):

    logging.info("Decoding firebase JWT token")
    try:
        if TEST != "ON":
            decoded_token = auth.verify_id_token(jwt_token)

        elif jwt_token != "test":
            raise auth.InvalidIdTokenError("Invalid JWT token")

        logging.info(f"Firebase JWT Token decoded")

        logging.info("Getting user by id from database")
        user = crud.get_user_by_id(id)
        
        if user is not None:
            logging.info("User found successfully")
            return JSONResponse(status_code=200, content=user)
        else:
            logging.error("No user found")
            return JSONResponse(status_code=404, content={"message": "Nenhum usuario encontrado!"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={"message": "Erro ao buscar o usuario: " + str(e)}
        )

class UpdateUserSchema(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    cargo: Optional[str] = None
    nome: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

@router.patch('/update_user/{id}', dependencies=[Depends(get_token_header)])
async def update_user(id: str, user_data: UpdateUserSchema, jwt_token: str = Header(...)):
    """
    Update user by id.

    E.g:

        {
            "email": "troquei@gmail.com",
            "password": "bombadorato1",
            "cargo": "Professor",
            "nome": "João"
        }

    """

    logging.info("Decoding firebase JWT token")
    try:
        if TEST != "ON":
            decoded_token = auth.verify_id_token(jwt_token)
        elif jwt_token != "test":
            raise auth.InvalidIdTokenError("Invalid JWT token")

        logging.info(f"Firebase JWT Token decoded")

        logging.info("Updating user in database")
        user = crud.update_user(id=id, email=user_data.email, cargo=user_data.cargo, nome=user_data.nome)
        print(user['firebaseId'])
        # Update user in Firebase
        if user_data.email or user_data.password:
            update_data = {}
            if user_data.email:
                update_data['email'] = user_data.email
            if user_data.password:
                update_data['password'] = user_data.password
            
            logging.info("Updating user in Firebase")
            auth.update_user(user['firebaseId'], **update_data)
            logging.info("User updated in Firebase")
        
        if user is not None:
            logging.info("User updated successfully")
            return JSONResponse(status_code=200, content=user)
        else:
            logging.error("No user found")
            return JSONResponse(status_code=404, content={"message": "Nenhum usuario encontrado!"})
    except auth.EmailAlreadyExistsError as e:
        logging.error(f"Firebase auth error: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar no Firebase: {e}")
    except auth.UserNotFoundError as e:
        logging.error(f"Firebase auth error: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar no Firebase: {e}")
    except auth.InvalidIdTokenError as e:
        logging.error(f"Firebase auth error: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar no Firebase: {e}")
    except Exception as e:
        logging.error(f"General error: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Erro ao atualizar o usuario: " + str(e)}
        )