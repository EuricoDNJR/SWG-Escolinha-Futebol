import os
import pyrebase
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(cert="firebase_cert_credentials.json")
        firebase_admin.initialize_app(cred)


    apiKey = os.getenv("FIREBASE_API_KEY")
    authDomain = os.getenv("FIREBASE_AUTH_DOMAIN")
    projectId = os.getenv("FIREBASE_PROJECT_ID")
    storageBucket = os.getenv("FIREBASE_STORAGE_BUCKET")
    messagingSenderId = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
    appId = os.getenv("FIREBASE_APP_ID")
    measurementId = os.getenv("FIREBASE_MEASUREMENT_ID")

    firebaseConfig = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "projectId": projectId,
    "storageBucket": storageBucket,
    "messagingSenderId": messagingSenderId,
    "appId": appId,
    "measurementId": measurementId,
    "databaseURL": ""}

    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase