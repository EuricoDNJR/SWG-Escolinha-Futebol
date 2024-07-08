import os

import dotenv
from fastapi import Header, HTTPException, status
from firebase_admin import auth

dotenv.load_dotenv()

TEST = os.getenv("TEST")


async def get_token_header(jwt_token: str = Header()):
    try:
        if TEST == "ON":
            if jwt_token != "test":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid JWT token"
                )

            return "test"

        decoded_token = auth.verify_id_token(jwt_token) 
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid JWT token"
            )

        return decoded_token

    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token")