from . import models

def create_user(firebaseId: str):
    return models.User.create(firebaseId=firebaseId)